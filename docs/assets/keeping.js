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

  fetch(dataUrl("operating_model.json"))
    .then(function (r) { return r.json(); })
    .then(draw)
    .catch(function () {
      var node = el("mechanisms");
      if (node) {
        node.innerHTML = '<p class="pending">This page could not read its data file. ' +
          "Serve the site over HTTP rather than opening the file directly.</p>";
      }
    });
})();
