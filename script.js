/* Dhruvi Vegda — portfolio behaviour. No dependencies. */
(() => {
  "use strict";

  const $  = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- theme: system default, explicit choice remembered ---------- */
  const root = document.documentElement;
  const stored = (() => { try { return localStorage.getItem("theme"); } catch { return null; } })();
  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;
  root.dataset.theme = stored || (prefersLight ? "light" : "dark");

  $("#themeToggle")?.addEventListener("click", () => {
    const next = root.dataset.theme === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    $('meta[name="theme-color"]')?.setAttribute("content", next === "dark" ? "#0a0e1a" : "#f6f8fc");
    try { localStorage.setItem("theme", next); } catch { /* private mode */ }
  });

  /* ---------- sticky nav shadow ---------- */
  const nav = $("#nav");
  const onScroll = () => nav?.classList.toggle("is-stuck", window.scrollY > 12);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- mobile menu ---------- */
  const burger = $("#navBurger");
  const links  = $("#navLinks");
  burger?.addEventListener("click", () => {
    const open = links.classList.toggle("is-open");
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });
  $$("#navLinks a").forEach(a => a.addEventListener("click", () => {
    links.classList.remove("is-open");
    burger?.setAttribute("aria-expanded", "false");
  }));

  /* ---------- reveal on scroll ---------- */
  const revealables = $$(".reveal");
  if (reduced || !("IntersectionObserver" in window)) {
    revealables.forEach(el => el.classList.add("is-in"));
  } else {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry, i) => {
        if (!entry.isIntersecting) return;
        setTimeout(() => entry.target.classList.add("is-in"), Math.min(i * 70, 280));
        obs.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealables.forEach(el => io.observe(el));
  }

  /* ---------- counters ---------- */
  const counters = $$("[data-count]");
  const runCount = el => {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    if (reduced) { el.textContent = target + suffix; return; }
    const duration = 1100;
    const start = performance.now();
    const tick = now => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ("IntersectionObserver" in window) {
    const co = new IntersectionObserver((entries, obs) => {
      entries.forEach(e => { if (e.isIntersecting) { runCount(e.target); obs.unobserve(e.target); } });
    }, { threshold: 0.5 });
    counters.forEach(el => co.observe(el));
  } else {
    counters.forEach(runCount);
  }

  /* ---------- scrollspy ---------- */
  const navAnchors = $$('#navLinks a[href^="#"]');
  const sections = navAnchors
    .map(a => document.getElementById(a.getAttribute("href").slice(1)))
    .filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    const so = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navAnchors.forEach(a =>
          a.classList.toggle("is-active", a.getAttribute("href") === `#${entry.target.id}`));
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach(s => so.observe(s));
  }

  /* ---------- lightbox ---------- */
  const lb = $("#lightbox"), lbImg = $("#lightboxImg"), lbClose = $("#lightboxClose");
  let lastFocus = null;

  const openLightbox = btn => {
    lastFocus = btn;
    lbImg.src = btn.dataset.full;
    lbImg.alt = btn.dataset.alt || "";
    lb.hidden = false;
    document.body.style.overflow = "hidden";
    lbClose.focus();
  };
  const closeLightbox = () => {
    lb.hidden = true;
    lbImg.src = "";
    document.body.style.overflow = "";
    lastFocus?.focus();
  };

  $$(".shot").forEach(btn => btn.addEventListener("click", () => openLightbox(btn)));
  lbClose?.addEventListener("click", closeLightbox);
  lb?.addEventListener("click", e => { if (e.target === lb) closeLightbox(); });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !lb.hidden) closeLightbox();
    if (e.key === "Tab" && !lb.hidden) { e.preventDefault(); lbClose.focus(); }
  });

  /* ---------- copy email ---------- */
  const toast = $("#toast");
  let toastTimer;
  const showToast = msg => {
    toast.textContent = msg;
    toast.classList.add("is-on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("is-on"), 2400);
  };

  $("#copyMail")?.addEventListener("click", async function () {
    const mail = this.dataset.mail;
    try {
      await navigator.clipboard.writeText(mail);
      showToast("Email address copied");
    } catch {
      showToast(mail);   // clipboard blocked: show it so it can be selected
    }
  });

  /* ---------- footer year ---------- */
  const year = $("#year");
  if (year) year.textContent = String(new Date().getFullYear());
})();
