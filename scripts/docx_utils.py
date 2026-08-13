#!/usr/bin/env python3
"""Shared helpers for regenerating docx files from _config.yml by editing a
hand-designed template in place, rather than building a document from
scratch. Each dynamic table's first row is used as a formatting template
(cloned via its XML) so fonts, colors, indentation, and column widths stay
exactly as designed — only the text changes.
"""
import copy
import re
from pathlib import Path

import yaml
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = REPO_ROOT / "_config.yml"


def load_config():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)
    sections_by_id = {section["id"]: section for section in config["sections"]}
    return config, sections_by_id


def format_date_token(token):
    token = token.strip()
    if token == "현재" or not token:
        return token
    m = re.match(r"^(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일$", token)
    if m:
        y, mo, d = m.groups()
        return f"{y}. {int(mo)}. {int(d)}."
    m = re.match(r"^(\d{4})년\s*(\d{1,2})월$", token)
    if m:
        y, mo = m.groups()
        return f"{y}. {int(mo)}."
    return token


def format_period(period):
    # _config.yml periods separate the start/end date with either a plain
    # hyphen (" - ") or an en dash (" – "), depending on the section.
    for separator in (" - ", " – "):
        if separator in period:
            start, end = period.split(separator, 1)
            return f"{format_date_token(start)} – {format_date_token(end)} "
    return format_date_token(period)


def get_section_tables(doc):
    """Map each Heading 2 title (or "header" for the table before any
    heading) to the table that immediately follows it."""
    tables = {}
    current_heading = "header"
    table_iter = iter(doc.tables)
    for child in doc.element.body:
        tag = child.tag.split("}")[-1]
        if tag == "p":
            paragraph = Paragraph(child, doc)
            if paragraph.style is not None and paragraph.style.name == "Heading 2":
                current_heading = paragraph.text.strip()
        elif tag == "tbl":
            tables[current_heading] = next(table_iter)
    return tables


def strip_html_tags(text):
    """_config.yml text sometimes embeds HTML for the website (e.g.
    <em>...</em> for italics, <br class="mobile-break"> for line breaks);
    docx text runs can't render markup, so drop the tags."""
    return re.sub(r"<[^>]+>", "", text)


def set_paragraph_text(p, text):
    """Rewrite a <w:p> element's visible text in place, keeping the first
    run's formatting (font, color; indentation belongs to pPr and is left
    untouched) and dropping any other runs/proofErr markers."""
    text = strip_html_tags(text)
    for proof_err in p.findall(qn("w:proofErr")):
        p.remove(proof_err)

    runs = p.findall(qn("w:r"))
    if not runs:
        return

    first_run = runs[0]
    for extra_run in runs[1:]:
        p.remove(extra_run)

    t_elements = first_run.findall(qn("w:t"))
    if t_elements:
        t = t_elements[0]
        for extra_t in t_elements[1:]:
            first_run.remove(extra_t)
    else:
        t = OxmlElement("w:t")
        first_run.append(t)

    t.text = text
    t.set(qn("xml:space"), "preserve")


def rebuild_table_rows(table, items, fill_row, template_tr=None):
    tbl = table._tbl
    original_trs = tbl.findall(qn("w:tr"))
    if template_tr is None:
        template_tr = copy.deepcopy(original_trs[0])
    for tr in original_trs:
        tbl.remove(tr)
    for item in items:
        new_tr = copy.deepcopy(template_tr)
        fill_row(new_tr, item)
        tbl.append(new_tr)


def find_heading_paragraph(doc, heading_text):
    for child in doc.element.body:
        if child.tag.split("}")[-1] != "p":
            continue
        paragraph = Paragraph(child, doc)
        if paragraph.style is not None and paragraph.style.name == "Heading 2" and paragraph.text.strip() == heading_text:
            return child
    return None


def find_blank_line_template(doc):
    """The template inserts a blank Normal paragraph before most (but not
    all) Heading 2 paragraphs for vertical spacing. Grab one to reuse."""
    body = list(doc.element.body)
    for i, child in enumerate(body):
        if child.tag.split("}")[-1] != "p" or i == 0:
            continue
        paragraph = Paragraph(child, doc)
        if paragraph.style is None or paragraph.style.name != "Heading 2":
            continue
        prev = body[i - 1]
        if prev.tag.split("}")[-1] == "p" and Paragraph(prev, doc).text.strip() == "":
            return copy.deepcopy(prev)
    return None


def ensure_blank_line_before(doc, heading_text, blank_line_template):
    heading = find_heading_paragraph(doc, heading_text)
    if heading is None or blank_line_template is None:
        return
    prev = heading.getprevious()
    if prev is not None and prev.tag.split("}")[-1] == "p" and Paragraph(prev, doc).text.strip() == "":
        return
    heading.addprevious(copy.deepcopy(blank_line_template))


def set_name_paragraph(doc, tables, title):
    name_paragraph = tables["header"].rows[0].cells[0].paragraphs[0]
    set_paragraph_text(name_paragraph._p, title)
