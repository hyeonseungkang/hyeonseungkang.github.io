#!/usr/bin/env python3
"""Regenerate data/ko/HyeonseungKang-CV.docx from _config.yml.

Only the 경력사항, 활동, and 자격사항 sections are synced into the CV — the
document keeps its existing scope rather than mirroring every section on
the website.
"""
from pathlib import Path

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "_config.yml"
OUTPUT_PATH = REPO_ROOT / "data" / "ko" / "HyeonseungKang-CV.docx"

# Not present in _config.yml (kept out of the public site data on purpose).
MOBILE = "+82 10-5934-0552"
PORTFOLIO_URL = "https://hyeonseungkang.github.io"

HISTORY_SECTION_IDS = ["경력사항", "활동"]
QUALIFICATION_SECTION_ID = "자격사항"
QUALIFICATION_HEADING = "어학 및 자격사항"


def load_config():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)
    sections_by_id = {section["id"]: section for section in config["sections"]}
    return config, sections_by_id


def add_header(doc, config):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    name_cell, contact_cell = table.rows[0].cells

    name_run = name_cell.paragraphs[0].add_run(config["title"])
    name_run.bold = True
    name_run.font.size = Pt(24)

    contact_lines = [
        ("Email: ", config["email"]),
        ("Mobile: ", MOBILE),
        ("Portfolio: ", PORTFOLIO_URL),
    ]
    contact_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i, (label, value) in enumerate(contact_lines):
        p = contact_cell.paragraphs[0] if i == 0 else contact_cell.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.add_run(label).bold = True
        p.add_run(value)


def add_history_table(doc, section):
    doc.add_heading(section["title"], level=2)
    table = doc.add_table(rows=0, cols=2)
    table.style = "Table Grid"
    for item in section["items"]:
        row = table.add_row()
        main_cell, period_cell = row.cells

        title_run = main_cell.paragraphs[0].add_run(item["title"])
        title_run.bold = True
        if item.get("description"):
            main_cell.add_paragraph(item["description"])

        period_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        period_cell.paragraphs[0].add_run(item["period"])


def add_qualification_table(doc, section):
    doc.add_heading(QUALIFICATION_HEADING, level=2)
    table = doc.add_table(rows=0, cols=3)
    table.style = "Table Grid"
    for item in section["items"]:
        row = table.add_row()
        title_cell, desc_cell, period_cell = row.cells

        title_cell.paragraphs[0].add_run(item["title"]).bold = True
        desc_cell.paragraphs[0].add_run(item.get("description", ""))
        period_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
        period_cell.paragraphs[0].add_run(item["period"])


def main():
    config, sections_by_id = load_config()

    doc = Document()
    add_header(doc, config)
    doc.add_paragraph()

    for section_id in HISTORY_SECTION_IDS:
        section = sections_by_id.get(section_id)
        if section is None:
            continue
        add_history_table(doc, section)
        doc.add_paragraph()

    qualification_section = sections_by_id.get(QUALIFICATION_SECTION_ID)
    if qualification_section is not None:
        add_qualification_table(doc, qualification_section)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
