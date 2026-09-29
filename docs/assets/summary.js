/* View 2: the question summary and the reading path.

   The summary gives the whole argument in the time it takes to read five
   lines. Each row carries a question a reader would put to a register and the
   short factual answer, visible without clicking. Selecting a row jumps to the
   section that answers it.

   Every section is open. The five read in sequence for anyone who scrolls,
   each handing off to the next question, with a rail at the side showing where
   the reader is. Nothing is behind a click and nothing is behind a second
   level of navigation.

   Short answers are computed in the notebook and loaded, never written here.
   None of them states a verdict. */

(function () {
  "use strict";

  var SECTIONS = ["s-count", "s-recon", "s-time", "s-counting", "s-compare"];

  function esc(s) {
    return String(s === undefined || s === null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function el(id) { return document.getElementById(id); }

  /* Every section is open. The owner ruled on 30 September 2026 that the five
     sections read as one continuous argument, so a reader who scrolls and
     clicks nothing still gets the whole of it. The summary rows and the rail
     are both ways of jumping to a section, not ways of revealing one. */
  function go_to(id) {
    var section = el(id);
    if (!section) { return; }
    var still = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (still) {
      section.scrollIntoView({ block: "start" });
      return;
    }
    var before = window.scrollY;
    section.scrollIntoView({ behavior: "smooth", block: "start" });
    // Some browsers and some settings drop a smooth scroll without reporting
    // it, which would leave a row click doing nothing at all. If the page has
    // not moved shortly afterwards, move the reader plainly instead.
    setTimeout(function () {
      if (window.scrollY === before) { section.scrollIntoView({ block: "start" }); }
    }, 250);
  }

  function build(questions) {
    var host = el("questions");
    if (!host) { return; }

    host.innerHTML = questions.map(function (q, i) {
      var elsewhere = q.elsewhere
        ? '<p class="qrow-elsewhere">' + esc(q.elsewhere.question) + " " +
          esc(q.elsewhere.answer) + ' <a href="' + esc(q.elsewhere.link) + '">Read it</a></p>'
        : "";
      return '<div class="qrow" data-section="' + esc(SECTIONS[i]) + '">' +
        '<a class="qrow-head" href="#' + esc(SECTIONS[i]) + '">' +
        '<span class="qrow-n">' + (i + 1) + "</span>" +
        '<span class="qrow-q">' + esc(q.question) + "</span>" +
        '<span class="qrow-a">' + esc(q.answer) + "</span>" +
        "</a>" + elsewhere + "</div>";
    }).join("");

    host.addEventListener("click", function (e) {
      var head = e.target.closest && e.target.closest(".qrow-head");
      if (!head) { return; }
      e.preventDefault();
      go_to(head.getAttribute("href").slice(1));
    });
  }

  function buildRail(questions) {
    var rail = el("rail");
    if (!rail) { return; }
    rail.innerHTML = questions.map(function (q, i) {
      return '<a class="railmark" href="#' + esc(SECTIONS[i]) + '" title="' + esc(q.question) +
        '"><span class="railbar"></span><span class="railtext">' + esc(q.question) + "</span></a>";
    }).join("");

    rail.addEventListener("click", function (e) {
      var mark = e.target.closest && e.target.closest(".railmark");
      if (!mark) { return; }
      e.preventDefault();
      go_to(mark.getAttribute("href").slice(1));
    });

    var marks = Array.prototype.slice.call(rail.querySelectorAll(".railmark"));
    function mark() {
      var best = 0;
      SECTIONS.forEach(function (id, i) {
        var node = el(id);
        if (node && node.getBoundingClientRect().top < window.innerHeight * 0.4) { best = i; }
      });
      marks.forEach(function (m, i) { m.classList.toggle("here", i === best); });
    }
    window.addEventListener("scroll", mark, { passive: true });
    mark();
  }

  document.addEventListener("figures:ready", function (e) {
    var questions = (e.detail && e.detail.__questions) || null;
    if (!questions) { return; }
    build(questions);
    buildRail(questions);
  });
})();
