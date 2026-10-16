# dv1612.github.io

Personal portfolio for **Dhruvi Vegda** — Business Analyst & Power BI developer.

**Live:** https://dv1612.github.io

Hand-built static site: semantic HTML, one stylesheet, ~150 lines of vanilla JavaScript.
No framework, no build step, no tracking.

### Features
- Dark/light theme following the system setting, with an explicit toggle remembered in `localStorage`
- Scroll-reveal animations, animated metric counters and scrollspy navigation — all disabled under `prefers-reduced-motion`
- Accessible dashboard lightbox (focus trap, Escape to close, restores focus)
- WebP imagery (~590 KB total), lazy loaded, with intrinsic sizes to avoid layout shift
- Open Graph card, JSON-LD `Person` schema, sitemap and canonical URL

### Structure
```
index.html      content and structure
styles.css      design tokens, components, responsive and print rules
script.js       theme, nav, reveal, counters, lightbox, clipboard
assets/img/     dashboard previews (WebP), portrait and Open Graph card
assets/         Dhruvi-Vegda-Resume.pdf (built from the LaTeX source)
```

### Local preview
```bash
python3 -m http.server 8000
# http://localhost:8000
```
