/* Page four: the author's design view, and the site's landing page.

   Everything is loaded from data/fieldset.json, which is written by
   scripts/build_fieldset.py. The real panel is generated from the published
   register, so no value in it can be typed in by hand, and the reading steps
   beside it are generated from that panel's own rows.

   Motion here is only ever used to make a fact easier to see: the headline
   counts to its real value while the rows it describes recede, and the reading
   steps point at one row at a time. Under prefers-reduced-motion every one of
   those is off and the same content is present and readable. Nothing is behind
   a scroll: a reader can pass straight through and reach every section. */

(function () {
  "use strict";

  var STILL = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function esc(s) {
    return String(s === undefined || s === null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function el(id) { return document.getElementById(id); }

  function bold(text) {
    return esc(text).replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  }

  function dataUrl(name) {
    var holder = document.querySelector("[data-dv]");
    var v = holder ? holder.getAttribute("data-dv") : "";
    return "data/" + name + (v ? "?v=" + v : "");
  }

  function resolve(store, path) {
    return path.split(".").reduce(function (acc, key) {
      return (acc === undefined || acc === null) ? undefined : acc[key];
    }, store);
  }

  function num(v) {
    return typeof v === "number" ? v.toLocaleString("en-US") : String(v);
  }

  function json(name) {
    return fetch(dataUrl(name)).then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  /* ---- the evidence strip -------------------------------------------------

     Each figure is a card, not a link. Only the figure itself is selectable,
     so the qualification underneath it reads as text rather than disappearing
     into one long underline. */

  function drawEvidence(d) {
    var strip = el("evidence");
    if (!strip || !d.evidence) { return; }
    strip.innerHTML = d.evidence.map(function (e) {
      if (e.value === undefined || e.value === null) { return ""; }
      var of = (e.of_value === undefined) ? null : e.of_value;
      var shown = num(e.value) + (e.suffix || "");
      return '<div class="evcard">' +
        '<p class="evcard-fig"><a href="' + esc(e.link) + '">' + esc(shown) + "</a>" +
        (of !== null && of !== undefined ? '<span class="evcard-of"> of ' + esc(num(of)) + "</span>" : "") +
        "</p>" +
        '<p class="evcard-reads">' + esc(e.reads) + "</p>" +
        '<p class="evcard-caveat">' + esc(e.caveat) + "</p>" +
        "</div>";
    }).join("");

    var held = el("evidence-withheld");
    if (held && d.evidence_withheld) {
      held.innerHTML = '<p class="note"><strong>Two findings are not shown here as figures.</strong> ' +
        "Their qualification does not survive being shortened to a line, so they are linked instead of reduced to a number.</p>" +
        "<ul>" + d.evidence_withheld.map(function (e) {
          return '<li><a href="' + esc(e.link) + '">' + esc(e.name) + "</a>. " + esc(e.why) + "</li>";
        }).join("") + "</ul>";
    }
  }

  /* ---- the one counting motion -------------------------------------------

     The slots fill one at a time as the strip comes into view, and the boxes
     on the published form empty as the forms come into view. Each reveals the
     fact it sits next to, where that fact can be seen.

     This replaces counting the headline numeral upward. A numeral counting
     from zero prints figures that are not the finding: mid-count the sentence
     read "of 1 things ... answers 0", which contradicted the strip beside it.
     Filling the slots counts the same thing and can only ever show the real
     split, because the marks it fills are the ones the data already set. */

  function fillSlots(strip) {
    var filled = [].slice.call(strip.querySelectorAll(".slot.is-filled"));
    if (!filled.length) { return; }
    // Nothing is emptied until the moment the run starts, so a strip that is
    // never reached is never left blank.
    filled.forEach(function (slot) { slot.classList.remove("is-filled"); });
    function settle() { filled.forEach(function (slot) { slot.classList.add("is-filled"); }); }
    var guard = setTimeout(settle, 2000);
    filled.forEach(function (slot, i) {
      setTimeout(function () {
        slot.classList.add("is-filled");
        if (i === filled.length - 1) { clearTimeout(guard); }
      }, 170 * (i + 1));
    });
  }

  function watchOnce(node, run, threshold) {
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        watch.unobserve(entry.target);
        run(entry.target);
      });
    }, { threshold: threshold });
    watch.observe(node);
  }

  function armMotion() {
    var strip = el("slots"), forms = el("forms");
    // Without the observer, or with motion turned down, the strip already
    // shows the real split and the boxes are already empty. Nothing to do.
    if (STILL || !("IntersectionObserver" in window)) { return; }
    if (strip) { watchOnce(strip, fillSlots, 0.6); }
    if (forms) {
      watchOnce(forms, function () {
        document.body.classList.add("counting-rows");
        setTimeout(function () { document.body.classList.remove("counting-rows"); }, 700);
      }, 0.15);
    }
  }

  /* ---- the slot strip ----------------------------------------------------

     Ten marks beside the opening sentence, solid for a box the published entry
     answers and hollow for one it does not. It is the page's argument at a
     glance. Both the count and the split come from the data, and the caption
     states the same figures in words, so the strip never carries the meaning
     on shape or colour alone. */

  function drawSlots(d) {
    var host = el("slots");
    if (!host || !d.headline) { return; }
    var h = d.headline;
    var marks = "";
    for (var i = 0; i < h.fields; i++) {
      marks += '<span class="slot' + (i < h.a_real_entry_can_fill ? " is-filled" : "") + '"></span>';
    }
    host.innerHTML = marks;
    var caption = el("slots-caption");
    if (caption) {
      caption.textContent = h.a_real_entry_can_fill + " of " + h.fields +
        " boxes answered by a real published entry. " + h.a_real_entry_cannot_fill + " left blank.";
    }
  }

  /* ---- the two forms -----------------------------------------------------

     Not a table describing a form: the form itself, twice, label above box.
     A box the published entry cannot answer is drawn as an empty box with its
     outline still there, because the shape of an empty form is the thing a
     reader should see before reading a word of it. Why it is empty is said
     underneath, in words, so the difference never rests on the drawing alone. */

  function boxes(rows, real) {
    return rows.map(function (r, i) {
      var blank = real && r.state !== "from_source";
      var value = real ? r.value : r.value;
      return '<div class="ffield' + (blank ? " is-blank" : "") + '" data-row="' + i + '">' +
        '<span class="ffield-label"><span class="ffield-n">' + (i + 1) + "</span>" +
        esc(r.field) + "</span>" +
        '<div class="ffield-box' + (blank ? " is-blank " + esc(r.state) : "") + '">' +
        (blank ? "" : esc(value)) + "</div>" +
        (blank ? '<span class="ffield-note">' + esc(r.short) + "</span>" : "") +
        "</div>";
    }).join("");
  }

  function drawForms(d) {
    var host = el("forms");
    if (!host) { return; }
    var one = d.panel_one, two = d.panel_two;

    host.innerHTML =
      '<section class="formsheet real">' +
      '<p class="formsheet-head">A real published entry</p>' +
      '<p class="formsheet-sub">' + esc(one.entry_id) + ", " + esc(one.agency) + "</p>" +
      '<div class="formsheet-body">' + boxes(one.rows, true) + "</div></section>" +
      '<section class="formsheet mine">' +
      '<p class="formsheet-head">A made-up entry, filled in completely</p>' +
      '<p class="formsheet-sub">' + esc(two.organisation) + ", " + esc(two.system) + "</p>" +
      '<div class="formsheet-body">' + boxes(two.rows, false) + "</div></section>";

    if (el("p1-why")) { el("p1-why").textContent = one.why_this_entry; }
    if (el("p1-rule")) { el("p1-rule").textContent = one.rule; }
    if (el("p2-label")) { el("p2-label").textContent = two.label; }

    var bar = el("switch");
    if (!bar) { return; }
    bar.addEventListener("click", function (e) {
      var btn = e.target.closest && e.target.closest(".switch-btn");
      if (!btn) { return; }
      host.setAttribute("data-side", btn.getAttribute("data-side"));
      [].slice.call(bar.querySelectorAll(".switch-btn")).forEach(function (b) {
        b.setAttribute("aria-pressed", String(b === btn));
      });
    });
  }

  /* ---- the reading steps --------------------------------------------------

     Short steps move past the pinned panels, each one pointing at a single
     row. Without IntersectionObserver, or with motion turned down, every step
     is plain text in order and every row reads normally. */

  function drawSteps(d) {
    var host = el("steps");
    if (!host || !d.steps) { return; }
    host.innerHTML = d.steps.map(function (s) {
      return '<li class="step' + (s.state === "summary" ? " step-sum" : "") + '"' +
        (s.row === null ? "" : ' data-row="' + s.row + '"') + ">" +
        '<p class="step-field">' + esc(s.field) + "</p>" +
        '<p class="step-line">' + esc(s.line) + "</p></li>";
    }).join("");

    if (STILL || !("IntersectionObserver" in window)) { return; }

    var forms = el("forms");
    var steps = [].slice.call(host.querySelectorAll(".step"));
    var watch = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) { return; }
        // Only now is it safe to let the other steps recede.
        host.classList.add("armed");
        steps.forEach(function (s) { s.classList.toggle("here", s === entry.target); });
        var index = entry.target.getAttribute("data-row");
        if (!forms) { return; }
        [].slice.call(forms.querySelectorAll(".ffield")).forEach(function (field) {
          field.classList.toggle("lit", index !== null && field.getAttribute("data-row") === index);
        });
        forms.classList.toggle("reading", index !== null);
      });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(function (s) { watch.observe(s); });
  }

  /* ---- the field set ------------------------------------------------------

     Ten compact cards, closed, showing number and title. Opening one expands
     it in place. The owner's ruling to open everything applied to the five
     sections on the gaps page, not to these. */

  function drawFields(d) {
    var host = el("fields");
    if (!host) { return; }
    host.innerHTML = d.fields.map(function (f, i) {
      var parts = f.sub_fields
        ? '<ol class="subfields">' + f.sub_fields.map(function (s) {
            return "<li>" + esc(s) + "</li>";
          }).join("") + "</ol>"
        : "";
      return '<details class="fieldcard"><summary><span class="num">' + (i + 1) + "</span>" +
        '<span class="fieldcard-name">' + esc(f.name) + "</span></summary>" +
        '<div class="fieldcard-body">' +
        "<p>" + esc(f.records) + "</p>" + parts +
        '<p class="from"><strong>Why it is here.</strong> ' + esc(f.finding) +
        ' <a href="' + esc(f.finding_link) + '">See the finding</a></p>' +
        // A field whose only source is a three-entry register says so here,
        // beside itself, not only in the disclosure at the foot of the page.
        (f.rests_on ? '<p class="rests-on"><strong>What this rests on.</strong> ' +
          esc(f.rests_on) + "</p>" : "") +
        '<div class="scroller"><table><tbody>' +
        "<tr><th>The federal register, 2025</th><td>" + bold(f.us_2025) + "</td></tr>" +
        "<tr><th>The Ontario register</th><td>" + bold(f.ontario) + "</td></tr>" +
        "</tbody></table></div></div></details>";
    }).join("");

    if (d.convention) {
      var c = d.convention;
      el("convention").innerHTML =
        '<p class="convention-label">A rule the whole field set follows, not one of the fields</p>' +
        "<h3>" + esc(c.name) + "</h3><p>" + esc(c.records) + "</p>" +
        '<p class="from"><strong>Why it is here.</strong> ' + esc(c.finding) +
        ' <a href="' + esc(c.finding_link) + '">See the findings</a></p>';
    }
  }

  /* The account of how the work was done. A link only once the repository
     exists; the sentence still tells a reader where to find it either way. */
  function drawReadme(d) {
    var node = el("readme-link");
    if (!node) { return; }
    var account = "The full account of how the work was done, with nine judgment " +
      "calls made along the way, is in the file named README.";
    if (d.repository_url) {
      node.innerHTML = esc(account) + ' <a href="' + esc(d.repository_url) +
        '">Read it in the repository</a>.';
    } else {
      node.textContent = account + " The link is added when the project is published.";
    }
  }

  function drawFigures(d) {
    document.querySelectorAll("[data-figure]").forEach(function (node) {
      var value = resolve(d, node.getAttribute("data-figure"));
      // Counts are grouped the same way they are everywhere else on the site.
      if (value !== undefined) { node.textContent = num(value); }
    });
    if (el("limits")) {
      el("limits").innerHTML = d.limits.map(function (l) { return "<li>" + esc(l) + "</li>"; }).join("");
    }
  }

  /* One request, for the field set alone. Every figure on this page, the
     evidence strip included, is resolved when the site is built, so the
     landing page does not download the whole findings set to read five numbers
     out of it. tests/test_evidence_figures.py fails if any of those resolved
     figures drifts from the finding it came from. */
  json("fieldset.json")
    .then(function (d) {
      if (!d) {
        var strip = el("evidence");
        if (strip) {
          strip.innerHTML = '<p class="loadfail">The field set could not be loaded ' +
            "(data/fieldset.json). Nothing on this page has been filled in.</p>";
        }
        return;
      }
      drawFigures(d);
      drawSlots(d);
      drawForms(d);
      drawSteps(d);
      drawEvidence(d);
      drawFields(d);
      drawReadme(d);
      armMotion();
    });
})();
