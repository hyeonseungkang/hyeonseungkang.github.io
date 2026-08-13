# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Single-page static résumé/portfolio site for 강현승 (Hyeonseung Kang), served at https://hyeonseungkang.github.io. Content is in Korean. The site is built with **Jekyll** — repeatable portfolio data is configured in `_config.yml` and rendered dynamically via Liquid templates in `_layouts/default.html` + `index.html` + `stylesheet.css`.

## Workflow & Commands

- **Local Web Server Development:**
  - Build site: `jekyll build` or `bundle exec jekyll build`
  - Run dev server with live reload: `jekyll serve` or `bundle exec jekyll serve` (default at `http://localhost:4000`)
- **CV & Portfolio Document Generation:**
  - Generate CV DOCX: `python3 scripts/generate_cv_docx.py`
  - Generate Portfolio DOCX: `python3 scripts/generate_portfolio_docx.py`
  - Required Python packages: `pyyaml`, `python-docx`
- **Deployment & Automation:**
  - Pushing to `master` triggers [.github/workflows/jekyll.yml](.github/workflows/jekyll.yml), which builds the Jekyll site (`actions/jekyll-build-pages@v1`) and deploys `_site` to GitHub Pages.
  - [.github/workflows/generate-cv.yml](.github/workflows/generate-cv.yml) and [.github/workflows/generate-portfolio.yml](.github/workflows/generate-portfolio.yml) automatically regenerate `.docx` and `.pdf` documents when `_config.yml` or generator scripts change.

## Architecture & Configuration

- **`_config.yml`**: Central source of truth for all portfolio content:
  - Meta info: `title`, `author`, `email`, `cv_url`, `portfolio_url`, `github_url`, `bio`, `profile_photo`, `gallery`.
  - `sections`: Array of sections (`학력`, `프로젝트`, `경력사항`, `활동`, `자격사항`, `교육사항`, `수상`, `장학`).
  - Adding, removing, or updating items or sections in `_config.yml` automatically updates the Table of Contents (TOC), section headers, section anchor links, and generated CV/Portfolio documents.

- **`_layouts/default.html`**: Master Liquid layout template that dynamically renders:
  - Header & Profile
  - Gallery
  - TOC navigation (dynamically generated from `site.sections`)
  - Entry lists based on section `type`:
    - `edu` (`.entry-list--edu`) — 학력
    - `media` (`.entry-list--media`) — 프로젝트 / 교육사항 / 수상 / 장학 (collapses vertically on mobile ≤600px)
    - `history` (`.entry-list--history`) — 경력사항 / 활동 / 자격사항

- **`scripts/`**: Document generators parsing `_config.yml`:
  - `docx_utils.py`: Low-level XML manipulation utilities for Word document formatting.
  - `generate_cv_docx.py` / `generate_portfolio_docx.py`: Fills template files (`cv_template.docx`, `portfolio_template.docx`) to produce output in `data/ko/`.

- **`index.html`**: Front-matter entry point (`layout: default`).

## Responsive & Print Conventions

- **Breakpoint:** `600px` (`@media (max-width: 600px)`).
- **Mobile line breaks:** `<br class="mobile-break">` in data strings renders breaks only on mobile.
- **Print hiding:** `class="remove-on-print"` hides navigation and chrome elements when exporting to PDF / printing (`@media print`).

## Assets & Fonts

- **Images:** Stored in `images/`; favicons in `images/favicon/`.
- **Documents:** Generated PDFs and Word documents in `data/ko/`.
- **Fonts:** **Lato** via Google Fonts; Korean text falls back to system fonts.