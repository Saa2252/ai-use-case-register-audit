/* The fifth page. One file, one request, no figures from the findings.

   Nothing on this page was counted from a published file, so it does not load
   the findings and carries no data-figure placeholders. The attribute here is
   data-om, deliberately different, so a number from the audit can never be
   filled into this page by the script that fills the other four. */

(function () {
  "use strict";

  function el(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s === undefined || s === null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function resolve(data, path) {
    return path.split(".").reduce(function (acc, key) {
      return (acc === undefined || acc === null) ? undefined : acc[key];
    }, data);
  }

  /* The same five answers in the same order for every mechanism. Written from
     one list rather than five times, so no mechanism can quietly answer four
     questions while its neighbours answer five. */
  var ROWS = [
    ["What it is", "mechanism"],
    ["Who does it", "who"],
    ["What sets it off", "trigger"],
    ["What it leaves behind", "record"],
    ["What it costs", "cost"]
  ];

  function draw(d) {
    document.querySelectorAll("[data-om]").forEach(function (node) {
      var value = resolve(d, node.getAttribute("data-om"));
      if (value !== undefined) { node.textContent = value; }
    });

    var host = el("mechanisms");
    if (host) {
      host.innerHTML = d.mechanisms.map(function (m, i) {
        return '<article class="mech">' +
          '<h3><span class="mech-n">' + (i + 1) + "</span>" + esc(m.name) + "</h3>" +
          '<p class="mech-gap">' + esc(m.why) + "</p>" +
          '<dl class="mech-rows">' + ROWS.map(function (r) {
            return "<dt>" + esc(r[0]) + "</dt><dd>" + esc(m[r[1]]) + "</dd>";
          }).join("") + "</dl>" +
          '<div class="mech-trace">' +
          '<p><span class="mech-label">What this came from</span>' + esc(m.finding) + "</p>" +
          '<p><span class="mech-label">Where it is already solved</span>' + esc(m.covered_by) + "</p>" +
          "</div></article>";
      }).join("");
    }

    [["signals", "signals"], ["wrong", "would_show_it_wrong"]].forEach(function (pair) {
      var node = el(pair[0]);
      if (node) {
        node.innerHTML = d[pair[1]].map(function (s) {
          return "<li>" + esc(s) + "</li>";
        }).join("");
      }
    });
  }

  function dataUrl(name) {
    var holder = document.querySelector("[data-dv]");
    var v = holder ? holder.getAttribute("data-dv") : "";
    return "data/" + name + (v ? "?v=" + v : "");
  }

  function json(name) {
    return fetch(dataUrl(name)).then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  /* Same check as the other two scripts. This page carries no figures, but its
     containers are filled by id, and stale markup loses its rows without
     looking broken. */
  function isStale(stampFile) {
    var holder = document.querySelector("[data-dv]");
    var built = holder ? holder.getAttribute("data-dv") : "";
    var served = stampFile && stampFile.stamp;
    return Boolean(built && served && built !== served);
  }

  function problem(message, link) {
    var node = el("mechanisms");
    if (!node) { return; }
    node.innerHTML = '<div class="loadfail" role="alert"><strong>' + message + "</strong>" +
      (link ? '<p><a href="' + link + '">Load the current version</a></p>' : "") + "</div>";
  }

  Promise.all([json("operating_model.json"), json("build_stamp.json")])
    .then(function (res) {
      if (isStale(res[1])) {
        problem("This page is an older version than the data it just loaded, so nothing " +
                "on it has been filled in. Your browser still holds the previous copy.",
                window.location.pathname + "?r=" + Date.now());
        return;
      }
      if (!res[0]) {
        problem("This page could not read its data file. Serve the site over HTTP " +
                "rather than opening the file directly.", "");
        return;
      }
      draw(res[0]);
    });
})();
