(function () {
  var KEY = "theme";
  var root = document.documentElement;
  var order = ["light", "dark", "auto"];

  function setButtonStates() {
    var current = root.getAttribute("data-theme") || "auto";
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      var i = order.indexOf(current);
      var next = order[(i + 1) % order.length];
      var curLabel =
        current === "auto" ? "System" : current.charAt(0).toUpperCase() + current.slice(1);
      var nextLabel =
        next === "auto" ? "system" : next;
      btn.setAttribute(
        "aria-label",
        "Color theme: " +
          curLabel +
          ". Activate to use " +
          nextLabel +
          " theme."
      );
      btn.title = "Theme: " + curLabel + " — click for " + nextLabel;
    });
  }

  function setTheme(value) {
    try {
      localStorage.setItem(KEY, value);
    } catch (e) {}
    root.setAttribute("data-theme", value);
    setButtonStates();
  }

  function cycleTheme() {
    var cur = root.getAttribute("data-theme") || "auto";
    var i = order.indexOf(cur);
    if (i < 0) i = 0;
    setTheme(order[(i + 1) % order.length]);
  }

  function onThemeToggleClick(e) {
    var btn = e.target && e.target.closest(".theme-toggle");
    if (!btn) return;
    e.preventDefault();
    cycleTheme();
  }

  function init() {
    setButtonStates();
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", function () {
        if (root.getAttribute("data-theme") === "auto") setButtonStates();
      });
    document.addEventListener("click", onThemeToggleClick);
  }

  window.refreshThemeToggleUI = setButtonStates;

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
