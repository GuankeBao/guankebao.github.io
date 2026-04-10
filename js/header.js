(function () {
  function currentPageKey() {
    var path = location.pathname;
    var parts = path.split("/").filter(Boolean);
    var last = parts.length ? parts[parts.length - 1] : "";
    if (!last || last === "") return "index.html";
    if (last.indexOf(".") === -1) return "index.html";
    return last;
  }

  function setNavCurrent() {
    var key = currentPageKey();
    document.querySelectorAll(".nav a[href]").forEach(function (a) {
      a.removeAttribute("aria-current");
      var href = a.getAttribute("href");
      if (!href) return;
      var file = href.split("/").pop();
      if (file === key) a.setAttribute("aria-current", "page");
    });
  }

  function load() {
    var root = document.getElementById("site-header-root");
    if (!root) return;
    var url = new URL("/header.html", location.origin);
    fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        return r.text();
      })
      .then(function (html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");
        var header = doc.querySelector("header.site-header");
        if (!header) throw new Error("no header in fragment");
        root.replaceWith(header);
        setNavCurrent();
        if (typeof window.refreshThemeToggleUI === "function") {
          window.refreshThemeToggleUI();
        }
      })
      .catch(function (err) {
        console.error("header load failed", err);
        root.innerHTML =
          '<p class="site-header-fallback">Navigation could not load. <a href="/index.html">Home</a></p>';
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
