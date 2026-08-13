# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-page static résumé/portfolio site for 강현승 (Hyeonseung Kang), served at https://hyeonseungkang.github.io. Content is in Korean. The entire site is [index.html](index.html) + [stylesheet.css](stylesheet.css) — no build step, no JavaScript, no framework. It is a heavily customized fork of [Jon Barron's academic website template](https://github.com/jonbarron/jonbarron_website).

## Workflow & Commands

- **No build, lint, or test steps.** Edit HTML/CSS directly.
- **Local Development:** Preview by opening `index.html` directly in a browser or running a static server:
  - `python3 -m http.server 8000`
  - `npx serve .`
- **Deployment:** Pushing to `master` triggers [.github/workflows/static.yml](.github/workflows/static.yml), which deploys the repository root to GitHub Pages. There is no staging environment — pushes to `master` deploy directly to production.
- **Commits:** Mix of Korean and Conventional Commits English prefixes (`feat:`, `fix:`, `content:`).

## Layout System

The page is a stack of résumé sections. Each section consists of an `<a id="한글">` anchor, an `<h2 class="section-heading">` heading with a hash link, an `<hr>`, and an `.entry-list`.

**Three-way synchronization:** When adding, removing, or renaming a section, keep three items in sync:
1. The section anchor `id` (e.g., `<a id="프로젝트"></a>`)
2. The hash link inside the section heading (e.g., `<a class="hash-link" href="#프로젝트">#</a>`)
3. The corresponding link in the `.toc` navigation block

`.entry-list` modifier classes control `.entry` layout:
- `.entry-list--edu` — Fixed-width date column (`.entry-side` 30%) beside text (`.entry-main`). Used for 학력.
- `.entry-list--media` — Thumbnail image in `.entry-side`, text in `.entry-main`. Used for 프로젝트/교육사항/수상/장학. **Collapses to vertical stacking on mobile (≤600px)**.
- `.entry-list--history` — Top-aligned date column beside text. Used for 경력사항/활동.

## Responsive & Print Conventions

- **Breakpoint:** `600px` (`@media (max-width: 600px)`).
- **Mobile line breaks:** `<br class="mobile-break">` renders breaks only on mobile screens (hidden on desktop).
- **Print hiding:** `class="remove-on-print"` hides navigation and chrome elements (TOC, hash links, floating back-to-top button, footer note) when printing or exporting to PDF (`@media print`).
- **Back-to-top button:** `#floating-button` is fixed-position and hidden on mobile.

## Assets & Fonts

- **Images:** Stored in `images/` (filenames include Korean terms); favicons in `images/favicon/`.
- **Documents:** Downloadable PDFs (CV, papers) in `data/ko/`.
- **Fonts:** **Lato** is loaded via Google Fonts; Korean text falls back to system fonts.