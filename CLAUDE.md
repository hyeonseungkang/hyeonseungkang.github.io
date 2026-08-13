# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-page static résumé/portfolio site for 강현승 (Hyeonseung Kang), served at https://hyeonseungkang.github.io. Content is in Korean. The site is built with **Jekyll** — repeatable portfolio data is configured in `_config.yml` and rendered dynamically via Liquid templates in `_layouts/default.html` + `index.html` + `stylesheet.css`.

## Workflow & Commands

- **Local Development:**
  - Build site: `jekyll build` or `bundle exec jekyll build`
  - Run dev server with live reload: `jekyll serve` or `bundle exec jekyll serve` (default at `http://localhost:4000`)
- **Deployment:** Pushing to `master` triggers [.github/workflows/static.yml](.github/workflows/static.yml), which builds the Jekyll site (`actions/jekyll-build-pages@v1`) and deploys `_site` to GitHub Pages.

## Architecture & Configuration

- **`_config.yml`**: Central source of truth for all portfolio content:
  - Meta info: `title`, `author`, `email`, `cv_url`, `github_url`, `bio`, `profile_photo`, `gallery`.
  - `sections`: Array of sections (`학력`, `프로젝트`, `경력사항`, `활동`, `자격사항`, `교육사항`, `수상`, `장학`).
  - Adding, removing, or updating items or sections in `_config.yml` automatically updates the Table of Contents (TOC), section headers, and section anchor links in sync.

- **`_layouts/default.html`**: Master Liquid layout template that dynamically renders:
  - Header & Profile
  - Gallery
  - TOC navigation (dynamically generated from `site.sections`)
  - Entry lists based on section `type`:
    - `edu` (`.entry-list--edu`) — 학력
    - `media` (`.entry-list--media`) — 프로젝트 / 교육사항 / 수상 / 장학 (collapses vertically on mobile ≤600px)
    - `history` (`.entry-list--history`) — 경력사항 / 활동 / 자격사항

- **`index.html`**: Front-matter entry point (`layout: default`).

## Responsive & Print Conventions

- **Breakpoint:** `600px` (`@media (max-width: 600px)`).
- **Mobile line breaks:** `<br class="mobile-break">` in data strings renders breaks only on mobile.
- **Print hiding:** `class="remove-on-print"` hides navigation and chrome elements when exporting to PDF / printing (`@media print`).

## Assets & Fonts

- **Images:** Stored in `images/`; favicons in `images/favicon/`.
- **Documents:** Downloadable PDFs in `data/ko/`.
- **Fonts:** **Lato** via Google Fonts; Korean text falls back to system fonts.