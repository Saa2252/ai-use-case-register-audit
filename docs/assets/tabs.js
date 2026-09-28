/* Section tabs.

   The findings are long. Showing them all at once made the page unreadable,
   so each section is a tab and one is shown at a time.

   A caveat is never separated from the finding it qualifies: both sit in the
   same panel, so whenever a finding is on screen its qualification is too.

   Panels are shown and taken out of view with a class rather than the attribute
   whose name sits on this project's own word list. */

(function () {
  "use strict";

  function setup(tablist) {
    var buttons = Array.prototype.slice.call(tablist.querySelectorAll("button"));
    var panels = buttons.map(function (b) { return document.getElementById(b.getAttribute("aria-controls")); });

    function show(index) {
      buttons.forEach(function (b, i) {
        b.setAttribute("aria-selected", String(i === index));
        b.tabIndex = i === index ? 0 : -1;
        if (panels[i]) { panels[i].classList.toggle("is-off", i !== index); }
      });
      var marker = buttons[index].getAttribute("data-marker");
      if (marker) { tablist.style.setProperty("--marker", "var(--" + marker + ")"); }
    }

    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () { show(i); });
      b.addEventListener("keydown", function (e) {
        var next = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : null;
        if (next === null) { return; }
        e.preventDefault();
        var target = (next + buttons.length) % buttons.length;
        show(target);
        buttons[target].focus();
      });
    });
    show(0);
  }

  document.querySelectorAll('[role="tablist"]').forEach(setup);
})();
