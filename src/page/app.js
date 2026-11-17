/* Shared helpers for die-luecke.html. Plain ES2020, globals only (no modules).
   Exposes window.DL = {fmt, tagBadge, tooltip, waffle, lineChart, smallMultiples, KINDS}. */
(function () {
  "use strict";
  const NF = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 1 });

  /** fmt(n, digits?) -> German formatted number ("1.000", "1,8"). null/NaN -> "–". */
  function fmt(n, digits) {
    if (n === null || n === undefined || Number.isNaN(+n)) return "–";
    if (digits !== undefined) return new Intl.NumberFormat("de-DE", { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(n);
    return NF.format(n);
  }

  const TAG_TITLES = { V: "verifiziert (Quelle geprüft)", S: "Schätzung", I: "Indiz / unbestätigt" };
  /** tagBadge(tag) -> HTML string. V is unobtrusive, S and I visibly marked. */
  function tagBadge(tag) {
    if (!tag) return "";
    const t = String(tag).toUpperCase();
    return `<span class="tag tag-${t}" title="${TAG_TITLES[t] || t}">${t}</span>`;
  }

  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function ttHtml(d) {
    const val = typeof d.value === "number" ? fmt(d.value) : esc(d.value);
    return `<div class="tt-value">${val}${d.unit ? " " + esc(d.unit) : ""}${tagBadge(d.tag)}</div>` +
      (d.label ? `<div>${esc(d.label)}</div>` : "") +
      `<div class="tt-meta">${[d.ref_date, d.spatial_unit].filter(Boolean).map(esc).join(" · ")}</div>` +
      (d.source ? `<div class="tt-meta">Quelle: ${esc(d.source)}</div>` : "");
  }
  function showTip(d, x, y) {
    const tip = document.getElementById("tooltip");
    tip.innerHTML = ttHtml(d);
    tip.hidden = false;
    const r = tip.getBoundingClientRect();
    tip.style.left = Math.max(8, Math.min(x + 12, innerWidth - r.width - 8)) + "px";
    tip.style.top = Math.max(8, Math.min(y + 12, innerHeight - r.height - 8)) + "px";
  }
  function hideTip() { document.getElementById("tooltip").hidden = true; }

  /** tooltip(el, info) -- info: {value, unit, ref_date, spatial_unit, source, tag, label?} or a function(event)->info.
      Hover, focus and tap all work. Returns el. */
  function tooltip(el, info) {
    const get = (ev) => (typeof info === "function" ? info(ev) : info);
    el.addEventListener("pointermove", (ev) => showTip(get(ev), ev.clientX, ev.clientY));
    el.addEventListener("pointerleave", hideTip);
    el.addEventListener("focus", () => { const r = el.getBoundingClientRect(); showTip(get(null), r.left, r.bottom); });
    el.addEventListener("blur", hideTip);
    return el;
  }
  document.addEventListener("pointerdown", (ev) => { if (!ev.target.closest("[data-tip]")) hideTip(); });

  const KINDS = ["stock", "built", "owner", "freed", "permit"];

  /** waffle(container, {squares:[{n, kind, info?}], outlines:[{n, label, strength:'strong'|'weak'}], perSquare=1000, cols=10, size?})
      kinds: stock | built | owner | freed | permit. n is in dwellings; squares = round(n/perSquare).
      Outlines are drawn as a rectangle-ish contour around the first ceil(n/perSquare) cells (reading order).
      Returns {svg, cells, update(newSquares)}. */
  function waffle(container, opts) {
    const o = Object.assign({ squares: [], outlines: [], perSquare: 1000, cols: 10 }, opts);
    const root = d3.select(container);
    root.selectAll("*").remove();
    const width = Math.min(container.clientWidth || 320, 480);
    const gap = 2;
    const size = o.size || Math.floor((width - gap * (o.cols - 1)) / o.cols);
    const step = size + gap;

    function expand(sq) {
      const cells = [];
      sq.forEach((s) => {
        const k = Math.round(s.n / o.perSquare);
        for (let i = 0; i < k; i++) cells.push({ kind: s.kind, info: s.info, n: s.n });
      });
      return cells;
    }
    let cells = expand(o.squares);
    const maxCells = Math.max(cells.length, ...o.outlines.map((l) => Math.ceil(l.n / o.perSquare)), 1);
    const rows = Math.ceil(maxCells / o.cols);
    const svg = root.append("svg")
      .attr("viewBox", `0 0 ${o.cols * step} ${rows * step + 4}`)
      .attr("width", "100%").attr("role", "img")
      .attr("aria-label", `Waffeldiagramm, 1 Quadrat = ${fmt(o.perSquare)} Wohnungen`);
    const g = svg.append("g").attr("transform", "translate(1,1)");
    const xy = (i) => [(i % o.cols) * step, Math.floor(i / o.cols) * step];

    function draw(cs, animate) {
      const sel = g.selectAll("rect.cell").data(cs);
      sel.exit().transition().duration(animate ? 250 : 0).attr("opacity", 0).remove();
      const entered = sel.enter().append("rect").attr("class", "cell").attr("rx", 2)
        .attr("width", size - 1).attr("height", size - 1).attr("data-tip", "")
        .attr("x", (d, i) => xy(i)[0]).attr("y", (d, i) => xy(i)[1])
        .attr("opacity", animate ? 0 : 1);
      const all = entered.merge(sel).attr("class", (d) => `cell m-${d.kind}`);
      (animate ? all.transition().duration(250) : all)
        .attr("x", (d, i) => xy(i)[0]).attr("y", (d, i) => xy(i)[1]).attr("opacity", 1);
      all.each(function (d) { if (d.info && !this._tt) { this._tt = 1; tooltip(this, () => d3.select(this).datum().info); } });
    }
    draw(cells, false);

    // track the tallest extent across all outlines so later (shorter) outlines
    // never shrink the viewBox below an earlier (taller) one's label/contour.
    let viewH = rows * step;
    o.outlines.forEach((l) => {
      const k = Math.ceil(l.n / o.perSquare);
      const full = Math.floor(k / o.cols), rem = k % o.cols, W = o.cols * step - gap, h = step;
      // contour: full rows block plus partial last row
      let p = `M0,0H${W}V${full * h - (full ? gap : 0)}`;
      if (rem) p += `H${rem * step - gap}V${(full + 1) * h - gap}H0Z`; else p += `H0Z`;
      g.append("path").attr("class", `waffle-outline ${l.strength === "weak" ? "weak" : ""}`).attr("d", p).attr("transform", "translate(-.5,-.5)");
      if (l.label) {
        g.append("text").attr("class", "waffle-label").attr("text-anchor", "end")
          .attr("x", W).attr("y", (full + (rem ? 1 : 0)) * h + 10).text(l.label);
        viewH = Math.max(viewH, (full + (rem ? 1 : 0)) * h + 14);
      }
    });
    svg.attr("viewBox", `0 0 ${o.cols * step} ${viewH}`);
    return { svg: svg.node(), cells, update(sq) { cells = expand(sq); draw(cells, true); } };
  }

  /** lineChart(container, series, opts)
      series: [{key, label, color (CSS var or hex), values:[{x:Number(year), y:Number, info?}]}] (two lines expected)
      opts: {height=220, yLabel, fillGap:[keyA,keyB] (shade where A>B), gapLabel, okLabel='Bau hat Schritt gehalten', estimatedFrom?:year}
      Returns svg node. Crosshair tooltip shows all series at the hovered year. */
  function lineChart(container, series, opts) {
    const o = Object.assign({ height: 220, okLabel: "Bau hat Schritt gehalten" }, opts);
    const root = d3.select(container); root.selectAll("*").remove();
    const width = Math.max(container.clientWidth || 320, 260);
    const m = { t: 12, r: 12, b: 24, l: 44 };
    const xs = series.flatMap((s) => s.values.map((v) => v.x));
    const ys = series.flatMap((s) => s.values.map((v) => v.y));
    const x = d3.scaleLinear().domain(d3.extent(xs)).range([m.l, width - m.r]);
    const y = d3.scaleLinear().domain([Math.min(0, d3.min(ys)), d3.max(ys) || 1]).nice().range([o.height - m.b, m.t]);
    const svg = root.append("svg").attr("viewBox", `0 0 ${width} ${o.height}`).attr("width", "100%");
    svg.append("g").attr("class", "grid").attr("transform", `translate(${m.l},0)`)
      .call(d3.axisLeft(y).ticks(4).tickSize(-(width - m.l - m.r)).tickFormat("")).select(".domain").remove();
    svg.append("g").attr("class", "axis").attr("transform", `translate(0,${o.height - m.b})`)
      .call(d3.axisBottom(x).ticks(Math.min(6, xs.length)).tickFormat(d3.format("d")));
    svg.append("g").attr("class", "axis").attr("transform", `translate(${m.l},0)`)
      .call(d3.axisLeft(y).ticks(4).tickFormat((d) => fmt(d))).select(".domain").remove();

    if (o.fillGap) {
      const [a, b] = o.fillGap.map((k) => series.find((s) => s.key === k));
      if (a && b) {
        const bm = new Map(b.values.map((v) => [v.x, v.y]));
        const pts = a.values.filter((v) => bm.has(v.x)).map((v) => ({ x: v.x, a: v.y, b: bm.get(v.x) }));
        svg.append("path").attr("class", "gap-area").attr("fill", a.color)
          .attr("d", d3.area().x((d) => x(d.x)).y0((d) => y(d.b)).y1((d) => y(Math.max(d.a, d.b)))(pts));
        const last = pts[pts.length - 1];
        if (last) svg.append("text").attr("class", "chart-label").attr("x", width - m.r).attr("y", m.t + 10)
          .attr("text-anchor", "end").text(last.a > last.b ? (o.gapLabel || "") : o.okLabel);
      }
    }
    const line = d3.line().x((d) => x(d.x)).y((d) => y(d.y));
    series.forEach((s) => {
      svg.append("path").attr("class", "line").attr("stroke", s.color).attr("d", line(s.values));
      const l = s.values[s.values.length - 1];
      if (l) svg.append("circle").attr("cx", x(l.x)).attr("cy", y(l.y)).attr("r", 3.5).attr("fill", s.color);
    });
    const cross = svg.append("line").attr("stroke", "var(--ink-3)").attr("y1", m.t).attr("y2", o.height - m.b).attr("visibility", "hidden");
    const hit = svg.append("rect").attr("x", m.l).attr("y", 0).attr("width", width - m.l - m.r).attr("height", o.height)
      .attr("fill", "transparent").attr("data-tip", "").node();
    tooltip(hit, (ev) => {
      if (!ev) return { value: "" };
      const pt = d3.pointer(ev, svg.node());
      const yr = Math.round(x.invert(pt[0] * (width / svg.node().getBoundingClientRect().width)));
      cross.attr("x1", x(yr)).attr("x2", x(yr)).attr("visibility", "visible");
      const rows = series.map((s) => { const v = s.values.find((d) => d.x === yr); return `${s.label}: ${v ? fmt(v.y) : "–"}`; });
      const first = series[0].values.find((d) => d.x === yr);
      return Object.assign({ value: yr, label: rows.join(" · ") }, first && first.info);
    });
    hit.addEventListener("pointerleave", () => cross.attr("visibility", "hidden"));
    return svg.node();
  }

  /** smallMultiples(container, data, opts)
      data: [{id, title, series:[...same as lineChart]}]; opts passed to lineChart (height default 120), shared y domain if opts.sharedY.
      Returns array of svg nodes. */
  function smallMultiples(container, data, opts) {
    const o = Object.assign({ height: 120 }, opts);
    const root = d3.select(container); root.selectAll("*").remove();
    const grid = root.append("div").attr("class", "sm-grid");
    return data.map((d) => {
      const cell = grid.append("div").attr("class", "sm-cell");
      cell.append("h3").text(d.title);
      return lineChart(cell.append("div").node(), d.series, o);
    });
  }

  // theme toggle: cycles explicit light/dark on the root element; system default when untouched
  function initTheme() {
    const btn = document.getElementById("theme-toggle");
    if (!btn) return;
    const isDark = () => {
      const t = document.documentElement.dataset.theme;
      return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    };
    const label = () => { btn.textContent = isDark() ? "Hell" : "Dunkel"; };
    btn.addEventListener("click", () => {
      document.documentElement.dataset.theme = isDark() ? "light" : "dark";
      try { localStorage.setItem("dl-theme", document.documentElement.dataset.theme); } catch (e) {}
      label();
    });
    try { const s = localStorage.getItem("dl-theme"); if (s) document.documentElement.dataset.theme = s; } catch (e) {}
    label();
  }

  window.DL = { fmt, tagBadge, tooltip, waffle, lineChart, smallMultiples, KINDS };
  document.addEventListener("DOMContentLoaded", initTheme);
})();
