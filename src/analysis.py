"""
Completions -> residents: does new dwelling supply explain population change
at district level in Berlin (12 Bezirke) and Copenhagen (10 bydele), 2010-2025?

Run: uv run python src/analysis.py
Writes all tables/figures/report into outputs/.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from skimpy import skim

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# dataviz palette (categorical slots 1 & 2; see dataviz skill reference)
# ---------------------------------------------------------------------------
BLUE = "#2a78d6"      # Berlin
ORANGE = "#eb6834"    # Copenhagen
GRAY_TXT = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"
RED = "#e34948"        # reference line / robustness

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": "#0b0b0b",
    "text.color": "#0b0b0b",
    "xtick.color": GRAY_TXT,
    "ytick.color": GRAY_TXT,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
    "figure.dpi": 150,
    "savefig.dpi": 150,
})

CITY_COLOR = {"Berlin": BLUE, "Copenhagen": ORANGE}

BERLIN_HH_SIZE = 1.8   # persons per dwelling, benchmark (Berlin ~1.8)
CPH_HH_SIZE = 1.95     # persons per dwelling, benchmark (Copenhagen ~1.9-2.0)

YEARS = list(range(2010, 2026))

# ===========================================================================
# 1. Build the panel
# ===========================================================================

def load_berlin() -> pd.DataFrame:
    comp = pd.read_csv(DATA / "berlin_completions_by_district.csv")
    pop = pd.read_csv(DATA / "berlin_population_by_district.csv")

    comp_w = comp.pivot_table(index=["year", "district"], columns="measure",
                               values="value", aggfunc="sum").reset_index()
    df = comp_w.merge(pop[["year", "district", "population"]],
                       on=["year", "district"], how="outer")
    df["city"] = "Berlin"
    return df


def load_copenhagen() -> pd.DataFrame:
    comp = pd.read_csv(DATA / "copenhagen_completions_by_district.csv")
    pop = pd.read_csv(DATA / "copenhagen_population_by_district.csv")

    dwellings_measure = "dwellings_by_commissioning_year (stock, ref. 2026)"
    comp = comp[comp["measure"] == dwellings_measure][["year", "district", "value"]]
    comp = comp.rename(columns={"value": "dwellings_total"})
    df = comp.merge(pop[["year", "district", "population"]],
                     on=["year", "district"], how="outer")
    df["city"] = "Copenhagen"
    return df


def build_panel() -> pd.DataFrame:
    b = load_berlin()
    c = load_copenhagen()
    panel = pd.concat([b, c], ignore_index=True, sort=False)
    panel = panel.sort_values(["city", "district", "year"]).reset_index(drop=True)

    # population change (register stock difference, 31 Dec t vs 31 Dec t-1 /
    # Q4 t vs Q4 t-1 for Copenhagen)
    panel["pop_change"] = panel.groupby(["city", "district"])["population"].diff()

    # completions per 1000 residents (using same-year population as denominator)
    panel["completions_per_1000"] = 1000 * panel["dwellings_total"] / panel["population"]

    # pop change per completion (same year)
    panel["pop_change_per_completion"] = panel["pop_change"] / panel["dwellings_total"]

    # lagged completions (previous year's completions explaining this year's pop change)
    panel["dwellings_total_lag1"] = panel.groupby(["city", "district"])["dwellings_total"].shift(1)
    if "dwellings_new_residential" in panel.columns:
        panel["dwellings_new_residential_lag1"] = panel.groupby(["city", "district"])[
            "dwellings_new_residential"].shift(1)

    return panel


panel = build_panel()
panel.to_csv(OUT / "panel.csv", index=False)

# ===========================================================================
# 2. Descriptives
# ===========================================================================

with open(OUT / "skim_summary.txt", "w") as f:
    import contextlib
    with contextlib.redirect_stdout(f):
        skim(panel)

city_year_totals = (panel.groupby(["city", "year"])
                    .agg(completions=("dwellings_total", "sum"),
                         population=("population", "sum"),
                         pop_change=("pop_change", "sum"))
                    .reset_index())
city_year_totals.to_csv(OUT / "city_year_totals.csv", index=False)

# district shares of completions vs district shares of pop growth, cumulative 2010-2024
window = panel[(panel["year"] >= 2010) & (panel["year"] <= 2024)]
cum = (window.groupby(["city", "district"])
       .agg(completions_cum=("dwellings_total", "sum"),
            pop_change_cum=("pop_change", "sum"))
       .reset_index())
cum["completions_share"] = cum["completions_cum"] / cum.groupby("city")["completions_cum"].transform("sum")
cum["pop_growth_share"] = cum["pop_change_cum"] / cum.groupby("city")["pop_change_cum"].transform("sum")
cum.to_csv(OUT / "district_shares_cumulative.csv", index=False)

# ===========================================================================
# 3. Regressions
# ===========================================================================

def fe_ols(df: pd.DataFrame, y: str, x: str, extra_fe: bool = True):
    """OLS of y on x with district and year fixed effects (dummy absorption)."""
    d = df.dropna(subset=[y, x, "district", "year"]).copy()
    if d["district"].nunique() < 2 or len(d) < 10:
        return None
    formula = f"{y} ~ {x} + C(district)"
    if extra_fe and d["year"].nunique() > 1:
        formula += " + C(year)"
    model = smf.ols(formula, data=d).fit(cov_type="cluster",
                                          cov_kwds={"groups": d["district"]})
    return model


def summarize_model(model, label: str, xvar: str) -> dict:
    if model is None:
        return {"spec": label, "coef": np.nan, "se": np.nan, "ci_low": np.nan,
                 "ci_high": np.nan, "n": np.nan, "r2": np.nan}
    coef = model.params.get(xvar, np.nan)
    se = model.bse.get(xvar, np.nan)
    ci = model.conf_int().loc[xvar] if xvar in model.params.index else (np.nan, np.nan)
    return {"spec": label, "coef": coef, "se": se, "ci_low": ci[0], "ci_high": ci[1],
            "n": int(model.nobs), "r2": model.rsquared}


results = []

for city in ["Berlin", "Copenhagen"]:
    sub = panel[panel["city"] == city]

    m_same = fe_ols(sub, "pop_change", "dwellings_total")
    results.append({**summarize_model(m_same, f"{city}: same-year, dwellings_total, district+year FE", "dwellings_total"), "city": city})

    m_lag = fe_ols(sub, "pop_change", "dwellings_total_lag1")
    results.append({**summarize_model(m_lag, f"{city}: lag1, dwellings_total, district+year FE", "dwellings_total_lag1"), "city": city})

    if "dwellings_new_residential" in sub.columns and sub["dwellings_new_residential"].notna().any():
        m_newres = fe_ols(sub, "pop_change", "dwellings_new_residential")
        results.append({**summarize_model(m_newres, f"{city}: same-year, dwellings_new_residential, district+year FE", "dwellings_new_residential"), "city": city})

# ---- cumulative cross-section (2010-2024), one point per district ----
cum_pooled = cum.copy()
cum_pooled["city_d"] = cum_pooled["city"]

def cross_section_ols(df, label, cluster=False):
    d = df.dropna(subset=["pop_change_cum", "completions_cum"])
    formula = "pop_change_cum ~ completions_cum"
    model = smf.ols(formula, data=d).fit()
    return summarize_model(model, label, "completions_cum")

results.append({**cross_section_ols(cum[cum.city == "Berlin"], "Berlin: cumulative 2010-2024 cross-section (12 districts)"), "city": "Berlin"})
results.append({**cross_section_ols(cum[cum.city == "Copenhagen"], "Copenhagen: cumulative 2010-2024 cross-section (10 districts)"), "city": "Copenhagen"})

# pooled cross-section with city fixed effect
d_pool = cum.dropna(subset=["pop_change_cum", "completions_cum"])
m_pool = smf.ols("pop_change_cum ~ completions_cum + C(city)", data=d_pool).fit(
    cov_type="cluster", cov_kwds={"groups": d_pool["city"]})
results.append({**summarize_model(m_pool, "Pooled (Berlin+Copenhagen): cumulative cross-section, city FE", "completions_cum"), "city": "Pooled"})

reg_results = pd.DataFrame(results)
reg_results.to_csv(OUT / "regression_results.csv", index=False)

# ===========================================================================
# 4. Robustness
# ===========================================================================

robust = []

# drop Berlin 2013 (census adjustment) and 2025 (provisional); drop Cph 2025
b_robust = panel[(panel.city == "Berlin") & (~panel.year.isin([2013, 2025]))]
c_robust = panel[(panel.city == "Copenhagen") & (panel.year != 2025)]

m = fe_ols(b_robust, "pop_change", "dwellings_total")
robust.append({**summarize_model(m, "Berlin: drop 2013 & 2025, dwellings_total", "dwellings_total"), "city": "Berlin"})

m = fe_ols(c_robust, "pop_change", "dwellings_total")
robust.append({**summarize_model(m, "Copenhagen: drop 2025, dwellings_total (KKBOL1)", "dwellings_total"), "city": "Copenhagen"})

# Berlin using dwellings_new_residential, dropping 2013/2025
m = fe_ols(b_robust, "pop_change", "dwellings_new_residential")
robust.append({**summarize_model(m, "Berlin: drop 2013 & 2025, dwellings_new_residential", "dwellings_new_residential"), "city": "Berlin"})

# Copenhagen scaled by BYGV22/KKBOL1 ratio (municipality-level calibration factor)
bygv22 = pd.read_csv(DATA / "copenhagen_dst_bygv22_crosscheck.csv")
kk_city_totals = (panel[panel.city == "Copenhagen"].groupby("year")["dwellings_total"]
                  .sum().reset_index().rename(columns={"dwellings_total": "kkbol1_total"}))
ratio_df = kk_city_totals.merge(bygv22, on="year")
ratio_df["ratio"] = ratio_df["dwellings_completed"] / ratio_df["kkbol1_total"]
ratio_df.to_csv(OUT / "copenhagen_calibration_ratio.csv", index=False)

cph_scaled = panel[panel.city == "Copenhagen"].merge(
    ratio_df[["year", "ratio"]], on="year", how="left")
cph_scaled["dwellings_total_scaled"] = cph_scaled["dwellings_total"] * cph_scaled["ratio"]
m = fe_ols(cph_scaled[cph_scaled.year != 2025], "pop_change", "dwellings_total_scaled")
robust.append({**summarize_model(m, "Copenhagen: KKBOL1 scaled by BYGV22/KKBOL1 ratio, drop 2025", "dwellings_total_scaled"), "city": "Copenhagen"})

robust_df = pd.DataFrame(robust)
robust_df.to_csv(OUT / "robustness_results.csv", index=False)

# ===========================================================================
# 5. Charts
# ===========================================================================

def style_ax(ax):
    ax.grid(True, axis="y", color=GRID, linewidth=0.6)
    ax.grid(False, axis="x")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=0)


# --- 5a. small multiples: completions & pop change by district, per city ---
for city in ["Berlin", "Copenhagen"]:
    sub = panel[panel.city == city]
    districts = sorted(sub["district"].dropna().unique())
    ncols = 4
    nrows = int(np.ceil(len(districts) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 3.4, nrows * 2.6), sharex=True)
    axes = np.atleast_1d(axes).flatten()
    for i, dist in enumerate(districts):
        ax = axes[i]
        d = sub[sub.district == dist].sort_values("year")
        ax2 = ax.twinx()
        ax.bar(d["year"], d["dwellings_total"], color=CITY_COLOR[city], alpha=0.55,
               width=0.7, label="Completions")
        ax2.plot(d["year"], d["pop_change"], color="#0b0b0b", linewidth=1.6,
                  marker="o", markersize=3, label="Pop. change")
        ax2.axhline(0, color=MUTED, linewidth=0.6)
        ax.set_title(dist, fontsize=9, color="#0b0b0b")
        style_ax(ax)
        ax2.tick_params(length=0, labelsize=7)
        ax.tick_params(labelsize=7)
        ax2.grid(False)
        ax2.spines["top"].set_visible(False)
    for j in range(len(districts), len(axes)):
        axes[j].axis("off")
    fig.suptitle(f"{city}: dwelling completions (bars) vs population change (line), 2010-2025",
                 fontsize=12, y=1.02)
    handles = [plt.Rectangle((0, 0), 1, 1, color=CITY_COLOR[city], alpha=0.55),
               plt.Line2D([0], [0], color="#0b0b0b", marker="o", markersize=3)]
    fig.legend(handles, ["Completions (dwellings)", "Population change"],
               loc="upper center", bbox_to_anchor=(0.5, 1.06), ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / f"small_multiples_{city.lower()}.png", bbox_inches="tight")
    plt.close(fig)

# --- 5b. cumulative scatter with fit line and household-size reference ---
fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=False)
for ax, city, hh in zip(axes, ["Berlin", "Copenhagen"], [BERLIN_HH_SIZE, CPH_HH_SIZE]):
    d = cum[cum.city == city]
    color = CITY_COLOR[city]
    ax.scatter(d["completions_cum"], d["pop_change_cum"], color=color, s=55,
               edgecolor="white", linewidth=0.8, zorder=3)
    for _, row in d.iterrows():
        ax.annotate(row["district"], (row["completions_cum"], row["pop_change_cum"]),
                    fontsize=6.5, color=GRAY_TXT, xytext=(4, 3), textcoords="offset points")
    xs = np.linspace(0, d["completions_cum"].max() * 1.05, 100)
    # OLS fit
    coefs = np.polyfit(d["completions_cum"], d["pop_change_cum"], 1)
    ax.plot(xs, np.polyval(coefs, xs), color=color, linewidth=2, zorder=2,
             label=f"Fitted (slope={coefs[0]:.2f})")
    # household-size reference line (through origin)
    ax.plot(xs, hh * xs, color=MUTED, linewidth=1.4, linestyle="--", zorder=1,
             label=f"Household-size benchmark ({hh})")
    ax.axhline(0, color=GRID, linewidth=0.8)
    ax.set_title(f"{city}: cumulative completions vs population change, 2010-2024",
                 fontsize=10.5)
    ax.set_xlabel("Cumulative dwelling completions")
    ax.set_ylabel("Cumulative population change")
    style_ax(ax)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig(OUT / "cumulative_scatter.png", bbox_inches="tight")
plt.close(fig)

# --- 5c. city-level time series: completions per 1000 residents ---
ts = city_year_totals.copy()
ts["completions_per_1000"] = 1000 * ts["completions"] / ts["population"]
fig, ax = plt.subplots(figsize=(8.5, 5))
for city in ["Berlin", "Copenhagen"]:
    d = ts[ts.city == city].sort_values("year")
    ax.plot(d["year"], d["completions_per_1000"], color=CITY_COLOR[city],
             linewidth=2.2, marker="o", markersize=4, label=city)
style_ax(ax)
ax.set_ylabel("Completions per 1,000 residents")
ax.set_xlabel("Year")
ax.set_title("Dwelling completions per 1,000 residents, Berlin vs Copenhagen")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "completions_per_1000_timeseries.png", bbox_inches="tight")
plt.close(fig)

print("Panel shape:", panel.shape)
print("Wrote outputs to", OUT)
