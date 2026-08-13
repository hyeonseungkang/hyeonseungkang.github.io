#!/usr/bin/env python3
"""Regenerate data/ko/HyeonseungKang-Portfolio.docx from _config.yml.

The 학력, 프로젝트, 교육사항, 수상, and 장학 sections are synced into the
portfolio doc — the sections already covered by the CV (경력사항/활동/
자격사항, see generate_cv_docx.py) are left out. Content is written into a
copy of scripts/portfolio_template.docx; see docx_utils.py for how the
template's formatting is preserved.
"""
import copy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

from docx_utils import (
    format_date_token,
    format_period,
    get_section_tables,
    load_config,
    rebuild_table_rows,
    set_name_paragraph,
    set_paragraph_text,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_PATH = REPO_ROOT / "scripts" / "portfolio_template.docx"
OUTPUT_PATH = REPO_ROOT / "data" / "ko" / "HyeonseungKang-Portfolio.docx"

ACADEMIC_SECTION_ID = "학력"
PROJECT_SECTION_ID = "프로젝트"
TRAINING_SECTION_ID = "교육사항"
AWARD_SECTION_ID = "수상"
SCHOLARSHIP_SECTION_ID = "장학"


def fill_academic_row(tr, item):
    main_tc, period_tc = tr.findall(qn("w:tc"))
    set_paragraph_text(main_tc.find(qn("w:p")), item["main"])
    set_paragraph_text(period_tc.find(qn("w:p")), format_period(item["period"]))


def fill_project_row(tr, item):
    main_tc, period_tc = tr.findall(qn("w:tc"))
    main_ps = main_tc.findall(qn("w:p"))
    title_p, trailing_blank_p = main_ps[0], main_ps[-1]
    old_detail_ps = main_ps[1:-1]

    set_paragraph_text(title_p, item["title"])

    detail_template = copy.deepcopy(old_detail_ps[0])
    for p in old_detail_ps:
        main_tc.remove(p)

    anchor = title_p
    for detail_text in item.get("details", []):
        new_p = copy.deepcopy(detail_template)
        set_paragraph_text(new_p, detail_text)
        anchor.addnext(new_p)
        anchor = new_p

    period_p, _blank_p = period_tc.findall(qn("w:p"))
    set_paragraph_text(period_p, format_period(item["period"]))


def fill_training_row(tr, item):
    main_tc, period_tc = tr.findall(qn("w:tc"))
    title_p, detail_p = main_tc.findall(qn("w:p"))
    set_paragraph_text(title_p, item["title"])
    set_paragraph_text(detail_p, item.get("subtitle", ""))

    period_p, _blank_p = period_tc.findall(qn("w:p"))
    set_paragraph_text(period_p, format_period(item["period"]))


def fill_award_row(tr, item):
    main_tc, period_tc = tr.findall(qn("w:tc"))
    title_p, context_p, description_p = main_tc.findall(qn("w:p"))
    set_paragraph_text(title_p, item["title"])
    set_paragraph_text(context_p, item.get("event", ""))
    set_paragraph_text(description_p, item.get("description", ""))

    period_p, _blank_p = period_tc.findall(qn("w:p"))
    # subtitle holds "date, awarding org" (e.g. "2026년 6월, 중소벤처기업진흥공단");
    # the org already appears in the award title, so only the date is shown here.
    date_token = item.get("subtitle", "").split(",", 1)[0].strip()
    set_paragraph_text(period_p, format_date_token(date_token))


def fill_scholarship_row(tr, item):
    title_tc, period_tc = tr.findall(qn("w:tc"))
    set_paragraph_text(title_tc.find(qn("w:p")), item["title"])
    # 장학 items have no "period" field; subtitle holds the date(s) instead.
    set_paragraph_text(period_tc.find(qn("w:p")), format_period(item.get("subtitle", "")))


def main():
    config, sections_by_id = load_config()

    doc = Document(TEMPLATE_PATH)
    tables = get_section_tables(doc)

    set_name_paragraph(doc, tables, config["title"])

    rebuild_table_rows(
        tables[ACADEMIC_SECTION_ID],
        sections_by_id[ACADEMIC_SECTION_ID]["items"],
        fill_academic_row,
    )
    rebuild_table_rows(
        tables[PROJECT_SECTION_ID],
        sections_by_id[PROJECT_SECTION_ID]["items"],
        fill_project_row,
    )
    rebuild_table_rows(
        tables[TRAINING_SECTION_ID],
        sections_by_id[TRAINING_SECTION_ID]["items"],
        fill_training_row,
    )
    rebuild_table_rows(
        tables[AWARD_SECTION_ID],
        sections_by_id[AWARD_SECTION_ID]["items"],
        fill_award_row,
    )
    rebuild_table_rows(
        tables[SCHOLARSHIP_SECTION_ID],
        sections_by_id[SCHOLARSHIP_SECTION_ID]["items"],
        fill_scholarship_row,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_PATH)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
