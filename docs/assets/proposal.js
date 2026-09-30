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
    if (!host || !d.headline || !d.panel_one) { return; }
    // One mark per row, carrying that row's own state. The strip used to draw
    // every unanswered box the same way and caption them "left blank", which
    // said the opposite of the paragraph beside it: none of them was asked and
    // left blank. A reader who looked at the picture and a reader who read the
    // words came away with different findings.
    host.innerHTML = d.panel_one.rows.map(function (r) {
      return '<span class="slot ' + esc(r.state) + '" title="' +
        esc(r.short || "answered by the published entry") + '"></span>';
    }).join("");
    var caption = el("slots-caption");
    // Written where the state words are, not here, so the caption and the marks
    // cannot describe different splits.
    if (caption) { caption.textContent = d.headline.slots_caption || ""; }
  }

  /* ---- the two forms -----------------------------------------------------

     Not a table describing a form: the form itself, twice, label above box.
     A box the published entry cannot answer is drawn as an empty box with its
     outline still there, because the shape of an empty form is the thing a
     reader should see before reading a word of it. Why it is empty is said
     underneath, in words, so the difference never rests on the drawing alone. */

  /* Nine answers inside one box is one answer with nine things written in it.
     The made-up entry used to store all nine as a paragraph, with two of them
     saying in words that there was no answer. That is an absence recorded as
     ordinary text, which is the one thing the convention on this page says no
     field does. Each of the nine now carries its own state, and a state that
     is not "answered" prints no answer at all. */
  function subRows(rows) {
    return '<ul class="ffield-sub">' + rows.map(function (s) {
      var answered = s.state === "answered";
      return '<li class="fsub' + (answered ? "" : " is-empty") + '">' +
        '<span class="fsub-label">' + esc(s.field) + "</span>" +
        (answered
          ? '<span class="fsub-value">' + esc(s.value) + "</span>"
          : '<span class="fsub-state ' + esc(s.state) + '">' + esc(s.state_word) + "</span>") +
        (s.ground ? '<span class="fsub-note">' + esc(s.ground) + "</span>" : "") +
        "</li>";
    }).join("") + "</ul>";
  }

  /* The two forms use different state words, because they record different
     things: what this project could read out of the published file, and what
     the proposed field set can hold. Each row carries its own state and its own
     caption, so neither side is drawn from an assumption about which it is. */
  function boxes(rows, real) {
    return rows.map(function (r, i) {
      var empty = real ? r.state !== "from_source" : r.state !== "answered";
      var note = real ? r.short : r.ground;
      return '<div class="ffield' + (empty ? " is-blank" : "") + '" data-row="' + i + '">' +
        '<span class="ffield-label"><span class="ffield-n">' + (i + 1) + "</span>" +
        esc(r.field) + "</span>" +
        '<div class="ffield-box' + (empty ? " is-blank " + esc(r.state) : "") +
        (r.sub_rows ? " has-sub" : "") + '">' +
        (r.sub_rows ? subRows(r.sub_rows)
          : (empty ? (real ? "" : '<span class="fsub-state ' + esc(r.state) + '">' +
             esc(r.state_word) + "</span>") : esc(r.value))) + "</div>" +
        (empty && note ? '<span class="ffield-note">' + esc(note) + "</span>" : "") +
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
      '<p class="formsheet-head">A made-up entry, every box resolved</p>' +
      '<p class="formsheet-sub">' + esc(two.organisation) + ", " + esc(two.system) + "</p>" +
      '<div class="formsheet-body">' + boxes(two.rows, false) + "</div></section>";

    if (el("p1-why")) { el("p1-why").textContent = one.why_this_entry; }
    if (el("p1-rule")) { el("p1-rule").textContent = one.rule; }
    if (el("p2-label")) { el("p2-label").textContent = two.label; }
    // What the right-hand form is showing. Not that every box holds words,
    // which is what it used to do, but that every box holds a state.
    if (el("p2-reading")) {
      el("p2-reading").textContent =
        (two.reading || "") + " " + (two.state_not_shown || "");
    }

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
        "<tr><th>The UK recording standard</th><td>" + bold(f.uk) + "</td></tr>" +
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
  /* Two cautions that qualify the whole field set. Loud rather than quiet,
     because a reader who takes the ten fields as a conclusion without them has
     taken more than the work supports. Figures come from the data like the
     rest. */
  function drawTiming(d) {
    var node = el("timing");
    if (!node || !d.timing) { return; }
    var t = d.timing;
    node.innerHTML =
      '<h2 class="h-caution">' + esc(t.heading) + "</h2>" +
      "<p class=\"caution-lead\">" + esc(t.lead) + "</p>" +
      '<p class="caution-fig"><strong>' + esc(num(t.in_progress_share)) + "%</strong> " +
      esc(t.reading) + "</p>" +
      "<p>" + esc(num(t.more_unfinished)) + " of the " + esc(num(t.entries_answering)) +
      " entries that answer at all, out of the " + esc(num(t.entries_asked)) +
      " the register asks, give more answers saying a step is under way " +
      "than saying it was done.</p>" +
      clock(t.the_clock) +
      '<p class="caution-take"><strong>' + esc(t.consequence) + "</strong></p>";
  }

  /* What the memorandum behind these fields actually says.

     This section used to decline to state the dates, because the project could
     not check them against a file it held. The memorandum was then downloaded,
     hashed and recorded like every other source, so the dates below are read
     from a file and the sections are named. The rule for reading the answer was
     written down before the memorandum was read, and it is printed here with
     the answer so a reader can see it was not chosen to suit the finding. */
  function clock(c) {
    if (!c) { return ""; }
    var rows = [
      ["The memorandum", c.source],
      ["The date it sets", c.deadline],
      ["Why it bears on these nine fields", c.why_it_bears_on_these_fields],
      ["What the register says about its own timing", c.what_the_register_says_about_its_own_timing],
      ["The rule, written down before the memorandum was read", c.rule_set_in_advance],
      ["The answer", c.answer],
      ["What would change it", c.what_would_change_it],
      ["What it still does not show", c.what_it_still_does_not_show]
    ];
    return '<div class="clockbox"><h3>' + esc(c.heading) + "</h3>" +
      '<dl class="clocklist">' + rows.map(function (r) {
        return "<dt>" + esc(r[0]) + "</dt><dd>" + esc(r[1]) + "</dd>";
      }).join("") + "</dl></div>";
  }

  function drawNotCovered(d) {
    var node = el("not-covered");
    if (!node || !d.not_covered) { return; }
    var n = d.not_covered;
    node.innerHTML =
      '<h2 class="h-caution">' + esc(n.heading) + "</h2>" +
      "<p class=\"caution-lead\">" + esc(n.lead) + "</p>" +
      '<ul class="misslist">' + n.missing.map(function (m) {
        // Each gap now says which published text covers it, so the section
        // names what is missing and where it has already been solved rather
        // than only the first.
        return "<li><strong>" + esc(m.name) + "</strong> " + esc(m.why) +
          (m.covered_by ? '<span class="covered"><span class="covered-label">' +
            "Covered by</span> " + esc(m.covered_by) + "</span>" : "") + "</li>";
      }).join("") + "</ul>" +
      "<p>" + esc(n.coverage) + "</p>" +
      "<p>" + esc(n.comparators_lead) + "</p>" +
      '<ul class="misslist">' + n.comparators.map(function (c) {
        // Whether a text was read is marked on the item itself. A comparator
        // nobody opened and one read from the publisher's own file are not the
        // same kind of statement and should not look alike.
        return '<li class="' + (c.read ? "was-read" : "not-read") + '">' +
          '<span class="readmark">' + (c.read ? "Read" : "Not read") + "</span>" +
          "<strong>" + esc(c.name) + "</strong> " + esc(c.what) +
          " <em>" + esc(c.why) + "</em>" +
          (c.what_it_settles ? '<span class="covered"><span class="covered-label">' +
            "What it settles</span> " + esc(c.what_it_settles) + "</span>" : "") +
          "</li>";
      }).join("") + "</ul>" +
      '<p class="caution-take"><strong>' + esc(n.consequence) + "</strong></p>";
  }

  /* The standing rules, published once. Each is a rule and a note saying where
     it bites, so a reader can check it against the figure in front of them
     rather than taking it as a disclaimer. */
  function drawReadingRules(d) {
    var node = el("reading-rules");
    if (!node || !d.reading) { return; }
    node.innerHTML = d.reading.rules.map(function (r) {
      return "<li><p class=\"howread-rule\">" + esc(r.rule) + "</p>" +
        '<p class="howread-where"><span class="howread-label">Where it bites</span>' +
        esc(r.applies_to) + "</p></li>";
    }).join("");
  }

  /* Ten fields is a design and nobody adopts a design. Each of the three
     carries the same four lines in the same order, so they can be read against
     each other: why it comes first, what it unlocks, what it costs, and the
     finding it answers. The cost is there for the same reason it is on the
     mechanisms page: a proposal with no costs in it is a wish. */
  function drawMinimumThree(d) {
    var node = el("minimum-three");
    if (!node || !d.minimum_three) { return; }
    var ROWS = [
      ["Why it comes first", "why_first"],
      ["What it unlocks", "unlocks"],
      ["What it costs", "cost"],
      ["What in the audit produced it", "evidence"]
    ];
    node.innerHTML = d.minimum_three.items.map(function (m) {
      return '<li class="minitem">' +
        '<h3>' + esc(m.name) +
        (m.position ? '<span class="minitem-ref">field ' + m.position + " of ten</span>"
                    : '<span class="minitem-ref">the rule, not a field</span>') + "</h3>" +
        '<p class="minitem-records">' + esc(m.records) + "</p>" +
        '<dl class="minitem-rows">' + ROWS.map(function (r) {
          return "<dt>" + esc(r[0]) + "</dt><dd>" + esc(m[r[1]]) + "</dd>";
        }).join("") + "</dl></li>";
    }).join("");
  }

  /* Who this is by, at the top rather than only in the footer. The link is
     rendered only when there is an address to point at, in the same way as the
     README link at the foot of the page. */
  function drawWhose(d) {
    var link = el("whose-link");
    if (!link || !d.about) { return; }
    if (d.repository_url) {
      link.setAttribute("href", d.repository_url);
      link.textContent = d.about.link_text;
    } else {
      link.remove();
    }
  }

  function drawReadme(d) {
    var node = el("readme-link");
    if (!node) { return; }
    var account = "The full account of how the work was done, with " +
      num(d.judgment_calls) + " judgment calls made along the way, is in the " +
      "file named README.";
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

  /* The page and the data it just fetched are from different builds. See the
     note on the same function in assets/figures.js: the host caches HTML for
     ten minutes, so shortly after a deployment a returning visitor can hold the
     previous markup while the data comes back current. A half-filled page is
     the state this exists to prevent, so nothing is drawn. */
  function staleBanner() {
    var main = document.querySelector("main");
    if (!main) { return; }
    var box = document.createElement("div");
    box.className = "loadfail";
    box.setAttribute("role", "alert");
    var fresh = window.location.pathname + "?r=" + Date.now();
    box.innerHTML = "<strong>This page is an older version than the figures it just loaded, " +
      "so nothing on it has been filled in.</strong>" +
      "<p>The site was updated in the last few minutes and your browser still holds the " +
      "previous copy of this page. Nothing here is wrong; this copy is simply out of date.</p>" +
      '<p><a href="' + fresh + '">Load the current version</a></p>';
    main.insertBefore(box, main.firstChild);
  }

  function isStale(stampFile) {
    var holder = document.querySelector("[data-dv]");
    var built = holder ? holder.getAttribute("data-dv") : "";
    var served = stampFile && stampFile.stamp;
    return Boolean(built && served && built !== served);
  }

  Promise.all([json("fieldset.json"), json("build_stamp.json")])
    .then(function (res) {
      var d = res[0];
      if (isStale(res[1])) { staleBanner(); return; }
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
      drawTiming(d);
      drawNotCovered(d);
      drawReadingRules(d);
      drawMinimumThree(d);
      drawWhose(d);
      drawReadme(d);
      armMotion();
    });
})();
