"""Reproducible builder for the Saber Pro academic paper (OPUS47 version).

Reads the structured content defined in ``paper/revised/paper_content.py``
and emits a Word document (``.docx``) with IEEE-style formatting:

- Two-column page setup is intentionally avoided here (the template used
  for the previous submission was a single-column letter draft). The
  builder focuses on correct typography, numbered headings, tables with
  borders, and figure placeholders.

Usage
-----
From the repository root::

    python scripts/build_paper.py --out outputs/saber_pro_paper_OPUS47.docx

The script is deterministic: running it twice produces byte-identical
documents up to the small set of internal fields that ``python-docx``
refreshes automatically (creation timestamp embedded by lxml).

Design
------
The function :func:`build_paper` is the single entry point. Dispatch on
the ``kind`` field of each section dict keeps the builder extensible:
adding a new block type (for example, code listings) only requires a
new ``_render_*`` helper and a branch in :func:`_render_section`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Make ``paper/revised`` importable without touching PYTHONPATH.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "paper" / "revised"))

import paper_content as C  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.table import WD_ALIGN_VERTICAL  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Cm, Pt, RGBColor  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def _set_cell_border(cell) -> None:
    """Add thin black borders to a table cell (all four sides)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        border = OxmlElement(f"w:{edge}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "4")
        border.set(qn("w:color"), "000000")
        tc_borders.append(border)
    tc_pr.append(tc_borders)


def _style_run(run, *, bold: bool = False, italic: bool = False,
               size_pt: float = 10.0, font: str = "Times New Roman") -> None:
    run.font.name = font
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)


def _add_paragraph(doc, text: str, *, size: float = 10.0,
                   align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                   bold: bool = False, italic: bool = False,
                   space_after: float = 6.0) -> None:
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(0.0)
    run = p.add_run(text)
    _style_run(run, bold=bold, italic=italic, size_pt=size)


# ---------------------------------------------------------------------------
# Block renderers
# ---------------------------------------------------------------------------


def _render_heading(doc, block) -> None:
    level = block.get("level", 1)
    number = block.get("number", "").strip()
    text = block["text"].strip()
    full = f"{number}. {text}" if number else text

    p = doc.add_paragraph()
    p.alignment = (
        WD_ALIGN_PARAGRAPH.CENTER if level == 1 else WD_ALIGN_PARAGRAPH.LEFT
    )
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(full)
    if level == 1:
        _style_run(run, bold=True, size_pt=11, font="Times New Roman")
    else:
        _style_run(run, bold=False, italic=True, size_pt=10,
                   font="Times New Roman")


def _render_paragraph(doc, block) -> None:
    _add_paragraph(doc, block["text"], size=10.0)


def _render_bullets(doc, block) -> None:
    for item in block["items"]:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        run = p.runs[0] if p.runs else p.add_run("")
        # ``List Bullet`` doesn't insert the text by itself via add_paragraph
        # when we pass a style; use explicit insertion:
        if not run.text:
            run = p.add_run(item)
        else:
            run.text = item
        _style_run(run, size_pt=10)


def _render_figure(doc, block) -> None:
    # Figure placeholder box: a centred italic caption line. Insertion of
    # actual PNG assets is intentionally out of scope here (figures live in
    # outputs/figures/ and are inserted by the submission template).
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run(f"[FIGURE {block['number']} PLACEHOLDER]")
    _style_run(run, italic=True, size_pt=9)

    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    run = cap.add_run(f"Fig. {block['number']}. {block['caption']}")
    _style_run(run, italic=False, size_pt=9)


def _render_table(doc, block) -> None:
    caption = doc.add_paragraph()
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_before = Pt(8)
    cap_run = caption.add_run(f"TABLE {block['number']}\n{block['caption']}")
    _style_run(cap_run, bold=False, size_pt=9)

    header = block["header"]
    rows = block["rows"]
    table = doc.add_table(rows=1 + len(rows), cols=len(header))
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.autofit = True

    # Header row
    for j, h in enumerate(header):
        cell = table.rows[0].cells[j]
        cell.text = ""
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(str(h))
        _style_run(run, bold=True, size_pt=9)
        _set_cell_border(cell)

    # Data rows
    for i, row in enumerate(rows, start=1):
        for j, value in enumerate(row):
            cell = table.rows[i].cells[j]
            cell.text = ""
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = (
                WD_ALIGN_PARAGRAPH.LEFT if j == 0 or j == len(row) - 1
                else WD_ALIGN_PARAGRAPH.CENTER
            )
            run = p.add_run(str(value))
            _style_run(run, size_pt=9)
            _set_cell_border(cell)

    # small spacer after the table
    doc.add_paragraph().paragraph_format.space_after = Pt(6)


_DISPATCH = {
    "heading": _render_heading,
    "paragraph": _render_paragraph,
    "bullets": _render_bullets,
    "figure": _render_figure,
    "table": _render_table,
}


def _render_section(doc, block) -> None:
    render = _DISPATCH.get(block["kind"])
    if render is None:
        raise ValueError(f"Unknown block kind: {block['kind']!r}")
    render(doc, block)


# ---------------------------------------------------------------------------
# Top-level layout
# ---------------------------------------------------------------------------


def _add_front_matter(doc) -> None:
    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(C.METADATA["title_es"])
    _style_run(run, bold=True, size_pt=14)

    # Author
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(C.METADATA["author"])
    _style_run(run, bold=False, size_pt=11)

    # Affiliation
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(C.METADATA["affiliation"])
    _style_run(run, italic=True, size_pt=9)

    # Repo
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run(f"Repositorio: {C.METADATA['repo']}")
    _style_run(run, italic=True, size_pt=9)


def _add_abstracts(doc) -> None:
    # Spanish abstract
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r1 = p.add_run("Resumen—")
    _style_run(r1, bold=True, italic=True, size_pt=9)
    r2 = p.add_run(C.ABSTRACT_ES)
    _style_run(r2, size_pt=9)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Index terms
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    r1 = p.add_run("Términos de indexación—")
    _style_run(r1, bold=True, italic=True, size_pt=9)
    r2 = p.add_run(C.INDEX_TERMS_ES)
    _style_run(r2, size_pt=9)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # English abstract
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    r1 = p.add_run("Abstract—")
    _style_run(r1, bold=True, italic=True, size_pt=9)
    r2 = p.add_run(C.ABSTRACT_EN)
    _style_run(r2, size_pt=9)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def _add_references(doc) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("REFERENCIAS")
    _style_run(run, bold=True, size_pt=11)

    for i, ref in enumerate(C.REFERENCES, start=1):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)
        run = p.add_run(f"[{i}] {ref}")
        _style_run(run, size_pt=9)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def _add_appendices(doc) -> None:
    for app in C.APPENDICES:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(app["title"])
        _style_run(run, bold=True, size_pt=11)
        for text in app["paragraphs"]:
            _add_paragraph(doc, text, size=10.0)


def build_paper(out_path: Path) -> Path:
    """Build the revised paper and write it to ``out_path``.

    Args:
        out_path: Destination .docx file.

    Returns:
        The absolute path that was written.
    """
    doc = Document()

    # Page margins (1 in / 2.54 cm all sides — IEEE submission style).
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    _add_front_matter(doc)
    _add_abstracts(doc)

    for block in C.SECTIONS:
        _render_section(doc, block)

    _add_references(doc)
    _add_appendices(doc)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    return out_path.resolve()


def _main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out",
        type=Path,
        default=REPO_ROOT / "outputs" / "saber_pro_paper_OPUS47.docx",
        help="Output .docx path (default: outputs/saber_pro_paper_OPUS47.docx)",
    )
    args = parser.parse_args(argv)
    written = build_paper(args.out)
    print(f"Wrote {written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
