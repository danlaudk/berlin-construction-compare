// Part B (Teil 2: Die Hebel). Waffle + lever cards + Vergesellschaften panel.
// Plain ES2020, globals only. Reads window.DATA.levers.partB and window.DL.
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    const root = document.getElementById("part-b-root");
    if (!root) return;
    const DL = window.DL;
    const DATA = window.DATA || {};
    const pb = (DATA.levers && DATA.levers.partB) || {};
    if (!pb.levers) { root.innerHTML = '<p class="placeholder">Keine Hebel-Daten.</p>'; return; }
    const L = pb.levers;
    const V = L.vergesellschaften || {};
    const FALLBACK_NEED = 137000;

    // ---- layout scaffold --------------------------------------------------
    root.innerHTML = `
      <div class="pb-waffle-wrap">
        <div id="pb-waffle" class="pb-waffle" aria-live="polite"></div>
        <p class="pb-totals">
          Gezogen: <strong id="pb-total">0 Felder</strong>
          gegen Bedarf <span id="pb-outline-need">–</span> und Senats-Ziel <span id="pb-outline-senate">–</span>.
        </p>
        <p class="pb-note">Nur volle (durchgezogene) Felder zählen gegen die Umrisse. Umgefärbte, schraffierte und gepunktete Felder bewegen den Umriss nicht.</p>
      </div>
      <div id="pb-cards" class="pb-cards"></div>
      <section id="pb-verg" class="pb-panel" aria-labelledby="pb-verg-h">
        <h3 id="pb-verg-h">Vergesellschaften</h3>
      </section>
      <section id="pb-secondary" class="pb-secondary" aria-label="Weitere, unsichere Zahlen"></section>
    `;

    // ---- state --------------------------------------------------------
    const state = {
      need: (window.DL && window.DL.need) || FALLBACK_NEED,
      pulled: {},            // key -> true/false for simple levers
      neuRate: "tempo_2025", // tempo_2025 | tempo_2019 | lwu
      neuYears: 1,           // 1 | 5 | 10
      leerstandMode: "market_active", // market_active | ceiling
      kostenT: 0,            // 0..1 slider position between compensation low/high -> DIW low/high
    };

    window.addEventListener("dl:need", (e) => {
      if (e && e.detail && typeof e.detail.total === "number") { state.need = e.detail.total; renderAll(); }
    });

    function v(x) { return x && typeof x === "object" && "value" in x ? x.value : x; }
    function info(x, extra) {
      if (!x || typeof x !== "object") return undefined;
      return Object.assign({ value: x.value, unit: x.unit, ref_date: x.ref_date, spatial_unit: x.spatial_unit, source: x.source, tag: x.tag }, extra);
    }

    // ---- lever definitions ---------------------------------------------
    // Each returns { squares: [{n, kind, info}], counted: dwellings-that-count-to-outline, totalAll: dwellings pulled }
    function neuBauenSquares() {
      const rate = L.neu_bauen[state.neuRate];
      const n = v(rate) * state.neuYears * 1000;
      return [{ n, kind: "built", info: info(rate, { label: `Neu bauen × ${state.neuYears} Jahr(e)` }) }];
    }
    function ueberhangSquares() {
      const f = L.ueberhang.felder;
      return [{ n: v(f) * 1000, kind: "permit", info: info(f, { label: "Überhang (genehmigt, nicht gebaut)" }) }];
    }
    function leerstandSquares() {
      const f = L.leerstand[state.leerstandMode];
      return [{ n: v(f) * 1000, kind: "freed", info: info(f, { label: "Leerstand aktivieren" }) }];
    }
    function ferienwohnungenSquares() {
      const f = L.ferienwohnungen.active;
      return [{ n: v(f) * 1000, kind: "freed", info: info(f, { label: "Ferienwohnungen zurückholen" }) }];
    }
    function zweckentfremdungSquares() {
      const f = L.zweckentfremdung_gesamt.felder;
      return [{ n: v(f) * 1000, kind: "freed", info: info(f, { label: "Zweckentfremdung gesamt" }) }];
    }
    function aufstockenSquares() {
      const s = L.aufstocken_umnutzen.supermaerkte, b = L.aufstocken_umnutzen.buero;
      const sMid = (v(s)[0] + v(s)[1]) / 2;
      return [
        { n: sMid * 1000, kind: "built", info: info(s, { label: "Aufstocken Supermärkte (Mittelwert)" }) },
        { n: v(b) * 1000, kind: "built", info: info(b, { label: "Büro-Umnutzung" }) },
      ];
    }
    function sozialbindungenSquares() {
      const f = L.sozialbindungen.felder; // -46
      return [{ n: Math.abs(v(f)) * 1000, kind: "reverse", info: info(f, { label: "Sozialbindungen laufen aus (recolour reverse)" }), reverse: true }];
    }
    function vergesellschaftenSquares() {
      const u = V.umfang && V.umfang.value;
      return [{ n: v(u) * 1000, kind: "owner", info: info(u, { label: "Vergesellschaften: Umfang" }) }];
    }

    const LEVER_ORDER = [
      { key: "leerstand", title: "Leerstand aktivieren", squares: leerstandSquares, counts: false },
      { key: "ferienwohnungen", title: "Ferienwohnungen", squares: ferienwohnungenSquares, counts: false },
      { key: "zweckentfremdung_gesamt", title: "Zweckentfremdung gesamt", squares: zweckentfremdungSquares, counts: false },
      { key: "vergesellschaften", title: "Vergesellschaften", squares: vergesellschaftenSquares, counts: false, isVerg: true },
      { key: "sozialbindungen", title: "Sozialbindungen", squares: sozialbindungenSquares, counts: false, reverse: true },
      { key: "aufstocken_umnutzen", title: "Aufstocken / umnutzen", squares: aufstockenSquares, counts: true },
      { key: "ueberhang", title: "Überhang fertigstellen", squares: ueberhangSquares, counts: false },
      { key: "neu_bauen", title: "Neu bauen", squares: neuBauenSquares, counts: true },
    ];

    // ---- waffle -----------------------------------------------------------
    let waffleHandle = null;
    const waffleEl = document.getElementById("pb-waffle");

    function buildSquares() {
      const stockTotal = v(pb.stock_squares) * 1000;
      let recolourOwner = 0, recolourFreed = 0, recolourReverse = 0, built = 0, permit = 0;
      let counted = 0, allPulled = 0;
      const extra = []; // built + permit cells, appended beyond stock
      const recolour = []; // owner + freed + reverse cells, drawn from within stock

      LEVER_ORDER.forEach((lv) => {
        if (!state.pulled[lv.key]) return;
        const sqs = lv.squares();
        sqs.forEach((s) => {
          allPulled += lv.reverse ? -s.n : s.n;
          if (s.kind === "built") { built += s.n; counted += s.n; extra.push(s); }
          else if (s.kind === "permit") { permit += s.n; extra.push(s); }
          else if (s.kind === "owner") { recolourOwner += s.n; recolour.push(s); }
          else if (s.kind === "freed") { recolourFreed += s.n; recolour.push(s); }
          else if (s.kind === "reverse") { recolourReverse += s.n; recolour.push(s); }
        });
      });

      const recolourTotal = Math.min(recolourOwner + recolourFreed + recolourReverse, stockTotal);
      const stockRemain = Math.max(stockTotal - recolourTotal, 0);
      const squares = [
        ...recolour,
        { n: stockRemain, kind: "stock" },
        ...extra,
      ];
      return { squares, counted, allPulled, freedN: recolourFreed, ownerN: recolourOwner, reverseN: recolourReverse, permitN: permit };
    }

    function outlineSquares() {
      return [
        { n: Math.max(state.need, 0), label: `Bedarf: ${DL.fmt(Math.round(state.need))}`, strength: "strong" },
        { n: v(pb.senate_need), label: `Senat: ${DL.fmt(v(pb.senate_need))}`, strength: "weak" },
      ];
    }

    function waffleCols() {
      const w = waffleEl.clientWidth || 320;
      return Math.max(20, Math.floor(w / 9));
    }

    function renderWaffle(forceNewLayout) {
      const { squares, counted, freedN, ownerN, reverseN, permitN } = buildSquares();
      const cols = waffleCols();
      if (!waffleHandle || forceNewLayout || waffleHandle.cols !== cols) {
        waffleHandle = DL.waffle(waffleEl, { squares, outlines: outlineSquares(), perSquare: 1000, cols });
        waffleHandle.cols = cols;
      } else {
        waffleHandle.update(squares);
      }
      {
        const k = (x) => DL.fmt(Math.round(x / 1000));
        const parts = [];
        if (freedN) parts.push(`${k(freedN)} zurückgeholt`);
        if (ownerN) parts.push(`${k(ownerN)} umgefärbt`);
        if (reverseN) parts.push(`${k(reverseN)} Bindungen laufen aus`);
        if (permitN) parts.push(`${k(permitN)} genehmigt`);
        document.getElementById("pb-total").textContent = `${k(counted)} volle Felder` + (parts.length ? ` (dazu ${parts.join(", ")})` : "");
      }
      document.getElementById("pb-outline-need").textContent = `${DL.fmt(Math.round(state.need / 1000))} Felder (Bedarf)`;
      document.getElementById("pb-outline-senate").textContent = `${DL.fmt(Math.round(v(pb.senate_need) / 1000))} Felder (Senat)`;
    }

    // Redraw the waffle (new column count) on resize, debounced.
    let resizeTimer = null;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => renderWaffle(true), 150);
    });

    // ---- lever cards --------------------------------------------------
    const cardsEl = document.getElementById("pb-cards");

    function feldText(lv) {
      switch (lv.key) {
        case "neu_bauen": {
          const rate = L.neu_bauen[state.neuRate];
          return `${DL.fmt(v(rate) * state.neuYears, 1)} Tsd. Wohnungen (${state.neuYears} Jahr${state.neuYears > 1 ? "e" : ""} × ${DL.fmt(v(rate), 1)} Tsd./Jahr)`;
        }
        case "ueberhang":
          return `${DL.fmt(v(L.ueberhang.felder), 1)} Tsd. Wohnungen genehmigt, nicht gebaut`;
        case "leerstand":
          return `${DL.fmt(v(L.leerstand[state.leerstandMode]), 1)} Tsd. Wohnungen`;
        case "ferienwohnungen":
          return `${DL.fmt(v(L.ferienwohnungen.active), 1)} Tsd. aktive Inserate`;
        case "zweckentfremdung_gesamt":
          return `${DL.fmt(v(L.zweckentfremdung_gesamt.felder), 1)} Tsd. Wohnungen seit 2014 zurückgeführt`;
        case "aufstocken_umnutzen": {
          const s = v(L.aufstocken_umnutzen.supermaerkte), b = v(L.aufstocken_umnutzen.buero);
          return `${DL.fmt(s[0])}–${DL.fmt(s[1])} Tsd. (Supermärkte) + ~${DL.fmt(b)} Tsd. (Büro)`;
        }
        case "sozialbindungen":
          return `${DL.fmt(v(L.sozialbindungen.felder))} Tsd. Wohnungen bis 2034`;
        case "vergesellschaften":
          return `${DL.fmt(v(V.umfang.value))} Tsd. Wohnungen, neue Wohnungen: 0`;
        default: return "";
      }
    }

    function tempoText(lv) {
      const F = L.ferienwohnungen, Z = L.zweckentfremdung_gesamt, U = L.ueberhang;
      switch (lv.key) {
        case "neu_bauen": return `${DL.fmt(v(L.neu_bauen.tempo_2025), 1)} Tsd./Jahr (2025), ${DL.fmt(v(L.neu_bauen.tempo_2019), 1)} Tsd./Jahr (2019), LWU ${DL.fmt(v(L.neu_bauen.lwu), 1)} Tsd./Jahr`;
        case "ueberhang": return `einmalig; ${DL.fmt(v(U.unter_dach), 1)} unter Dach, ${DL.fmt(v(U.rohbau), 1)} Rohbau, ${DL.fmt(v(U.nicht_begonnen), 1)} nicht begonnen (Tsd., 31.12.2025)`;
        case "leerstand": return "kein Tempo gemessen; marktaktiver Leerstand 0,3 % (2025)";
        case "ferienwohnungen": return `≈ ${DL.fmt(v(F.per_year), 1)} Tsd./Jahr zurückgeführt (${DL.fmt(v(F.returned_since_2014), 1)} Tsd. seit 2014)`;
        case "zweckentfremdung_gesamt": return `≈ ${DL.fmt(v(Z.felder) / 11.5, 1)} Tsd./Jahr (${DL.fmt(v(Z.felder), 1)} Tsd. 2014 – Mitte 2025)`;
        case "aufstocken_umnutzen": return "Potenzialschätzung, keine Bautätigkeit gemessen";
        case "sozialbindungen": return "≈ 4 Tsd./Jahr laufen aus, bis 2034";
        case "vergesellschaften": return "einmalig, Stichtag 31.12.2021";
        default: return "";
      }
    }

    function werZahltText(key) {
      const map = {
        neu_bauen: L.neu_bauen.wer_zahlt,
        ueberhang: "Bauherr (privat/LWU)",
        leerstand: "Eigentümer",
        ferienwohnungen: "Vermieter / Plattform",
        zweckentfremdung_gesamt: "Vermieter, Bußgeld bei Verstoß",
        aufstocken_umnutzen: "Eigentümer / Investor",
        sozialbindungen: "entfällt (läuft aus)",
        vergesellschaften: "Land Berlin (Entschädigung, siehe Panel)",
      };
      return map[key] || "–";
    }

    function quelleOf(key) {
      const map = {
        neu_bauen: L.neu_bauen.quelle, ueberhang: L.ueberhang.quelle, leerstand: L.leerstand.quelle,
        ferienwohnungen: L.ferienwohnungen.quelle, zweckentfremdung_gesamt: L.zweckentfremdung_gesamt.quelle,
        aufstocken_umnutzen: L.aufstocken_umnutzen.quelle, sozialbindungen: L.sozialbindungen.quelle,
        vergesellschaften: (V.umfang && V.umfang.value && V.umfang.value.source) || "",
      };
      return map[key] || "";
    }

    function cardControls(lv) {
      if (lv.key === "neu_bauen") {
        return `
          <div class="pb-chip-row" role="group" aria-label="Zeitraum">
            ${[1, 5, 10].map((y) => `<button type="button" class="pb-chip" data-years="${y}" aria-pressed="${state.neuYears === y}">${y} J.</button>`).join("")}
          </div>
          <div class="pb-chip-row" role="group" aria-label="Rate">
            <button type="button" class="pb-chip" data-rate="tempo_2025" aria-pressed="${state.neuRate === "tempo_2025"}">2025 (11,0/J.)</button>
            <button type="button" class="pb-chip" data-rate="tempo_2019" aria-pressed="${state.neuRate === "tempo_2019"}">2019 (19/J.)</button>
            <button type="button" class="pb-chip" data-rate="lwu" aria-pressed="${state.neuRate === "lwu"}">LWU (4,7/J.)</button>
          </div>`;
      }
      if (lv.key === "leerstand") {
        return `<div class="pb-chip-row" role="group" aria-label="Leerstand-Basis">
          <button type="button" class="pb-chip" data-leerstand="market_active" aria-pressed="${state.leerstandMode === "market_active"}">marktaktiv (5,4)</button>
          <button type="button" class="pb-chip" data-leerstand="ceiling" aria-pressed="${state.leerstandMode === "ceiling"}">Obergrenze (11,8)</button>
        </div>`;
      }
      return "";
    }

    function cardHtml(lv) {
      const tag = lv.key === "vergesellschaften" ? "V" : (lv.key === "aufstocken_umnutzen" ? "S" : "V");
      const pulled = !!state.pulled[lv.key];
      return `
        <article id="lever-${lv.key}" class="pb-card ${lv.reverse ? "pb-card-reverse" : ""}" data-key="${lv.key}">
          <h4>${lv.title} ${DL.tagBadge(tag)}</h4>
          <dl class="pb-fields">
            <div><dt>Felder</dt><dd>${feldText(lv)}</dd></div>
            <div><dt>Tempo</dt><dd>${tempoText(lv)}</dd></div>
            <div><dt>Wer zahlt</dt><dd>${werZahltText(lv.key)}</dd></div>
            <div><dt>Quelle</dt><dd>${quelleOf(lv.key)}</dd></div>
          </dl>
          ${cardControls(lv)}
          <button type="button" class="pb-pull" data-pull data-key="${lv.key}" aria-pressed="${pulled}">${pulled ? "Zurücklegen" : "Ziehen"}</button>
        </article>`;
    }

    function unterkuenfteCardHtml() {
      const f = L.unterkuenfte.felder;
      return `
        <article id="lever-unterkuenfte" class="pb-card pb-card-marker">
          <h4>Unterkünfte ${DL.tagBadge(f.tag)}</h4>
          <dl class="pb-fields">
            <div><dt>Felder</dt><dd>${DL.fmt(v(f))} Tsd. Personen (Bedarfsmarker)</dd></div>
            <div><dt>Tempo</dt><dd>Stand 31.01.2025</dd></div>
            <div><dt>Wer zahlt</dt><dd>Land Berlin</dd></div>
            <div><dt>Quelle</dt><dd>${L.unterkuenfte.quelle}</dd></div>
          </dl>
          <p class="pb-note">${L.unterkuenfte.note} Keine Wohnungen, kein Feld im Waffeldiagramm.</p>
        </article>`;
    }

    function renderCards() {
      cardsEl.innerHTML = LEVER_ORDER.filter((l) => !l.isVerg).map(cardHtml).join("")
        + unterkuenfteCardHtml();

      cardsEl.querySelectorAll("[data-pull]").forEach((btn) => {
        btn.addEventListener("click", () => {
          const key = btn.dataset.key;
          state.pulled[key] = !state.pulled[key];
          renderAll();
        });
      });
      cardsEl.querySelectorAll("[data-years]").forEach((btn) => btn.addEventListener("click", () => {
        state.neuYears = +btn.dataset.years; renderAll();
      }));
      cardsEl.querySelectorAll("[data-rate]").forEach((btn) => btn.addEventListener("click", () => {
        state.neuRate = btn.dataset.rate; renderAll();
      }));
      cardsEl.querySelectorAll("[data-leerstand]").forEach((btn) => btn.addEventListener("click", () => {
        state.leerstandMode = btn.dataset.leerstand; renderAll();
      }));

      // tooltips on the Felder values
      cardsEl.querySelectorAll(".pb-card").forEach((card) => {
        const key = card.dataset.key;
        const lv = LEVER_ORDER.find((l) => l.key === key);
        if (!lv) return;
        const dd = card.querySelector(".pb-fields dd");
        if (dd) { dd.setAttribute("data-tip", ""); DL.tooltip(dd, () => (lv.squares()[0] && lv.squares()[0].info) || { value: "" }); }
      });
    }

    // ---- Vergesellschaften panel ---------------------------------------
    const vergEl = document.getElementById("pb-verg");

    function kostenLerp() {
      const lo = v(V.kosten.diw_annual_low_bn_eur), hi = v(V.kosten.diw_annual_high_bn_eur);
      return lo + (hi - lo) * state.kostenT;
    }

    function renderVerg() {
      const pulled = !!state.pulled.vergesellschaften;
      vergEl.innerHTML = `
        <h3 id="pb-verg-h">Vergesellschaften</h3>
        <div class="pb-verg-grid">
          <section class="pb-verg-field">
            <h4>Umfang ${DL.tagBadge(V.umfang.value.tag)}</h4>
            <p>${V.umfang.text}</p>
            <p class="pb-meta">${DL.fmt(v(V.umfang.share_all_dwellings), 1)} % aller Wohnungen ${DL.tagBadge(V.umfang.share_all_dwellings.tag)},
              ${DL.fmt(v(V.umfang.share_rental_stock), 1)} % des Mietwohnungsbestands ${DL.tagBadge(V.umfang.share_rental_stock.tag)}</p>
            <button type="button" class="pb-pull" data-pull data-key="vergesellschaften" aria-pressed="${pulled}">${pulled ? "Zurücklegen" : "Ziehen"}</button>
          </section>
          <section class="pb-verg-field">
            <h4>Vergabe <span class="pb-axis-note">eigene Achse, nicht Teil der Waffel</span></h4>
            <div id="pb-vergabe-axis" class="pb-vergabe-axis" aria-label="Jährlicher Netto-Zuwachs WBS-Vermietungen"></div>
            <p>${V.vergabe.text}</p>
            <p class="pb-meta">${V.vergabe.lock_in_text}</p>
          </section>
          <section class="pb-verg-field">
            <h4>Miete</h4>
            <p>${V.miete.text}</p>
          </section>
          <section class="pb-verg-field">
            <h4>Kosten</h4>
            <p>${V.kosten.text}</p>
            <label class="pb-slider-label" for="pb-kosten-slider">Jährliche Belastung Landeshaushalt (DIW-Spanne)</label>
            <input type="range" id="pb-kosten-slider" min="0" max="100" value="${Math.round(state.kostenT * 100)}">
            <output id="pb-kosten-out">${DL.fmt(kostenLerp(), 1)} Mrd. €/Jahr</output>
          </section>
          <section class="pb-verg-field">
            <h4>Bauen?</h4>
            <button type="button" class="pb-chip" id="pb-bauen-toggle" aria-expanded="false">Zitate anzeigen</button>
            <div id="pb-bauen-quotes" hidden>
              ${V.bauen.quotes.map((q) => `<p class="pb-quote"><strong>${q.side}:</strong> „${q.text}" ${DL.tagBadge(q.tag)}</p>`).join("")}
              <p class="pb-meta">${V.bauen.risk_band.text}</p>
            </div>
          </section>
          <section class="pb-verg-field">
            <h4>Leerstand bei den Konzernen</h4>
            <p>${V.vacancy_card.text}</p>
          </section>
          <section class="pb-verg-field pb-verg-quotes">
            <h4>Stimmen</h4>
            ${V.quotes_both_sides.map((q) => `<p class="pb-quote"><strong>${q.side}:</strong> „${q.text}" ${DL.tagBadge(q.tag)}</p>`).join("")}
          </section>
        </div>`;

      vergEl.querySelectorAll("[data-pull]").forEach((btn) => btn.addEventListener("click", () => {
        state.pulled.vergesellschaften = !state.pulled.vergesellschaften; renderAll();
      }));
      const slider = vergEl.querySelector("#pb-kosten-slider");
      slider.addEventListener("input", () => {
        state.kostenT = +slider.value / 100;
        vergEl.querySelector("#pb-kosten-out").textContent = `${DL.fmt(kostenLerp(), 1)} Mrd. €/Jahr`;
      });
      const bauenBtn = vergEl.querySelector("#pb-bauen-toggle");
      bauenBtn.addEventListener("click", () => {
        const box = vergEl.querySelector("#pb-bauen-quotes");
        const open = box.hidden;
        box.hidden = !open;
        bauenBtn.setAttribute("aria-expanded", String(open));
      });

      renderVergabeAxis();
    }

    function renderVergabeAxis() {
      const el = document.getElementById("pb-vergabe-axis");
      if (!el || !window.d3) return;
      el.innerHTML = "";
      const lo = v(V.vergabe.net_flow_low), hi = v(V.vergabe.net_flow_high), campaign = v(V.vergabe.campaign_gross_quote);
      const width = Math.max(el.clientWidth || 300, 240), height = 56, m = { l: 8, r: 8 };
      const max = Math.ceil(Math.max(campaign, hi) * 1.1 / 1000) * 1000;
      const x = d3.scaleLinear().domain([0, max]).range([m.l, width - m.r]);
      const svg = d3.select(el).append("svg").attr("viewBox", `0 0 ${width} ${height}`).attr("width", "100%");
      svg.append("line").attr("x1", m.l).attr("x2", width - m.r).attr("y1", 40).attr("y2", 40).attr("stroke", "var(--rule)");
      svg.append("rect").attr("x", x(lo)).attr("y", 30).attr("width", x(hi) - x(lo)).attr("height", 10)
        .attr("fill", "var(--k-owner)").attr("rx", 2).attr("data-tip", "");
      DL.tooltip(svg.select("rect").node(), { value: `${DL.fmt(lo)}–${DL.fmt(hi)}`, unit: "Wohnungen/Jahr (netto)", source: V.vergabe.net_flow_low.source, tag: "I" });
      svg.append("line").attr("x1", x(campaign)).attr("x2", x(campaign)).attr("y1", 24).attr("y2", 46).attr("stroke", "var(--ink-3)").attr("stroke-dasharray", "2 2");
      const campaignLabelX = x(campaign);
      const nearRightEdge = campaignLabelX > width - m.r - 44;
      svg.append("text").attr("x", nearRightEdge ? width - m.r : campaignLabelX)
        .attr("y", 18).attr("text-anchor", nearRightEdge ? "end" : "middle")
        .attr("class", "chart-label").text(`Initiative: ${DL.fmt(campaign)}`);
      svg.append("text").attr("x", m.l).attr("y", 54).attr("class", "chart-label").text("0");
      svg.append("text").attr("x", width - m.r).attr("y", 54).attr("text-anchor", "end").attr("class", "chart-label").text(DL.fmt(max));
    }

    // ---- secondary items -------------------------------------------------
    function renderSecondary() {
      const sec = pb.secondary_items || {};
      const el = document.getElementById("pb-secondary");
      const rows = Object.keys(sec).map((k) => {
        const it = sec[k];
        if (it.tag !== "S" && it.tag !== "I") return "";
        const label = it.text || `${Array.isArray(it.value) ? it.value.join("–") : DL.fmt(it.value)} ${it.unit || ""}`;
        return `<li>${DL.tagBadge(it.tag)} ${label} <span class="pb-meta">${it.source || ""}</span></li>`;
      }).filter(Boolean).join("");
      el.innerHTML = rows ? `<h3>Weitere Zahlen, unsicher</h3><ul class="pb-secondary-list">${rows}</ul>` : "";
    }

    function renderAll() {
      renderWaffle();
      renderCards();
      renderVerg();
      renderSecondary();
    }

    renderAll();
  });
})();
