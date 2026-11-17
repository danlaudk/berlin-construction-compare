// Part A (Wohnungsbilanz). Teil 1: zwei Runden, Bezirk-Vergleich, zwei Regler.
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(init);

  function init() {
    var root = document.getElementById("part-a-root");
    if (!root) return;
    var DATA = window.DATA || { panel: [], levers: {} };
    var L = DATA.levers || {};
    var fmt = window.DL.fmt, tagBadge = window.DL.tagBadge, tooltip = window.DL.tooltip;

    var UEBERNOMMEN_REVEAL =
      "Rund 20.000 Wohnungen kauften die landeseigenen Gesellschaften 2021–2025. " +
      "Darin wohnten schon Menschen. Zusätzlich untergebracht: praktisch niemand. " +
      "Die Felder färben sich um, keins kommt dazu.";
    var UEBERNOMMEN_HINT = "Wohnungen, die den Besitzer wechselten.";

    root.innerHTML =
      '<div class="dl-rounds">' +
      '<section class="dl-round" id="round1"></section>' +
      '<section class="dl-round" id="round2"></section>' +
      "</div>" +
      '<section class="dl-bezirk" id="bezirk-section"></section>' +
      '<section class="dl-dials" id="dials-section"></section>' +
      '<section class="dl-caveats" id="part-a-caveats"></section>';

    buildRound({
      container: document.getElementById("round1"),
      idPrefix: "r1",
      roundKey: "roundA",
      round: L.roundA,
      step: 10000,
      withIdentity: true,
    });
    buildRound({
      container: document.getElementById("round2"),
      idPrefix: "r2",
      roundKey: "roundB",
      round: L.roundB,
      step: 10000,
      withIdentity: false,
    });

    buildBezirkSection(document.getElementById("bezirk-section"), DATA);
    buildDials(document.getElementById("dials-section"), L.dials || {});
    buildCaveats(document.getElementById("part-a-caveats"), (L.partB && L.partB.caveats) || []);

    // ---- Round builder (shared mechanic for Round 1 and Round 2) ----
    function buildRound(cfg) {
      var c = cfg.container;
      if (!c || !cfg.round) return;
      var round = cfg.round;
      var budget = round.arrivals.value;
      var taps = buildTapList(cfg.roundKey, round);
      var alloc = {}; // key -> allocated amount (guess, in people)
      taps.forEach(function (t) { alloc[t.key] = 0; });

      c.innerHTML =
        '<h3>' + esc(round.label) + "</h3>" +
        '<p class="dl-frame">' + esc(round.frame_text || "") + "</p>" +
        '<p class="dl-budget">Zu verteilen: <strong>' + fmt(budget) + "</strong> " + esc(round.arrivals.unit) +
        tagBadge(round.arrivals.tag) + ' <span id="' + cfg.idPrefix + '-remaining"></span></p>' +
        '<div class="dl-taps" id="' + cfg.idPrefix + '-taps"></div>' +
        '<button type="button" class="dl-commit" id="' + cfg.idPrefix + '-commit" disabled>Festlegen</button>' +
        '<div class="dl-ledger" id="' + cfg.idPrefix + '-ledger" hidden></div>';

      tooltip(c.querySelector(".dl-budget strong"), {
        value: budget, unit: round.arrivals.unit, ref_date: round.arrivals.ref_date,
        spatial_unit: round.arrivals.spatial_unit, source: round.arrivals.source, tag: round.arrivals.tag,
      });

      var tapsRoot = document.getElementById(cfg.idPrefix + "-taps");
      taps.forEach(function (t) {
        var row = document.createElement("div");
        row.className = "dl-tap";
        row.innerHTML =
          '<div class="dl-tap-label">' + esc(t.label) + (t.hint ? '<span class="dl-tap-hint">' + esc(t.hint) + "</span>" : "") + "</div>" +
          '<div class="dl-tap-controls">' +
          '<button type="button" class="dl-step-minus" aria-label="weniger">−</button>' +
          '<input type="number" class="dl-tap-input" step="' + cfg.step + '" value="0" inputmode="numeric">' +
          '<button type="button" class="dl-step-plus" aria-label="mehr">+</button>' +
          "</div>" +
          '<div class="dl-tap-reveal" hidden></div>';
        tapsRoot.appendChild(row);
        var input = row.querySelector(".dl-tap-input");
        var minus = row.querySelector(".dl-step-minus");
        var plus = row.querySelector(".dl-step-plus");
        function setVal(v) {
          alloc[t.key] = v;
          input.value = v;
          updateRemaining();
        }
        minus.addEventListener("click", function () { setVal(alloc[t.key] - cfg.step); });
        plus.addEventListener("click", function () { setVal(alloc[t.key] + cfg.step); });
        input.addEventListener("change", function () {
          var v = parseInt(input.value, 10);
          setVal(Number.isFinite(v) ? v : 0);
        });
        t._row = row;
      });

      var remainingEl = document.getElementById(cfg.idPrefix + "-remaining");
      var commitBtn = document.getElementById(cfg.idPrefix + "-commit");

      function sumAlloc() {
        return taps.reduce(function (s, t) { return s + (alloc[t.key] || 0); }, 0);
      }
      function updateRemaining() {
        var remaining = budget - sumAlloc();
        remainingEl.textContent = "Rest: " + fmt(remaining);
        commitBtn.disabled = remaining !== 0;
      }
      updateRemaining();

      commitBtn.addEventListener("click", function () {
        commitBtn.disabled = true;
        taps.forEach(function (t) { revealTap(t, alloc[t.key]); });
        var ledger = document.getElementById(cfg.idPrefix + "-ledger");
        ledger.hidden = false;
        ledger.innerHTML = cfg.withIdentity ? identityHtml(round.identity) : overlapHtml(round);
      });
    }

    function buildTapList(roundKey, round) {
      if (roundKey === "roundA") {
        return Object.keys(round.taps).map(function (key) {
          var t = Object.assign({ key: key }, round.taps[key]);
          if (key === "uebernommen") { t.hint = UEBERNOMMEN_HINT; t.extraReveal = UEBERNOMMEN_REVEAL; }
          return t;
        });
      }
      // Round 2: synthesize a tap list from the roundB fields.
      var list = [];
      list.push(Object.assign({ key: "stock_change", label: "Neu gebaut / Bestand" }, round.stock_change,
        { note: "+" + fmt(round.stock_change.value) + " Whg. ≈ " + fmt(Math.round(round.stock_change.value * 1.79 / 1000) * 1000) + " Menschen" }));
      list.push(Object.assign({ key: "unterkuenfte_change", label: "In Unterkünften" }, round.unterkuenfte_change,
        { note: "+" + fmt(round.unterkuenfte_change.value) + " Personen" }));
      list.push(Object.assign({ key: "uebernommen", label: "Übernommen", hint: UEBERNOMMEN_HINT, extraReveal: UEBERNOMMEN_REVEAL },
        round.uebernommen.persons,
        { note: "≈" + fmt(round.uebernommen.dwellings.value) + " Whg., 0 Menschen", dwellings: round.uebernommen.dwellings }));
      list.push({ key: "gar_nicht_gekommen", label: "Gar nicht gekommen", value: null, unit: "Personen",
        note: "nicht messbar", tag: "I" });
      return list;
    }

    function revealTap(t, guess) {
      var row = t._row;
      var reveal = row.querySelector(".dl-tap-reveal");
      reveal.hidden = false;
      var guessHtml = '<div class="dl-tap-guess">Ihre Schätzung: ' + fmt(guess) + "</div>";
      var noteHtml = '<div class="dl-tap-note">' + esc(t.note || "") + " " + tagBadge(t.tag) + "</div>";
      var extraHtml = t.extraReveal ? '<div class="dl-tap-extra">' + esc(t.extraReveal) + "</div>" : "";
      reveal.innerHTML = guessHtml + noteHtml + extraHtml;
      if (typeof t.value === "number") {
        tooltip(reveal.querySelector(".dl-tap-note"), {
          value: t.value, unit: t.unit, ref_date: t.ref_date, spatial_unit: t.spatial_unit,
          source: t.source, tag: t.tag, label: t.label,
        });
      }
    }

    function identityHtml(identity) {
      var d = identity.dwellings, ppH = identity.persons_per_household;
      var persons = Math.round(d.value * ppH.value);
      return '<p class="dl-identity"><span class="dl-formula">' + esc(identity.formula) + ' Haushalte</span> × ' +
        fmt(ppH.value, 2) + " = " + fmt(persons) + " Menschen (" + esc(identity.label) + ")" +
        tagBadge(d.tag) + "</p>";
    }

    function overlapHtml(round) {
      var pct = round.overlap_pct;
      return '<p class="dl-overlap">' + esc(round.overlap_caveat) + " (" + fmt(pct.value) + " %" + tagBadge(pct.tag) + ")</p>";
    }

    // ---- Bezirk picker + basis toggle + line chart + vacancy small multiples ----
    function buildBezirkSection(c, DATA) {
      if (!c) return;
      var panel = DATA.panel || [];
      var bezirke = Array.from(new Set(panel.map(function (r) { return r.bezirk; }))).sort();
      // Put "Berlin" first.
      bezirke = bezirke.filter(function (b) { return b !== "Berlin"; });
      bezirke.unshift("Berlin");

      c.innerHTML =
        '<h3>Je Bezirk: Bedarf und Bautätigkeit</h3>' +
        '<div class="dl-controls">' +
        '<label for="bezirk-select">Bezirk</label>' +
        '<select id="bezirk-select"></select>' +
        '<fieldset class="dl-basis-toggle" id="basis-toggle">' +
        '<legend>Bevölkerungsbasis</legend>' +
        '<label><input type="radio" name="basis" value="census" checked> Zensus-basiert</label>' +
        '<label><input type="radio" name="basis" value="register"> Melderegister</label>' +
        "</fieldset>" +
        "</div>" +
        '<div class="chart-wrap" id="bezirk-chart"></div>' +
        '<p class="dl-chart-note" id="bezirk-chart-note"></p>' +
        '<h3>Leerstand je Bezirk, 2011 vs. 2022</h3>' +
        '<div id="vacancy-sm"></div>';

      var select = document.getElementById("bezirk-select");
      bezirke.forEach(function (b) {
        var opt = document.createElement("option");
        opt.value = b; opt.textContent = b === "Berlin" ? "Berlin (gesamt)" : b;
        select.appendChild(opt);
      });

      function rowsFor(b) {
        return panel.filter(function (r) { return r.bezirk === b; }).sort(function (a, c2) { return a.year - c2.year; });
      }

      function render() {
        var b = select.value;
        var basis = (document.querySelector('input[name="basis"]:checked') || {}).value || "census";
        var rows = rowsFor(b);
        if (!rows.length) return;
        var base = rows[0];
        var baseHh = base.hh_size || 1.79;
        var cumCompleted = 0, cumNeed = 0;
        var needSeries = [], builtSeries = [];
        rows.forEach(function (r) {
          cumCompleted += r.completions || 0;
          var pop = basis === "register" ? r.population_register : r.population_census_basis;
          var popBase = basis === "register" ? base.population_register : base.population_census_basis;
          var hh = r.hh_size || baseHh;
          var dwellingsNeed = (pop - popBase) / hh;
          needSeries.push({ x: r.year, y: Math.round(dwellingsNeed), info: {
            value: Math.round(dwellingsNeed), unit: "Wohnungen (Bedarf, kumuliert)", ref_date: String(r.year),
            spatial_unit: b, source: "berlin_panel.csv", tag: r.estimated ? "S" : "V",
          } });
          builtSeries.push({ x: r.year, y: Math.round(cumCompleted), info: {
            value: Math.round(cumCompleted), unit: "Wohnungen (gebaut, kumuliert)", ref_date: String(r.year),
            spatial_unit: b, source: "F II 2 Baufertigstellungen", tag: "V",
          } });
        });
        var series = [
          { key: "need", label: "Bedarf (Bevölkerung ÷ Haushaltsgröße)", color: "var(--k-need)", values: needSeries },
          { key: "built", label: "Gebaut (kumuliert)", color: "var(--k-built)", values: builtSeries },
        ];
        window.DL.lineChart(document.getElementById("bezirk-chart"), series, {
          fillGap: ["need", "built"],
          gapLabel: "Lücke",
          okLabel: "Bau hat Schritt gehalten",
        });

        // 1 square = 1.000 annotation at the 2019 peak.
        var peak2019 = builtSeries.find(function (p) { return p.x === 2019; });
        var noteEl = document.getElementById("bezirk-chart-note");
        if (peak2019 && noteEl) {
          var squares = Math.round(peak2019.y / 1000);
          noteEl.textContent = "2019 kumuliert: " + fmt(squares) + " Felder (1 Feld = 1.000 Wohnungen).";
        } else if (noteEl) {
          noteEl.textContent = "";
        }

        // Vacancy small multiples: 2011 vs 2022 per Bezirk (fixed set, not just the selected one).
        var smData = (bezirke.length ? bezirke : []).filter(function (bb) { return bb !== "Berlin"; }).map(function (bb) {
          var bRows = rowsFor(bb).filter(function (r) { return r.year === 2011 || r.year === 2022; });
          var values = bRows.map(function (r) {
            return { x: r.year, y: +(r.vacancy_rate * 100).toFixed(2), info: {
              value: +(r.vacancy_rate * 100).toFixed(2), unit: "% Leerstand", ref_date: String(r.year),
              spatial_unit: bb, source: "Zensus " + r.year, tag: "V",
            } };
          });
          return { id: bb, title: bb, series: [{ key: "vac", label: "Leerstand %", color: "var(--k-freed)", values: values }] };
        });
        window.DL.smallMultiples(document.getElementById("vacancy-sm"), smData, { height: 100, sharedY: true });
      }

      select.addEventListener("change", render);
      c.querySelectorAll('input[name="basis"]').forEach(function (r) { r.addEventListener("change", render); });
      render();
    }

    // ---- Dials: Reserve + Haushaltsgröße -> bridge total, dispatched as dl:need ----
    function buildDials(c, dials) {
      if (!c || !dials.reserve) return;
      var r = dials.reserve, h = dials.hh_size, bridge = dials.bridge;
      c.innerHTML =
        '<h3>Zwei Regler: wie viel Platz soll Berlin vorhalten?</h3>' +
        '<p class="dl-bridge-text">' + esc(bridge.bridge_text) + "</p>" +
        '<div class="dl-dial">' +
        '<label for="dial-reserve">Reserve: <output id="dial-reserve-out"></output> %</label>' +
        '<input type="range" id="dial-reserve" min="' + r.min + '" max="' + r.max + '" step="0.1" value="' + r.default + '">' +
        "</div>" +
        '<div class="dl-dial">' +
        '<label for="dial-hhsize">Haushaltsgröße: <output id="dial-hhsize-out"></output> Personen/Haushalt</label>' +
        '<input type="range" id="dial-hhsize" min="' + h.min + '" max="' + h.max + '" step="0.01" value="' + h.default + '">' +
        "</div>" +
        '<button type="button" id="dial-reset">Senatswerte</button>' +
        '<dl class="dl-bridge-components">' +
        '<div><dt>Reserve</dt><dd id="bridge-reserve"></dd></div>' +
        '<div><dt>Entlastung</dt><dd id="bridge-relief"></dd></div>' +
        '<div><dt>Ersatz</dt><dd id="bridge-replacement"></dd></div>' +
        '<div class="dl-bridge-total"><dt>Gesamt</dt><dd id="bridge-total"></dd></div>' +
        "</dl>" +
        '<p class="dl-bridge-excludes">Nicht enthalten: ' + esc(bridge.excludes) + "</p>";

      var reserveInput = document.getElementById("dial-reserve");
      var hhInput = document.getElementById("dial-hhsize");
      var reserveOut = document.getElementById("dial-reserve-out");
      var hhOut = document.getElementById("dial-hhsize-out");
      var stock = bridge.stock_2025_for_reserve_calc.value;

      function reserveComponentAt(reservePct) {
        // calibrated so reserve=3% -> 41000, linear in stock*reserve/100
        return Math.round(stock * (reservePct / 100) * (bridge.reserve_component.value / (stock * (r.senate_value.value / 100))));
      }
      function reliefComponentAt(hhSize) {
        // inversely proportional to hh_size, anchored at hh_size=1.77 -> 77000
        return Math.round(bridge.relief_component.value * (h.senate_value.value / hhSize));
      }

      function compute() {
        var reserveVal = parseFloat(reserveInput.value);
        var hhVal = parseFloat(hhInput.value);
        reserveOut.textContent = fmt(reserveVal, 1);
        hhOut.textContent = fmt(hhVal, 2);
        var reserveComp = reserveComponentAt(reserveVal);
        var reliefComp = reliefComponentAt(hhVal);
        var replacementComp = bridge.replacement_component.value;
        var total = reserveComp + reliefComp + replacementComp;
        document.getElementById("bridge-reserve").textContent = fmt(reserveComp) + " Wohnungen";
        document.getElementById("bridge-relief").textContent = fmt(reliefComp) + " Wohnungen";
        document.getElementById("bridge-replacement").textContent = fmt(replacementComp) + " Wohnungen";
        document.getElementById("bridge-total").textContent = fmt(total) + " Wohnungen";
        window.DL.need = total;
        window.dispatchEvent(new CustomEvent("dl:need", { detail: { total: total, reserve: reserveComp, hhSize: reliefComp } }));
      }

      reserveInput.addEventListener("input", compute);
      hhInput.addEventListener("input", compute);
      document.getElementById("dial-reset").addEventListener("click", function () {
        reserveInput.value = r.default; hhInput.value = h.default; compute();
      });
      compute();
    }

    function buildCaveats(c, caveats) {
      if (!c) return;
      c.innerHTML = "<h3>Drei Vorbehalte</h3><ol>" +
        caveats.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ol>";
    }

    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }
  }
})();
