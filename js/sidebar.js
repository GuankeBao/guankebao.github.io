(function () {
  function load() {
    var root = document.getElementById("sidebar-root");
    if (!root) return;
    var url = new URL("sidebar.html", location.href);
    fetch(url)
      .then(function (r) {
        if (!r.ok) throw new Error(String(r.status));
        return r.text();
      })
      .then(function (html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, "text/html");
        var aside = doc.querySelector("aside.sidebar");
        if (!aside) throw new Error("no sidebar in fragment");
        root.replaceWith(aside);
      })
      .catch(function (err) {
        console.error("sidebar load failed", err);
        root.innerHTML =
          '<p class="sidebar-fallback"><a href="index.html">Home</a></p>';
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
