#!/usr/bin/env python3
"""Regenerate data/ko/HyeonseungKang-CV.docx from _config.yml.

Only the 경력사항, 활동, and 자격사항 sections are synced into the CV — the
document keeps its existing scope rather than mirroring every section on
the website. Content is written into a copy of scripts/cv_template.docx;
see docx_utils.py for how the template's formatting is preserved.
"""
import copy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

from docx_utils import (
    ensure_blank_line_before,
    find_blank_line_template,
    format_period,
    get_section_tables,
    load_config,
    rebuild_table_rows,
    set_name_paragraph,
    set_paragraph_text,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "scripts" / "cv_template.docx"
OUTPUT_PATH = REPO_ROOT / "data" / "ko" / "HyeonseungKang-CV.docx"

CAREER_SECTION_ID = "경력사항"
ACTIVITY_SECTION_ID = "활동"
QUALIFICATION_SECTION_ID = "자격사항"
QUALIFICATION_HEADING = "어학 및 자격사항"


def fill_history_row(tr, item):
    main_tc, period_tc = tr.findall(qn("w:tc"))
    title_p, description_p = main_tc.findall(qn("w:p"))
    set_paragraph_text(title_p, item["title"])
    set_paragraph_text(description_p, item.get("description", ""))

    _, period_p = period_tc.findall(qn("w:p"))
    set_paragraph_text(period_p, format_period(item["period"]))


def fill_qualification_row(tr, item):
    title_tc, description_tc, period_tc = tr.findall(qn("w:tc"))
    set_paragraph_text(title_tc.find(qn("w:p")), item["title"])
    set_paragraph_text(description_tc.find(qn("w:p")), item.get("description", ""))
    set_paragraph_text(period_tc.find(qn("w:p")), format_period(item["period"]))


def build_qualification_template(table):
    """The template's 자격사항 table crams every entry into one row as
    stacked paragraphs (a leftover from manual editing) instead of one row
    per entry. Trim it down to a single-paragraph-per-cell row so it can be
    cloned per item like the other tables."""
    tr = copy.deepcopy(table._tbl.findall(qn("w:tr"))[0])
    for tc in tr.findall(qn("w:tc")):
        paragraphs = tc.findall(qn("w:p"))
        for paragraph in paragraphs[1:]:
            tc.remove(paragraph)
    return tr


def main():
    config, sections_by_id = load_config()

    doc = Document(TEMPLATE_PATH)
    tables = get_section_tables(doc)
    blank_line_template = find_blank_line_template(doc)

    set_name_paragraph(doc, tables, config["title"])

    # 경력사항's template row is already one-row-per-entry; reuse it for
    # 활동 too, since 활동's own row has the same stacked-paragraph drift
    # as the qualifications table.
    history_template = copy.deepcopy(tables[CAREER_SECTION_ID]._tbl.findall(qn("w:tr"))[0])

    rebuild_table_rows(
        tables[CAREER_SECTION_ID],
        sections_by_id[CAREER_SECTION_ID]["items"],
        fill_history_row,
        template_tr=history_template,
    )
    rebuild_table_rows(
        tables[ACTIVITY_SECTION_ID],
        sections_by_id[ACTIVITY_SECTION_ID]["items"],
        fill_history_row,
        template_tr=history_template,
    )

    qualification_table = tables[QUALIFICATION_HEADING]
    qualification_template = build_qualification_template(qualification_table)
    rebuild_table_rows(
        qualification_table,
        sections_by_id[QUALIFICATION_SECTION_ID]["items"],
        fill_qualification_row,
        template_tr=qualification_template,
    )

    # The template relied on a trailing blank paragraph inside 활동's old
    # single-row layout for spacing before this heading; that paragraph no
    # longer exists now that 활동 is rebuilt as one row per entry.
    ensure_blank_line_before(doc, QUALIFICATION_HEADING, blank_line_template)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
