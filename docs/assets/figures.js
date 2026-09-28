/* Loads every number shown on the site from JSON the notebook produces.
   Safeguard S5: no figure is typed into the HTML by hand.

   An element carries data-figure="<path>" and this script fills its text from
   the loaded data. Paths are dotted, e.g. "M4.bands.High-impact".
   data-fmt="n" renders a number with thousand separators.

   If the data cannot be loaded at all, the page says so once, at the top,
   rather than showing every figure as unavailable. A page whose data did not
   load is a broken page, not a register with missing values, and the two
   should not look the same. */

(function () {
  "use strict";

  var STORE = {};

  // The page carries a stamp covering every data file. Appending it means a
  // changed figure is fetched rather than served from a stale cache.
  function dataUrl(name) {
    var holder = document.querySelector("[data-dv]");
    var v = holder ? holder.getAttribute("data-dv") : "";
    return "data/" + name + (v ? "?v=" + v : "");
  }


  function get(path) {
    return path.split(".").reduce(function (acc, key) {
      return (acc === undefined || acc === null) ? undefined : acc[key];
    }, STORE);
  }

  function fmt(value, how) {
    if (value === undefined || value === null) { return null; }
    if (how === "n" && typeof value === "number") { return value.toLocaleString("en-US"); }
    return String(value);
  }

  function banner(isFileOrigin, missing) {
    var main = document.querySelector("main");
    if (!main) { return; }
    var box = document.createElement("div");
    box.className = "loadfail";
    box.setAttribute("role", "alert");
    var which = missing && missing.length ? missing.join(", ") : "its data files";
    var why = isFileOrigin
      ? "This page was opened directly from the filesystem. Browsers block a page served over file:// from reading local data files, so " + which + " could not be read."
      : "This page could not read " + which + ".";
    box.innerHTML = "<strong>The data did not load, so no figures are shown on this page.</strong>" +
      "<p>" + why + "</p>" +
      "<p>Serve the site over HTTP instead. From the repository root:</p>" +
      "<pre>python3 -m http.server 8765 --directory docs</pre>" +
      "<p>Then open <code>http://localhost:8765/</code>.</p>";
    main.insertBefore(box, main.firstChild);
    document.querySelectorAll("[data-figure]").forEach(function (el) {
      el.textContent = "\u2014";
      el.classList.add("pending");
    });
  }

  function fill() {
    document.querySelectorAll("[data-figure]").forEach(function (el) {
      var out = fmt(get(el.getAttribute("data-figure")), el.getAttribute("data-fmt"));
      if (out !== null) { el.textContent = out; }
      else { el.textContent = "unavailable"; el.classList.add("pending"); }
    });
    document.dispatchEvent(new CustomEvent("figures:ready", { detail: STORE }));
  }

  function load(url) {
    return fetch(url).then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  var SOURCES = [dataUrl("findings.json"), dataUrl("reusability_findings.json")];

  Promise.all(SOURCES.map(load))
    .then(function (res) {
      var missing = SOURCES.filter(function (url, i) { return !res[i]; });
      // Any missing source leaves figures on the page with nothing to show, so
      // the page says which file did not load rather than leaving the reader to
      // infer it from scattered placeholders.
      if (missing.length) {
        banner(window.location.protocol === "file:", missing);
        return;
      }
      var findings = res[0], reuse = res[1];
      if (findings && findings.findings) {
        findings.findings.forEach(function (f) { STORE[f.measure] = f; });
        STORE.meta = { generated: findings.generated };
      }
      if (reuse && reuse.findings) {
        reuse.findings.forEach(function (f) { STORE[f.id] = f; });
      }
      fill();
    });
})();
