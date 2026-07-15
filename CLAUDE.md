# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-page static résumé/portfolio site for 강현승 (Hyeonseung Kang), served at https://hyeonseungkang.github.io. Content is in Korean. The entire site is [index.html](index.html) + [stylesheet.css](stylesheet.css) — no build step, no JavaScript, no framework. It is a heavily customized fork of [Jon Barron's academic website template](https://github.com/jonbarron/jonbarron_website).

## Workflow

- **No build, lint, or test.** Edit HTML/CSS directly and preview by opening `index.html` in a browser (or any static server).
- **Deploy:** pushing to `master` triggers [.github/workflows/static.yml](.github/workflows/static.yml), which uploads the whole repository root to GitHub Pages. There is no staging — a push to `master` is a production deploy.
- Commit messages in history are a mix of Korean and Conventional-Commits English prefixes (`feat:`, `fix:`, `content:`).

## Layout system (the main thing to understand)

The page is a stack of résumé sections. Each section is an `<a id="한글">` anchor + an `<h2 class="section-heading">` + `<hr>` + one `.entry-list`. **When adding or renaming a section, keep three things in sync:** the anchor `id`, the `#`-hash-link inside the heading, and the matching link in the `.toc` block near the top.

`.entry-list` has three layout modifier classes that control how each `.entry` (an `.entry-side` + `.entry-main` pair) is arranged. Pick the one matching the content shape:

- `.entry-list--edu` — fixed-width date column (`.entry-side` 30%) beside a text column. Used for 학력.
- `.entry-list--media` — thumbnail image in `.entry-side` (sized to content), text in `.entry-main`. Used for 프로젝트/교육사항/수상/장학. **This is the only variant that collapses to vertical stacking on mobile** (≤600px).
- `.entry-list--history` — top-aligned date column beside text. Used for 경력사항/활동.

## Responsive & print conventions

- Breakpoint is **600px**, referenced in several `@media` blocks in the stylesheet.
- `class="mobile-break"` on a `<br>` renders the break only on mobile (hidden ≥600px) — used to wrap date ranges like `2018년 3월 -<br class="mobile-break">2021년 2월`.
- `class="remove-on-print"` hides an element in print/PDF export (`@media print`). Applied to the TOC, hash-links, the floating "상단으로" button, and the footer note. Add it to any navigation/chrome that shouldn't appear in a printed résumé.
- `#floating-button` ("상단으로" / back-to-top) is fixed-position and hidden on mobile.

## Assets

- Images live in [images/](images/) (many filenames are Korean); favicons in `images/favicon/`; downloadable PDFs (CV, papers) in [data/ko/](data/ko/).
- Fonts: only **Lato** is `@font-face`-loaded from Google's CDN; Korean text falls back to system fonts.
