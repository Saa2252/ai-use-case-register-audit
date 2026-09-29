/* View 1 register table.

   Rows are loaded from JSON (S5), never written into HTML. The completeness
   indicator counts, for that entry alone, how many core fields hold a value.

   Three behaviours beyond filtering:
   - a row expands to show that entry's whole field set, with blanks shown as
     blanks rather than omitted, because an empty field is part of what the
     register says;
   - the filters can be set from the address, so a finding on another view can
     link to the entries it describes;
   - the full field set is fetched only when a row is first opened, since it is
     much larger than the table itself. */

(function () {
  "use strict";

  var DATA = null, FULL = null, PAGE = 50, shown = PAGE, open = {};

  // The page carries a stamp covering every data file. Appending it means a
  // changed figure is fetched rather than served from a stale cache.
  function dataUrl(name) {
    var holder = document.querySelector("[data-dv]");
    var v = holder ? holder.getAttribute("data-dv") : "";
    return "data/" + name + (v ? "?v=" + v : "");
  }


  function el(id) { return document.getElementById(id); }

  function esc(s) {
    return String(s === undefined || s === null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function matches(row, q, stage, band) {
    if (stage === "__none" && row.s !== "") { return false; }
    if (stage && stage !== "__all" && stage !== "__none" && row.s !== stage) { return false; }
    if (band === "__none" && row.h !== "") { return false; }
    if (band && band !== "__all" && band !== "__none" && row.h !== band) { return false; }
    if (!q) { return true; }
    return (row.u + " " + row.a + " " + row.i).toLowerCase().indexOf(q) !== -1;
  }

  // The emptiness rule is fetched, never restated here. A second copy of a
  // rule drifts, and the drift stays invisible until someone checks one entry
  // by hand. This one already had: the rule held twenty-eight values and the
  // copy held twenty-one.
  var RULE = null, LABELS = {}, GROUPS = {};

  function label(column) {
    return LABELS[column] || column.replace(/_/g, " ");
  }

  function recordsNothing(field, value) {
    if (!RULE) { return String(value).trim() === ""; }
    var v = String(value).trim().toLowerCase();
    if (RULE.empty_always.indexOf(v) !== -1) { return true; }
    var type = (RULE.field_types || {})[field] || "free_text";
    var textual = type === "free_text" || type === "date" || type === "url";
    return textual && RULE.empty_in_text_and_url_fields_only.indexOf(v) !== -1;
  }

  function detailHtml(index) {
    if (!FULL) { return '<p class="note">Loading the full entry.</p>'; }
    var values = FULL.rows[index];
    // Fields asked only under a condition are introduced by that condition, once,
    // rather than each carrying it in its own name.
    var currentGroup = null;
    var cells = FULL.fields.map(function (field, i) {
      var value = values[i];
      var blank = recordsNothing(field, value);
      var group = GROUPS[field] || null;
      var header = "";
      if (group !== currentGroup) {
        currentGroup = group;
        if (group) {
          header = '<tr class="groupline"><th colspan="2">' + esc(group) + "</th></tr>";
        }
      }
      return header + "<tr><th>" + esc(label(field)) + "</th><td" +
        (blank ? ' class="blank">(blank)' : ">" + esc(value)) + "</td></tr>";
    }).join("");
    return '<p class="note">Every field this register publishes for this entry. Blanks are shown ' +
      'as blanks, because an empty field is part of what the register says. Vendor, product and ' +
      'contact fields are not present: they are removed from the published data.</p>' +
      '<div class="scroller"><table class="detail"><tbody>' + cells + "</tbody></table></div>";
  }

  function render() {
    if (!DATA) { return; }
    var q = el("q").value.trim().toLowerCase();
    var stage = el("stage").value;
    var band = el("band") ? el("band").value : "__all";
    var list = [];
    DATA.rows.forEach(function (r, i) { if (matches(r, q, stage, band)) { list.push([r, i]); } });
    el("count").textContent = list.length.toLocaleString("en-US");

    el("tbody").innerHTML = list.slice(0, shown).map(function (pair) {
      var r = pair[0], i = pair[1];
      var pct = Math.round((r.n / DATA.core_fields) * 100);
      var isOpen = !!open[i];
      var main = '<tr class="entry" data-index="' + i + '" tabindex="0" role="button" aria-expanded="' +
        isOpen + '"><td><span class="tw">' + (isOpen ? "▾" : "▸") + "</span> " + esc(r.u) +
        "</td><td>" + esc(r.a) + "</td><td>" + esc(r.s || "not recorded") + "</td><td>" +
        esc(r.h || "not recorded") + "</td><td>" + esc(r.i || "none") +
        '</td><td><span class="bar"><span style="width:' + pct + '%"></span></span> ' + pct + "%</td></tr>";
      var detail = isOpen
        ? '<tr class="detailrow"><td colspan="6">' + detailHtml(i) + "</td></tr>"
        : "";
      return main + detail;
    }).join("");
    el("more").classList.toggle("is-off", list.length <= shown);
  }

  function toggle(index) {
    if (open[index]) { delete open[index]; render(); return; }
    open[index] = true;
    if (FULL) { render(); return; }
    render();
    fetch(dataUrl("register_full.json")).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { FULL = d; render(); })
      .catch(function () { render(); });
  }

  function applyAddress() {
    var params = new URLSearchParams(window.location.search);
    var band = params.get("band"), stage = params.get("stage"), q = params.get("q");
    if (q) { el("q").value = q; }
    if (band && el("band")) { el("band").value = band; }
    if (stage) { el("stage").value = stage; }
    if (band || stage || q) {
      var note = el("from-finding");
      if (note) { note.classList.remove("is-off"); }
    }
  }

  fetch(dataUrl("field_labels.json"))
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (d) {
      LABELS = (d && d.labels) || {};
      GROUPS = (d && d.group_of) || {};
      render();
    })
    .catch(function () { LABELS = {}; });

  fetch(dataUrl("empty_value_rule.json"))
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (rule) { RULE = rule; })
    .catch(function () { RULE = null; });

  fetch(dataUrl("register_table.json")).then(function (r) { return r.json(); }).then(function (d) {
    DATA = d;
    var stages = {};
    d.rows.forEach(function (r) { if (r.s) { stages[r.s] = (stages[r.s] || 0) + 1; } });
    var sel = el("stage");
    Object.keys(stages).sort().forEach(function (s) {
      var o = document.createElement("option");
      o.value = s; o.textContent = s + " (" + stages[s].toLocaleString("en-US") + ")";
      sel.appendChild(o);
    });
    var none = d.rows.filter(function (r) { return r.s === ""; }).length;
    var o = document.createElement("option");
    o.value = "__none"; o.textContent = "no stage recorded (" + none.toLocaleString("en-US") + ")";
    sel.appendChild(o);

    var bands = {};
    d.rows.forEach(function (r) { if (r.h) { bands[r.h] = (bands[r.h] || 0) + 1; } });
    var bsel = el("band");
    Object.keys(bands).sort().forEach(function (b) {
      var opt = document.createElement("option");
      opt.value = b; opt.textContent = b + " (" + bands[b].toLocaleString("en-US") + ")";
      bsel.appendChild(opt);
    });
    var unclassified = d.rows.filter(function (r) { return r.h === ""; }).length;
    var bopt = document.createElement("option");
    bopt.value = "__none";
    bopt.textContent = "classification not recorded (" + unclassified.toLocaleString("en-US") + ")";
    bsel.appendChild(bopt);

    el("stage-coverage").textContent = (d.rows.length - none).toLocaleString("en-US") +
      " of " + d.rows.length.toLocaleString("en-US") + " entries carry a stage. " +
      none.toLocaleString("en-US") + " carry none and sit outside every option above.";

    applyAddress();
    render();
  });

  document.addEventListener("input", function (e) {
    if (e.target.id === "q") { shown = PAGE; open = {}; render(); }
  });
  document.addEventListener("change", function (e) {
    if (e.target.id === "stage" || e.target.id === "band") { shown = PAGE; open = {}; render(); }
  });
  document.addEventListener("click", function (e) {
    if (e.target.id === "more") { shown += PAGE * 4; render(); return; }
    if (e.target.id === "clear-filters") {
      el("q").value = ""; el("stage").value = "__all";
      if (el("band")) { el("band").value = "__all"; }
      shown = PAGE; open = {}; render();
      el("from-finding").classList.add("is-off");
      return;
    }
    var row = e.target.closest ? e.target.closest("tr.entry") : null;
    if (row) { toggle(Number(row.getAttribute("data-index"))); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") { return; }
    var row = e.target.closest ? e.target.closest("tr.entry") : null;
    if (row) { e.preventDefault(); toggle(Number(row.getAttribute("data-index"))); }
  });
})();
