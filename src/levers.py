"""Build data/processed/levers.json for "Die Lücke" / "Was bringt wie viele Wohnungen?".

Every leaf number is an object {value, unit, ref_date, spatial_unit, source, tag}
with tag in {V, S, I}. Structure and values follow docs/die-luecke-design.md §6.1
(roundA, roundB, dials) and §6.2 (partB.vergesellschaften), and the fact-checker
citation table in docs/research/opus3_design_review.md. Figures are taken from
docs/research/consolidated_findings.md unless noted inline.

Run with: uv run python src/levers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"


def n(value, unit, ref_date, spatial_unit, source, tag):
    assert tag in ("V", "S", "I"), tag
    return {"value": value, "unit": unit, "ref_date": ref_date, "spatial_unit": spatial_unit,
            "source": source, "tag": tag}


# Shared citations (fact-checker table, opus3_design_review.md §3)
SRC_ZENSUS_1122 = "Zensus 2011 & 2022, Ergebnisse Berlin (Gemeinde-Level); docs/research/stage3a_gap_report.md §1"
SRC_STEP = "StEP Wohnen 2040, Senat Berlin 2024, S. 75-77"
SRC_STEP_UPDATE = "Fortschrittsbericht StEP Wohnen 2040, Senatspressemitteilung 1682261, 16.06.2026"
SRC_FI1 = "F I 1, Statistischer Bericht, Amt für Statistik Berlin-Brandenburg"
SRC_WOHNUNGSLOSE = "AfS Berlin-Brandenburg, Wohnungslosenstatistik"
SRC_EXPERTENKOMMISSION = "Expertenkommission Vergesellschaftung, Abschlussbericht, 27.06.2023"
SRC_BERNT_HOLM = "Bernt, M. / Holm, A. (2023): Vergesellschaftung ..., RLS Studien 1/2023"
SRC_KOOPV = 'Kooperationsvereinbarung "Leistbare Mieten, mehr Neubau, soziale Wohnungspolitik", Berichte 2021-2024 (SenSBW)'
SRC_DIW126 = "DIW aktuell 126, 05.10.2026"
SRC_ZENSUS_OWNER = "Zensus 2022, Tabelle 4000W-3006, Berlin, Stichtag 15.5.2022"
SRC_RECHNUNGSHOF = "Rechnungshof Berlin, Bericht 20.02.2024"
SRC_KHOLODILIN = "Kholodilin, K. (2024): literature review of rent-control mobility effects (cited via opus3_design_review.md)"


def build() -> dict:
    data: dict = {}

    # ----------------------------------------------------------------- roundA
    tap = lambda value, unit, label, tag, source, note=None: {
        **n(value, unit, "2011-05-09/2022-05-15", "Berlin", source, tag),
        "label": label, **({"note": note} if note else {}),
    }
    data["roundA"] = {
        "label": "Runde 1, „gezählt“: Zensus 9.5.2011 → Zensus 15.5.2022",
        "arrivals": n(304614, "Personen", "2011-05-09/2022-05-15", "Berlin", SRC_ZENSUS_1122, "V"),
        "frame_text": "Die Stadt hat Platz geschaffen durch …",
        "taps": {
            "neu_gebaut": tap(149403, "Wohnungen", "Neu gebaut",
                               "V", "F II 2 Baufertigstellungen; " + SRC_ZENSUS_1122,
                               "+149.403 Whg. ≈ 267.000 Menschen (88 %)"),
            "aus_leeren_wohnungen": tap(25577, "Wohnungen", "Aus leeren Wohnungen",
                                        "V", SRC_ZENSUS_1122,
                                        "25.577 Whg. ≈ 46.000 (15 %); Leerstand 3,5 % → 2,0 %"),
            "ferienwohnungen_gewerbe_zweitwohnungen": tap(-9562, "Wohnungen", "Ferienwohnungen, Gewerbe, Zweitwohnungen",
                                                            "V", SRC_ZENSUS_1122,
                                                            "−9.562 Whg. ≈ −17.000 (−6 %)"),
            "enger_gewohnt": tap(0, "Personen", "Enger gewohnt",
                                  "I", SRC_ZENSUS_1122,
                                  "≈ 0 (± 20.000): Zensus-Haushaltsgröße bleibt bei ≈ 1,79, aber der 2011-Wert hängt an der nicht ermittelten Anstaltsbevölkerung"),
            "in_unterkuenften": tap(None, "Personen", "In Unterkünften",
                                     "I", "AfS: Unterkunftsstatistik beginnt erst 31.01.2022",
                                     "nicht gemessen (Statistik beginnt 31.01.2022); im Rest ≈ 8.500 (3 %)"),
            "umgebaut_aufgestockt": tap(None, "Wohnungen", "Umgebaut, aufgestockt",
                                        "V", "F II 2 (Baumaßnahmen an bestehenden Gebäuden, in 'Neu gebaut' enthalten)",
                                        "in „Neu gebaut“ enthalten"),
            "uebernommen": tap(0, "Personen", "Übernommen",
                                "S", "docs/research/sonnet2_transfers_allocation.md (2021-2025 LWU-Käufe)",
                                "0 Menschen; Felder färben sich um"),
            "gar_nicht_gekommen": tap(None, "Personen", "Gar nicht gekommen",
                                      "I", "A III 1 Brandenburg-Wanderung (nicht beschafft)",
                                      "nicht messbar in der Bilanz"),
        },
        "identity": {
            "formula": "149403 + 25577 - 9562 = 165418",
            "dwellings": n(165418, "Wohnungen", "2011-05-09/2022-05-15", "Berlin", SRC_ZENSUS_1122, "V"),
            "persons_per_household": n(1.79, "Personen/Haushalt", "2022-05-15", "Berlin", SRC_ZENSUS_1122, "I"),
            "label": "rechnerisch",
        },
    }

    # ----------------------------------------------------------------- roundB
    data["roundB"] = {
        "label": "Runde 2, „geschätzt“: 15.5.2022 → 31.12.2025",
        "arrivals": n(103598, "Personen", "2022-05-15/2025-12-31", "Berlin", "A I 3", "V"),
        "stock_change": n(50592, "Wohnungen", "2022-05-15/2025-12-31", "Berlin", SRC_FI1, "V"),
        "unterkuenfte_change": n(27635, "Personen", "2022-01-31/2025-01-31", "Berlin", SRC_WOHNUNGSLOSE, "V"),
        "uebernommen": {
            "dwellings": n(5400, "Wohnungen", "2023-2025", "Berlin", "docs/research/sonnet2_transfers_allocation.md (2023-2025 LWU-Ankäufe)", "V"),
            "persons": n(0, "Personen", "2023-2025", "Berlin", "docs/research/sonnet2_transfers_allocation.md", "V"),
        },
        "overlap_caveat": "Schätzung, keine Volkszählung. Die Teile ergeben mehr als 100 %, weil die Quellen sich überschneiden.",
        "overlap_pct": n(114, "%", "2022-05-15/2025-12-31", "Berlin", "I (50.592×1,79 + 27.635) / 103.598 ≈ 114 %", "I"),
    }

    # ----------------------------------------------------------------- dials
    data["dials"] = {
        "reserve": {"default": 3, "min": 0, "max": 5, "unit": "%",
                    "senate_value": n(3, "%", "2024", "Berlin", SRC_STEP, "V")},
        "hh_size": {"default": 1.77, "min": 1.70, "max": 2.00, "unit": "Personen/Haushalt",
                    "senate_value": n(1.77, "Personen/Haushalt", "2024", "Berlin", SRC_STEP, "V")},
        "bridge": {
            "formula": "total = reserve_component + relief_component + replacement_component; "
                       "at reserve=3% and hh_size=1.77 these equal 41000 + 77000 + 19000 = 137000 "
                       "(StEP Wohnen 2040 pp. 75-77). reserve_component scales linearly with the "
                       "reserve dial from a 2025 stock of 2,069,432 (0%-reserve point = 0 Wohnungen "
                       "below the stock at reserve=0, i.e. component = stock * reserve/100, "
                       "calibrated so reserve=3% -> 41000); relief_component is held at the StEP "
                       "figure (77000) at hh_size=1.77 and scales inversely with hh_size (lower "
                       "hh_size = more relief needed); replacement_component is fixed at 19000 "
                       "(StEP, 1,000/yr x 19 years to 2040) and does not depend on the dials.",
            "total_at_senate_values": n(137000, "Wohnungen", "2022-2040", "Berlin", SRC_STEP, "V"),
            "reserve_component": n(41000, "Wohnungen", "2022-2040", "Berlin", SRC_STEP, "V"),
            "relief_component": n(77000, "Wohnungen", "2022-2040", "Berlin", SRC_STEP, "V"),
            "replacement_component": n(19000, "Wohnungen", "2022-2040", "Berlin", SRC_STEP, "V"),
            "excludes": "die Menschen in Unterkünften",
            "stock_2025_for_reserve_calc": n(2069432, "Wohnungen", "2025-12-31", "Berlin", SRC_FI1, "V"),
            "update_211000": n(211000, "Wohnungen", "2026-2040", "Berlin", SRC_STEP_UPDATE, "S"),
            "update_components": {"relief": n(138000, "Wohnungen", "2026-2040", "Berlin", SRC_STEP_UPDATE, "S"),
                                   "demographic": n(73000, "Wohnungen", "2026-2040", "Berlin", SRC_STEP_UPDATE, "S")},
            "bridge_text": "Berlin hat Platz geschaffen, auch indem es Reserven aufgebraucht hat. "
                           "Stellen Sie ein, wie viel Reserve und wie viel Platz pro Haushalt Berlin "
                           "haben sollte. Mit den Werten des Senats (3 % Reserve, 1,77 Personen je "
                           "Haushalt) ergibt sich der Entlastungsbedarf von 137.000 Wohnungen: "
                           "41.000 Reserve, 77.000 Entlastung, 19.000 Ersatz (StEP Wohnen 2040). "
                           "Nicht enthalten: die Menschen in Unterkünften.",
        },
    }

    # ----------------------------------------------------------------- partB
    data["partB"] = {
        "stock_squares": n(2069, "x1000 Wohnungen", "2025-12-31", "Berlin", SRC_FI1, "V"),
        "senate_need": n(211000, "Wohnungen", "2026-2040", "Berlin", SRC_STEP_UPDATE, "S"),
        "caveats": [
            "Die Zahlen beruhen auf der zensus-korrigierten Bevölkerung (Zensus 2011 und die "
            "Fortschreibung auf Basis 2022), nicht auf dem Melderegister. Das Register zeigt seit "
            "2011 rund 78.000 mehr Wachstum wegen veralteter Anmeldungen.",
            "Die Haushaltsgröße ist eine Annahme, und sie ist gestiegen, nicht gefallen. Je "
            "0,05 Personen ändert sich die Berliner Lücke um etwa 5.000-6.000 Wohnungen. Der "
            "Berliner Durchschnitt stieg von 1,75 (2011) auf 1,85 (2024).",
            "„Lücke“ hier ist nicht „Bedarf“. Sie zeigt den Rückstand des Bauens "
            "gegenüber dem Bevölkerungswachstum seit 2011, sichtbar am sinkenden Leerstand "
            "(3,5 % → 2,0 %). Die 137.000/138.000 des Senats sind ein Zielwert, kein gemessener "
            "Rückstand.",
        ],
        "levers": {
            "neu_bauen": {
                "felder": n(11.0, "x1000 Wohnungen/Jahr", "2025", "Berlin", "F II 2 Baufertigstellungen", "V"),
                "tempo_2025": n(11.0, "x1000/Jahr", "2025", "Berlin", "F II 2", "V"),
                "tempo_2019": n(19.0, "x1000/Jahr", "2019", "Berlin", "F II 2", "V"),
                "wer_zahlt": "gemischt (privat, LWU, Land)",
                "lwu": n(4.7, "x1000/Jahr", "2025", "Berlin", SRC_KOOPV, "V"),
                "quelle": "F II 2 Baufertigstellungen; KoopV-Jahresbericht 2024",
            },
            "ueberhang": {
                "felder": n(48.4, "x1000 Wohnungen", "2025-12-31", "Berlin", "F II 2 Tab. 17", "V"),
                "unter_dach": n(12.9, "x1000 Wohnungen", "2025-12-31", "Berlin", "F II 2 Tab. 17", "V"),
                "rohbau": n(12.3, "x1000 Wohnungen", "2025-12-31", "Berlin", "F II 2 Tab. 17", "V"),
                "nicht_begonnen": n(15.8, "x1000 Wohnungen", "2025-12-31", "Berlin", "F II 2 Tab. 17", "V"),
                "quelle": "F II 2, Statistischer Bericht, Tabellen 16-17",
            },
            "leerstand": {
                "market_active": n(5.4, "x1000 Wohnungen", "2024", "Berlin", "CBRE-empirica Leerstandsindex", "V"),
                "ceiling": n(11.8, "x1000 Wohnungen", "2022-05-15", "Berlin", "Zensus 2022, Drs. 19/20607", "V"),
                "quelle": "CBRE-empirica Leerstandsindex 2025; Zensus 2022 / Drs. 19/20607",
            },
            "ferienwohnungen": {
                "listings": n(8.4, "x1000 Inserate", "2026-09-19", "Berlin", "Inside Airbnb", "V"),
                "active": n(4.9, "x1000 Inserate", "2026-09-19", "Berlin", "Inside Airbnb (in letzten 12 Monaten bewertet)", "V"),
                "returned_since_2014": n(8.3, "x1000 Wohnungen", "2014-2025-06-30", "Berlin", "Drs. 19/24230; 19/21276", "V"),
                "per_year": n(0.5, "x1000/Jahr", "2020-2025", "Berlin", "Drs. 19/24230; 19/21276", "V"),
                "quelle": "Inside Airbnb; Senatsverwaltung Drs. 19/24230, 19/21276",
            },
            "zweckentfremdung_gesamt": {
                "felder": n(31.7, "x1000 Wohnungen", "2014-2025-06-30", "Berlin", "Drs. 19/24230", "V"),
                "quelle": "Drs. 19/24230 (Zweckentfremdungsverbot, seit 2014 zurückgeführt)",
            },
            "aufstocken_umnutzen": {
                "supermaerkte": n([20, 36], "x1000 Wohnungen", "2019", "Berlin", "Deutschlandstudie 2019 (TU Darmstadt + Pestel)", "S"),
                "buero": n(30, "x1000 Wohnungen", "2025", "Berlin", "bulwiengesa/Berlin Hyp Kurzstudie 2025", "S"),
                "quelle": "Deutschlandstudie 2019; bulwiengesa/Berlin Hyp 2025",
            },
            "sozialbindungen": {
                "felder": n(-46, "x1000 Wohnungen", "2024-2034", "Berlin", "IBB Wohnungsmarktbericht 2024", "V"),
                "note": "Sozialbindungen laufen aus; kein Zugewinn, Darstellung recolour-reverse",
                "quelle": "IBB Wohnungsmarktbericht 2024",
            },
            "unterkuenfte": {
                "felder": n(54, "x1000 Personen", "2025-01-31", "Berlin", SRC_WOHNUNGSLOSE, "V"),
                "note": "Bedarfsmarker, keine Wohnungs-Angebotszahl",
                "quelle": "AfS Wohnungslosenstatistik",
            },
            "vergesellschaften": {
                "umfang": {
                    "value": n(222, "x1000 Wohnungen", "2021-12-31", "Berlin", SRC_EXPERTENKOMMISSION, "V"),
                    "neue_wohnungen": n(0, "Wohnungen", "2021-12-31", "Berlin", SRC_EXPERTENKOMMISSION, "V"),
                    "share_all_dwellings": n(10.7, "%", "2021-12-31", "Berlin", SRC_EXPERTENKOMMISSION, "I"),
                    "share_rental_stock": n(13.5, "%", "2021-12-31", "Berlin", SRC_EXPERTENKOMMISSION, "V"),
                    "text": "222.000 Wohnungen großer Vermieter (ab 3.000 Wohnungen) gingen an eine "
                            "Anstalt öffentlichen Rechts. Neue Wohnungen: 0.",
                },
                "vergabe": {
                    "net_flow_low": n(3300, "Wohnungen/Jahr", "2024", "Berlin", "I (3,3 % Fluktuation x 75 % Quote vs. 30 % Bündnis-Quote), siehe " + SRC_BERNT_HOLM + " und " + SRC_KOOPV, "I"),
                    "net_flow_high": n(5000, "Wohnungen/Jahr", "2024", "Berlin", "I (5 % Fluktuation x 63-75 % Quote vs. 30 % Bündnis-Quote)", "I"),
                    "campaign_gross_quote": n(6999, "Wohnungen/Jahr", "2023", "Berlin", SRC_BERNT_HOLM, "S"),
                    "lock_in_text": "Risiko: Wer günstig wohnt, zieht seltener um (25 von 26 Studien, " + SRC_KHOLODILIN + "). "
                                    "Gegenschätzung (bankfinanziert, nicht kausal): empirica/Simons 2026 ≈ 7.200 "
                                    "Wohnungen Fläche außer Umlauf, „grob und ausdrücklich ohne Anspruch auf "
                                    "Kausalität“.",
                    "text": "Pro Jahr würden rund 3.300-5.000 Wohnungen mehr an Haushalte mit WBS "
                            "vermietet als heute. Gleiche Wohnungen, andere Mieter. Die Initiative "
                            "rechnet mit 7.000 (brutto). Risiko: Wer günstig wohnt, zieht seltener "
                            "um (25 von 26 Studien).",
                    "axis_note": "eigene Achse: Jahresfluss, nicht Teil der Waffel-Quadrate",
                },
                "miete": {
                    "rent_relief_pct": n(-16, "%", "2023", "Berlin", SRC_BERNT_HOLM, "S"),
                    "rent_relief_eur_per_hh_year": n(936, "EUR/Haushalt/Jahr", "2023", "Berlin", SRC_BERNT_HOLM, "S"),
                    "text": "−16 % für Neuvermietete, ca. 936 € pro Haushalt und Jahr "
                            "(Schätzung der Initiative, Bernt/Holm 2023).",
                },
                "kosten": {
                    "compensation_low_bn_eur": n(8, "Mrd. EUR", "2024", "Berlin", SRC_RECHNUNGSHOF, "V"),
                    "compensation_high_bn_eur": n(36, "Mrd. EUR", "2024", "Berlin", SRC_RECHNUNGSHOF, "V"),
                    "diw_annual_low_bn_eur": n(-0.3, "Mrd. EUR/Jahr", "2026", "Berlin", SRC_DIW126, "V"),
                    "diw_annual_high_bn_eur": n(1.1, "Mrd. EUR/Jahr", "2026", "Berlin", SRC_DIW126, "V"),
                    "no_dwelling_conversion": True,
                    "text": "Entschädigung 8-36 Mrd. € (Schätzungen 2019-2026), über Kredite "
                            "und Mieten finanziert. Jährliche Belastung für den Landeshaushalt: "
                            "−0,3 bis +1,1 Mrd. € (DIW, je nach Entschädigung und Miete).",
                },
                "bauen": {
                    "toggle": True,
                    "quotes": [
                        {"side": "Mehrheit Expertenkommission", "text": "verspricht einen hohen Beitrag zum Neubau, wenn gesetzlich vorgegeben", "source": SRC_EXPERTENKOMMISSION, "tag": "V"},
                        {"side": "Sondervotum (Minderheit)", "text": "nicht belegt und eher unplausibel", "source": SRC_EXPERTENKOMMISSION, "tag": "V"},
                        {"side": "Initiative (AöR-Konzept)", "text": "nach einer Konsolidierungsphase sind auch eigene Neubauprojekte … denkbar", "source": "DW & Co. enteignen, AöR-Konzept", "tag": "V"},
                    ],
                    "text": "Mehrheit der Kommission: „verspricht einen hohen Beitrag“ zum Neubau, "
                            "wenn gesetzlich vorgegeben. Minderheit: „nicht belegt und eher "
                            "unplausibel“. Initiative: eigene Neubauprojekte „denkbar“. Keine Zahl.",
                    "risk_band": {
                        "private_share_pct": n([42, 46], "%", "2008-2025", "Berlin", SRC_DIW126, "V"),
                        "label": "alle privaten Wohnungsunternehmen",
                        "text": "Private Wohnungsunternehmen bauten 42-46 % der neuen Wohnungen (DIW). "
                                "Welcher Teil davon auf die betroffenen Konzerne entfällt, ist nicht "
                                "veröffentlicht.",
                    },
                },
                "vacancy_card": {
                    "private_company_pct": n(2.07, "%", "2022-05-15", "Berlin", SRC_ZENSUS_OWNER, "V"),
                    "berlin_pct": n(2.02, "%", "2022-05-15", "Berlin", SRC_ZENSUS_OWNER, "V"),
                    "implied_vacant_of_222000": n(4600, "Wohnungen", "2022-05-15", "Berlin", "I (2,07 % x 222.000)", "I"),
                    "district_range_caveat": "Bezirk-Spanne 1,1-2,9 % beruht auf kleinen Zellen, hier nicht gezeigt.",
                    "text": "Stehen bei den Konzernen Wohnungen leer? Kaum mehr als anderswo: 2,1 % bei "
                            "privaten Wohnungsunternehmen, 2,0 % in ganz Berlin (Zensus, 15.5.2022; "
                            "Leerstand wegen Sanierung eingerechnet). Bei gleicher Quote wären das "
                            "etwa 4.600 der 222.000. Nicht gemessen: Verdrängung aus bewohnten "
                            "Wohnungen.",
                },
                "quotes_both_sides": [
                    {"side": "Initiative", "text": "nicht gegen Neubau", "source": "docs/research/sonnetB_enteignen_supply.md", "tag": "S"},
                    {"side": "AöR-Konzept", "text": "nach einer Konsolidierungsphase sind auch eigene Neubauprojekte … denkbar", "source": "DW & Co. enteignen, AöR-Konzept", "tag": "V"},
                    {"side": "IMK Policy Brief 225", "text": "Neubau in großem Stil ist hier der einzige Weg", "source": "IMK Policy Brief 225, 2026", "tag": "V"},
                    {"side": "DIW aktuell 126", "text": "schafft keine zusätzliche Wohnung", "source": SRC_DIW126, "tag": "V"},
                    {"side": "Sondervotum Expertenkommission", "text": "nicht belegt und eher unplausibel", "source": SRC_EXPERTENKOMMISSION, "tag": "V"},
                ],
            },
        },
        "secondary_items": {
            "pestel_deficit": n(58000, "Wohnungen", "2026-08", "Berlin", "Pestel Bau-Monitor 2026 (für BDB)", "S"),
            "bulwiengesa_office_conversion": n(30000, "Wohnungen", "2025", "Berlin", "bulwiengesa/Berlin Hyp Kurzstudie 2025", "S"),
            "campaign_vacancy_threshold": n([10, 20], "%", "2023-2024", "Berlin", "docs/research/sonnetB_enteignen_supply.md (taz.de/verfassungsblog.de, unverifiziert)", "S"),
            "vonovia_halt": {
                "text": "Vonovia-CEO Luka Mucic stoppt laut Presseberichten neue Berliner Bauprojekte nach Fertigstellung der laufenden.",
                "source": "docs/research/sonnet2_transfers_allocation.md (boerse-express.com, Nov 2026)",
                "tag": "S",
                "ref_date": "2026-11",
                "spatial_unit": "Berlin",
            },
        },
        "bezirk_tables": {
            "headline_gap": {
                "unit": "Wohnungen", "tag": "I",
                "source": "docs/research/stage3a_gap_report.md §7 (Definition ii: census-anchored "
                           "Bevölkerungswachstum 9.5.2011-31.12.2025 ÷ Mikrozensus-Haushaltsgröße "
                           "2024 je Bezirk, minus Fertigstellungen 2012-2025)",
                "ref_date": "2011-05-09/2025-12-31",
                "values": {
                    "Mitte": 3800, "Friedrichshain-Kreuzberg": -4500, "Pankow": 5200,
                    "Charlottenburg-Wilmersdorf": 7100, "Spandau": 6000, "Steglitz-Zehlendorf": 1000,
                    "Tempelhof-Schöneberg": 2800, "Neukölln": -1700, "Treptow-Köpenick": -1800,
                    "Marzahn-Hellersdorf": 3500, "Lichtenberg": 6800, "Reinickendorf": 2700,
                    "Berlin": 32000,
                },
                "sensitivity_range_berlin": {"floor": 16000, "ceiling": 44000},
            },
        },
    }

    return data


def main() -> None:
    data = build()
    out = PROCESSED / "levers.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
