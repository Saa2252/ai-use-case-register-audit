/* Builds the tables on views 2 and 3 from the loaded findings.
   Every value comes from docs/data (S5). Nothing here computes a figure. */

(function () {
  "use strict";

  // Labels are fetched, never restated, for the same reason the emptiness rule
  // is: a second copy drifts. Loaded before the findings render.

  function esc(s) {
    return String(s === undefined || s === null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function el(id) { return document.getElementById(id); }
  function rows(id, html) { var t = el(id); if (t) { t.innerHTML = html; } }
  function n(v) { return typeof v === "number" ? v.toLocaleString("en-US") : esc(v); }

  function drillFigure(selector, band) {
    var node = document.querySelector(selector);
    if (!node) { return; }
    var link = document.createElement("a");
    link.className = "drill";
    link.href = "register.html?band=" + encodeURIComponent(band);
    link.textContent = node.textContent;
    node.textContent = "";
    node.appendChild(link);
  }

  var LABELS = {}, GROUPS = {};
  var REPAINT = [];

  function label(column) {
    return LABELS[column] || column.replace(/_/g, " ");
  }

  // Anything that prints a label registers here, so that when the labels arrive
  // it is drawn again. Without this the first paint shows raw column names and
  // only a later interaction corrects them, which is worse than either.
  function onLabels(fn) {
    REPAINT.push(fn);
    if (Object.keys(LABELS).length) { fn(); }
  }

  (function loadLabels() {
    var holder = document.querySelector("[data-dv]");
    var v = holder ? holder.getAttribute("data-dv") : "";
    fetch("data/field_labels.json" + (v ? "?v=" + v : ""))
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (d) {
        LABELS = (d && d.labels) || {};
        GROUPS = (d && d.group_of) || {};
        REPAINT.forEach(function (fn) { fn(); });
      })
      .catch(function () { LABELS = {}; });
  })();

  document.addEventListener("figures:ready", function (e) {
    var S = e.detail;

    // Figures that name a population lead to that population.
    drillFigure('[data-figure="M4.subset_size"]', "High-impact");
    drillFigure('[data-figure="M4.bands.classification not recorded"]', "__none");
    drillFigure('[data-figure="M4.presumed_band.rows"]', "Presumed High-Impact, but Not High-impact");

    if (S.M1 && el("thresholds")) {
      rows("thresholds", S.M1.candidate_duplicates_not_confirmed.map(function (b) {
        return "<tr><td>" + b.threshold + "</td><td>" + n(b.candidate_pairs) + "</td><td>" +
          n(b.entries_flagged) + "</td><td>" + b.share_of_register + "%</td></tr>";
      }).join(""));
    }

    if (S.M2 && el("mismatches")) {
      var m = S.M2.reconciliation.figures_that_do_not_match;
      rows("mismatches", Object.keys(m).map(function (k) {
        // A figure that could not be reconciled prints as that, not as a
        // number. Publishing nothing here is the finding.
        var observed = (m[k].observed === null || m[k].observed === undefined)
          ? '<span class="unreconciled">could not be reconciled</span>'
          : n(m[k].observed);
        return "<tr><td>" + esc(k) + "</td><td>" + n(m[k].published) + "</td><td>" +
          observed + "</td><td>" + esc(m[k].note || "Both candidate explanations are stated in the provenance document. Neither is chosen.") + "</td></tr>";
      }).join(""));
    }

    if (S.M3 && el("group-one")) {
      el("group-one").innerHTML = S.M3.re_verification_trigger_diagnostic.group_one.triggers
        .map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("");
    }

    // The clearest finding is shown in full. The other five open in place, so
    // every word stays on the page without all six competing for attention.
    if (el("reuse-lead") && S.R1) {
      el("reuse-lead").innerHTML =
        '<div class="finding-lead"><h3>' + esc(S.R1.plain_name || S.R1.name) + "</h3><p>" + esc(S.R1.plain || S.R1.detail) +
        '</p><details><summary class="tech">How it is written in the file</summary><p class="note"><strong>' +
        esc(S.R1.technical_name || S.R1.name) + '.</strong> ' + esc(S.R1.detail) + '</p></details><p class="qualifier">' + esc(S.R1.caveat) + "</p></div>";
    }
    if (el("reuse-rest")) {
      var rest = ["R2", "R3", "R4", "R5", "R6"].filter(function (i) { return S[i]; });
      el("reuse-rest").innerHTML = rest.map(function (i) {
        var r = S[i];
        // The opening sentence goes in the summary, which is what shows when the
        // finding is closed. The body carries what follows it. Printing both the
        // teaser and the whole text repeated the first sentence every time.
        var full = String(r.plain || r.detail);
        var breakAt = full.indexOf(". ");
        var gist = breakAt === -1 ? full : full.slice(0, breakAt + 1);
        var rest = breakAt === -1 ? "" : full.slice(breakAt + 2);
        return "<details class=\"finding\"><summary>" + esc(r.plain_name || r.name) +
          '<span class="gist">' + esc(gist) + "</span></summary>" +
          (rest ? "<p>" + esc(rest) + "</p>" : "") +
          '<details><summary class="tech">How it is written in the file</summary><p class="note"><strong>' +
          esc(r.technical_name || r.name) + '.</strong> ' + esc(r.detail) + "</p></details>" +
          (r.mechanism_differs_from ? '<p class="note">' + esc(r.mechanism_differs_from) + "</p>" : "") +
          '<p class="qualifier">' + esc(r.caveat) + "</p></details>";
      }).join("");
    }

    /* What a pair at this setting actually looks like.

       The entries are not named. Two of the three marginal pairs carry product
       names that the vendor list did not catch, so naming them would break the
       safeguard, and picking different pairs to avoid that would mean choosing
       an example to dodge a safeguard. What is shown is the wording the two
       share, which is what produced the score and cannot contain a name that
       appears in only one of them. It is also the more useful thing to see:
       high similarity is often shared boilerplate rather than a shared system. */
    function marginalPair(e) {
      var node = el("thr-example");
      if (!node) { return; }
      if (!e) { node.innerHTML = ""; return; }
      var who = e.same_agency
        ? "Both are at the same agency."
        : "They are at two different agencies, so one system written down twice is unlikely.";
      var ref = e.neither_carries_an_identifier
        ? "Neither carries an identifier."
        : "Identifiers: " + e.identifiers.join(", ") + ".";
      node.innerHTML =
        '<p class="marginal-head">The closest call at this setting</p>' +
        "<p>Two entries scoring <strong>" + e.score + "</strong>. " + esc(who) + " " +
        esc(ref) + "</p>" +
        '<p class="marginal-label">The wording they share</p>' +
        '<p class="marginal-terms">' + e.shared_wording.map(function (w) {
          return '<span class="term">' + esc(w) + "</span>";
        }).join("") + "</p>" +
        '<p class="marginal-note">' + esc(e.reading) + "</p>";
    }

    // 2. The similarity control: the reader moves it and the count moves.
    var slider = el("thr");
    if (slider && S.M1) {
      var bands = S.M1.candidate_duplicates_not_confirmed;
      slider.max = String(bands.length - 1);
      var showBand = function () {
        var b = bands[Number(slider.value)];
        el("thr-value").textContent = b.threshold;
        el("thr-entries").textContent = n(b.entries_flagged);
        el("thr-share").textContent = b.share_of_register + "%";
        el("thr-pairs").textContent = n(b.candidate_pairs);
        marginalPair(b.example);
      };
      slider.addEventListener("input", showBand);
      showBand();
    }

    // 3. The empty-answer control: the reader switches the reading and watches
    // the figure change, rather than being told it changes.
    var toggle = el("empty-toggle");
    if (toggle && S.R1) {
      var figures = S.R1.figures;
      var corrected = false;
      var paint = function () {
        rows("emptylist", Object.keys(figures).map(function (k) {
          var f = figures[k];
          return "<tr><td>" + esc(label(k)) + "</td><td><strong>" +
            esc(corrected ? f.corrected : f.read_naively) + "</strong></td></tr>";
        }).join(""));
        el("empty-mode").textContent = corrected ? "What it actually holds" : "Read at a glance";
        toggle.textContent = corrected ? "Show how it reads at a glance" : "Show what they actually hold";
        toggle.setAttribute("aria-pressed", String(corrected));
      };
      toggle.addEventListener("click", function () { corrected = !corrected; paint(); });
      onLabels(paint);
      paint();
    }

    var prep = S["M2-preparation"];
    if (prep && el("folded")) {
      var per = prep.per_category;
      rows("folded", Object.keys(per)
        .sort(function (a, b) { return per[b].written_forms_folded_in - per[a].written_forms_folded_in; })
        .map(function (name) {
          return "<tr><td>" + esc(name) + "</td><td>" + n(per[name].written_forms_folded_in) + "</td></tr>";
        }).join(""));
    }

    if (S.M5 && el("uk-only")) {
      rows("uk-only", S.M5.asked_by_the_uk_not_by_the_federal_register.map(function (r) {
        return "<tr><td>" + esc(r.field) + "</td><td>" + esc(r.note) + "</td></tr>";
      }).join(""));
      rows("fed-only", S.M5.asked_by_the_federal_register_not_by_the_uk.map(function (r) {
        return "<tr><td>" + esc(r.field) + "</td><td>" + esc(r.note) + "</td></tr>";
      }).join(""));
    }

    if (S.M4 && el("bands")) {
      var b = S.M4.bands;
      var keys = Object.keys(b);
      // Each band links to the register filtered to those entries, so a finding
      // can be opened rather than only read.
      rows("bands", keys.map(function (k) {
        var value = k === "classification not recorded" ? "__none" : k;
        var href = "register.html?band=" + encodeURIComponent(value);
        return '<tr><td><a class="drill" href="' + href + '">' + esc(k) + "</a></td><td>" +
          n(b[k]) + "</td></tr>";
      }).join(""));
      el("band-sum").textContent = keys.map(function (k) { return n(b[k]); }).join(" + ") +
        " = " + n(S.M4.bands_total) + ", which is every entry in the register.";
    }

    if (S.M4 && el("coverage")) {
      var c = S.M4.oversight_field_coverage;
      var paintCoverage = function () {
        // The condition is stated once above the nine, not repeated on each row.
        var condition = GROUPS[Object.keys(c)[0]];
        var caption = condition
          ? '<tr class="groupline"><td colspan="2">' + esc(condition) + "</td></tr>"
          : "";
        rows("coverage", caption + Object.keys(c).map(function (k) {
          return "<tr><td>" + esc(label(k)) + "</td><td>" + c[k] + "%</td></tr>";
        }).join(""));
      };
      onLabels(paintCoverage);
      paintCoverage();
    }
  });
})();
