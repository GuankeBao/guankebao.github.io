#!/usr/bin/env python3
"""One-off patch script — run from repo root then delete."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent

OLD_START = """      <div class="site-header-inner">
        <div class="site-header-main">
"""

NEW_START = """      <div class="site-header-inner">
        <div class="site-header-aside">
          <a href="index.html" class="site-header-portrait-link" aria-label="Guanke Bao — Home">
            <img class="portrait portrait--header" src="images/portrait.png" alt="" width="96" height="96" decoding="async" />
          </a>
          <div class="footer-socials header-socials" aria-label="Contact and profiles">
            <a class="footer-social" href="mailto:guanke.bao@gmail.com" aria-label="Email (Gmail)">
              <svg class="footer-social-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#EA4335" d="M24 5.457v13.909c0 .904-.732 1.636-1.636 1.636h-3.819V11.73L12 16.64l-6.545-4.91v9.273H1.636A1.636 1.636 0 0 1 0 19.366V5.457c0-2.023 2.641-2.641 4.39-1.19l6.974 5.238 6.974-5.238c1.749-1.451 4.39-.833 4.39 1.19z"/></svg>
            </a>
            <a class="footer-social" href="https://www.linkedin.com/in/guankebao/" rel="noopener noreferrer" aria-label="LinkedIn">
              <svg class="footer-social-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A66C2" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
            </a>
            <a class="footer-social footer-social--github" href="https://github.com/guankebao" rel="noopener noreferrer" aria-label="GitHub">
              <svg class="footer-social-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
            </a>
          </div>
        </div>
        <div class="site-header-body">
        <div class="site-header-main">
"""

OLD_END = """        <button type="button" class="theme-toggle" aria-label="Color theme" title="Theme">
          <svg class="theme-toggle-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
        </button>
      </div>
    </header>"""

NEW_END = """        <button type="button" class="theme-toggle" aria-label="Color theme" title="Theme">
          <svg class="theme-toggle-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
        </button>
        </div>
      </div>
    </header>"""

FOOTER_SOCIALS_RE = re.compile(
    r"\s*<div class=\"footer-socials\"[^>]*>[\s\S]*?</div>\s*\n",
    re.MULTILINE,
)

for p in sorted(root.glob("*.html")):
    if p.name.startswith("_"):
        continue
    s = p.read_text(encoding="utf-8")
    if "site-header-aside" in s:
        print("skip header", p.name)
    else:
        if OLD_START not in s:
            raise SystemExit(f"missing OLD_START: {p}")
        s = s.replace(OLD_START, NEW_START, 1)
        if OLD_END not in s:
            raise SystemExit(f"missing OLD_END: {p}")
        s = s.replace(OLD_END, NEW_END, 1)
    s2, n = FOOTER_SOCIALS_RE.subn("\n", s)
    if n:
        s = s2
        print("stripped footer socials", p.name)
    p.write_text(s, encoding="utf-8")
    print("ok", p.name)

Path(__file__).unlink()
print("removed patch script")
