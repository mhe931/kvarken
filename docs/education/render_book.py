"""Render the educational Markdown source as a DOCX and PDF.

Optional local tools: python-docx and PyMuPDF. No network access is used.
Run from the repository root with:
    python docs/education/render_book.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import NamedTuple

import pymupdf
from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "education" / "Kvarken_Thesis_Learn.md"
DOCX_PATH = SOURCE.with_name("Kvarken_Thesis_Learn.docx")
PDF_PATH = SOURCE.with_name("Kvarken_Thesis_Learn.pdf")
PAGE = pymupdf.paper_rect("a4")
MARGIN_X = 52
MARGIN_TOP = 54
MARGIN_BOTTOM = 48


class Block(NamedTuple):
    kind: str
    text: str = ""
    level: int = 0
    rows: tuple[tuple[str, ...], ...] = ()


GREEK = {
    r"\lambda": "λ",
    r"\rho": "ρ",
    r"\tau": "τ",
    r"\mu": "μ",
    r"\Sigma": "Σ",
    r"\Delta": "Δ",
    r"\mathbf": "",
    r"\boldsymbol": "",
    r"\mathrm": "",
    r"\text": "",
    r"\log": "log",
    r"\sum": "Σ",
}
SUBSCRIPT = str.maketrans("0123456789inxy", "₀₁₂₃₄₅₆₇₈₉ᵢₙₓᵧ")
SUPERSCRIPT = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def _take_group(value: str, start: int) -> tuple[str, int]:
    if start >= len(value) or value[start] != "{":
        return "", start
    depth = 0
    for index in range(start, len(value)):
        if value[index] == "{":
            depth += 1
        elif value[index] == "}":
            depth -= 1
            if depth == 0:
                return value[start + 1 : index], index + 1
    return value[start + 1 :], len(value)


def latex_to_text(value: str) -> str:
    """Convert the book's small LaTeX subset to readable Unicode text."""
    value = re.sub(r"\\begin\{(?:aligned|cases)\}|\\end\{(?:aligned|cases)\}", "", value)
    value = value.replace(r"\\", "\n").replace("&", "")
    value = value.replace(r"\qquad", "    ").replace(r"\quad", "  ")
    value = value.replace(r"\,", " ").replace(r"\left", "").replace(r"\right", "")
    value = value.replace(r"\leq", "≤").replace(r"\geq", "≥")
    value = value.replace(r"\approx", "≈").replace(r"\cdot", "·")
    value = value.replace(r"\times", "×").replace(r"\neq", "≠")
    value = value.replace(r"\mathrm{dB}", "dB").replace(r"\%", "%")

    # Resolve grouped commands and fractions from the inside out.
    for _ in range(12):
        old = value
        for command in (r"\frac", r"\mathrm", r"\text", r"\boldsymbol", r"\mathbf"):
            match = re.search(re.escape(command) + r"\{", value)
            while match:
                first, after_first = _take_group(value, match.end() - 1)
                if command == r"\frac":
                    second, after_second = _take_group(value, after_first)
                    replacement = f"({latex_to_text(first)})/({latex_to_text(second)})"
                    value = value[: match.start()] + replacement + value[after_second:]
                else:
                    replacement = latex_to_text(first)
                    value = value[: match.start()] + replacement + value[after_first:]
                match = re.search(re.escape(command) + r"\{", value)
        if value == old:
            break

    for command, replacement in GREEK.items():
        value = value.replace(command, replacement)
    value = re.sub(r"_\{([^{}]+)\}", lambda m: m.group(1).translate(SUBSCRIPT), value)
    value = re.sub(r"\^\{([^{}]+)\}", lambda m: m.group(1).translate(SUPERSCRIPT), value)
    value = re.sub(r"_([A-Za-z0-9]+)", lambda m: m.group(1).translate(SUBSCRIPT), value)
    value = re.sub(r"\^([A-Za-z0-9+-]+)", lambda m: m.group(1).translate(SUPERSCRIPT), value)
    value = re.sub(r"\\[a-zA-Z]+", "", value)
    value = value.replace(r"\{", "{").replace(r"\}", "}")
    value = value.replace(r"\_", "_").replace(r"\ ", " ")
    value = value.replace("{", "").replace("}", "")
    value = value.replace("=", " = ").replace("\n", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    return value.strip()


def _split_table_row(line: str) -> tuple[str, ...]:
    cells = line.strip().strip("|").split("|")
    return tuple(cell.strip().replace(r"\|", "|") for cell in cells)


def parse_markdown(text: str) -> list[Block]:
    lines = text.splitlines()
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            code: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += i < len(lines)
            blocks.append(Block("code", "\n".join(code), level=0))
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            blocks.append(Block("heading", heading.group(2).strip(), len(heading.group(1))))
            i += 1
            continue
        if i + 1 < len(lines) and line.startswith("|") and re.match(r"^\|?\s*:?-{3}", lines[i + 1]):
            rows = [_split_table_row(line)]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(_split_table_row(lines[i]))
                i += 1
            blocks.append(Block("table", rows=tuple(rows)))
            continue
        image = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", line)
        if image:
            blocks.append(Block("image", image.group(1) + "\n" + image.group(2)))
            i += 1
            continue
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(re.sub(r"^>\s?", "", lines[i]).strip())
                i += 1
            blocks.append(Block("quote", "\n".join(quote)))
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        number = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if bullet or number:
            list_kind = "bullet" if bullet else "number"
            items: list[str] = []
            item_pattern = r"^\s*[-*]\s+(.+)$" if list_kind == "bullet" else r"^\s*\d+\.\s+(.+)$"
            while i < len(lines):
                item = re.match(item_pattern, lines[i])
                if not item:
                    break
                items.append(item.group(1).strip())
                i += 1
            blocks.append(Block(f"{list_kind}_list", rows=tuple((item,) for item in items)))
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines):
            next_line = lines[i].rstrip()
            if (
                not next_line.strip()
                or next_line.startswith(("```", "#", ">", "|", "!["))
                or next_line.strip() == "---"
                or re.match(r"^\s*[-*]\s+", next_line)
                or re.match(r"^\s*\d+\.\s+", next_line)
            ):
                break
            paragraph.append(next_line.strip())
            i += 1
        blocks.append(Block("paragraph", " ".join(paragraph)))
    return blocks


def _inline_tokens(text: str) -> list[tuple[str, str]]:
    """Split a paragraph into plain, bold, italic, code, and linked runs."""
    pattern = re.compile(r"(\*\*.*?\*\*|`[^`]+`|\*[^*]+\*|\[[^\]]+\]\([^)]+\)|\\\(.*?\\\))")
    tokens: list[tuple[str, str]] = []
    cursor = 0
    for match in pattern.finditer(text):
        if match.start() > cursor:
            tokens.append(("plain", text[cursor : match.start()]))
        value = match.group()
        if value.startswith("**"):
            tokens.append(("bold", value[2:-2]))
        elif value.startswith("`"):
            tokens.append(("code", value[1:-1]))
        elif value.startswith("*"):
            tokens.append(("italic", value[1:-1]))
        elif value.startswith(r"\("):
            tokens.append(("math", latex_to_text(value[2:-2])))
        else:
            link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", value)
            tokens.append(("link", link.group(1) + "\n" + link.group(2)))
        cursor = match.end()
    if cursor < len(text):
        tokens.append(("plain", text[cursor:]))
    return tokens


def _html_inline(text: str) -> str:
    parts: list[str] = []
    for kind, value in _inline_tokens(text):
        if kind == "link":
            label, url = value.split("\n", 1)
            parts.append(f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>')
        elif kind == "bold":
            parts.append(f"<strong>{html.escape(value)}</strong>")
        elif kind == "italic":
            parts.append(f"<em>{html.escape(value)}</em>")
        elif kind == "code":
            parts.append(f"<code>{html.escape(value)}</code>")
        elif kind == "math":
            parts.append(f'<span class="math-inline">{html.escape(value)}</span>')
        else:
            parts.append(html.escape(value))
    return "".join(parts).replace("\n", "<br>")


def _set_cell_shading(cell, fill: str) -> None:
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shading)


def _add_hyperlink(paragraph, label: str, url: str) -> None:
    relationship = paragraph.part.relate_to(
        url,
        "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True,
    )
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), relationship)
    run = OxmlElement("w:r")
    properties = OxmlElement("w:rPr")
    color = OxmlElement("w:color")
    color.set(qn("w:val"), "176B87")
    properties.append(color)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    properties.append(underline)
    run.append(properties)
    content = OxmlElement("w:t")
    content.text = label
    run.append(content)
    link.append(run)
    paragraph._p.append(link)


def _add_docx_inline(paragraph, text: str) -> None:
    for kind, value in _inline_tokens(text):
        if kind == "link":
            label, url = value.split("\n", 1)
            _add_hyperlink(paragraph, label, url)
        else:
            run = paragraph.add_run(latex_to_text(value) if kind == "math" else value)
            if kind == "bold":
                run.bold = True
            elif kind == "italic":
                run.italic = True
            elif kind == "code":
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(35, 84, 95)
            elif kind == "math":
                run.font.name = "Cambria Math"


def _add_equation(doc, value: str) -> None:
    paragraph = doc.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(6)
    paragraph.paragraph_format.space_after = Pt(8)
    run = paragraph.add_run(latex_to_text(value))
    run.font.name = "Cambria Math"
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(20, 68, 83)


def _add_docx_table(doc, rows: tuple[tuple[str, ...], ...]) -> None:
    cols = max(len(row) for row in rows)
    table = doc.add_table(rows=1, cols=cols)
    table.style = "Light Shading Accent 1"
    table.autofit = True
    for row_index, source_row in enumerate(rows):
        cells = table.rows[0].cells if row_index == 0 else table.add_row().cells
        for col, cell in enumerate(cells):
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            value = source_row[col] if col < len(source_row) else ""
            cell.text = ""
            _add_docx_inline(cell.paragraphs[0], value)
            for run in cell.paragraphs[0].runs:
                run.font.size = Pt(8.5)
                if row_index == 0:
                    run.bold = True
            if row_index == 0:
                _set_cell_shading(cell, "DCEEF1")


def _docx_page_field(paragraph) -> None:
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instruction = OxmlElement("w:instrText")
    instruction.set(qn("xml:space"), "preserve")
    instruction.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    result = OxmlElement("w:t")
    result.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for element in (begin, instruction, separate, result, end):
        run._r.append(element)


def _source_lines(text: str) -> tuple[str, str, list[str]]:
    lines = text.splitlines()
    title = next(line[2:].strip() for line in lines if line.startswith("# "))
    subtitle = next(line[3:].strip() for line in lines if line.startswith("## "))
    start = next(
        i for i, line in enumerate(lines) if line.startswith("### How evidence is labelled")
    )
    return title, subtitle, lines[start:]


def build_docx(title: str, subtitle: str, body: str) -> None:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.72)
    section.bottom_margin = Inches(0.68)
    section.left_margin = Inches(0.78)
    section.right_margin = Inches(0.78)
    section.header_distance = Inches(0.32)
    section.footer_distance = Inches(0.32)

    styles = doc.styles
    styles["Normal"].font.name = "Calibri"
    styles["Normal"].font.size = Pt(10)
    styles["Normal"].paragraph_format.space_after = Pt(5)
    for name, size, color in (
        ("Title", 30, "13485A"),
        ("Heading 1", 21, "13485A"),
        ("Heading 2", 16, "176B87"),
        ("Heading 3", 12, "176B87"),
    ):
        style = styles[name]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)

    cover = doc.add_paragraph()
    cover.paragraph_format.space_before = Pt(120)
    cover.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover.add_run(title)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(30)
    run.font.color.rgb = RGBColor(19, 72, 90)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(16)
    run = para.add_run(subtitle)
    run.font.size = Pt(17)
    run.font.color.rgb = RGBColor(23, 107, 135)
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(30)
    para.add_run("Educational derivative · Version 1.0 · 26 October 2026").italic = True
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(14)
    para.add_run("Based on the MSc thesis by Däniel Ebrahimzadeh Esfahani")
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.space_before = Pt(115)
    para.add_run(
        "A beginner-to-advanced guide to Earth observation, data engineering, "
        "and the Kvarken case study"
    ).bold = True
    doc.add_page_break()

    header = section.header.paragraphs[0]
    header.text = "KVARKEN THESIS  ·  LEARN THE SCIENCE AND ENGINEERING"
    header.style = styles["Caption"]
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in header.runs:
        run.font.color.rgb = RGBColor(100, 120, 128)
        run.font.size = Pt(8)
    _docx_page_field(section.footer.paragraphs[0])

    blocks = parse_markdown(body)
    for block in blocks:
        if block.kind == "heading":
            paragraph = doc.add_paragraph(style=f"Heading {min(block.level, 3)}")
            if block.level == 1 and block.text.startswith("Lesson "):
                paragraph.paragraph_format.page_break_before = True
                paragraph.paragraph_format.keep_with_next = True
            paragraph.add_run(latex_to_text(block.text))
        elif block.kind == "paragraph":
            if re.fullmatch(r"\\\[.*?\\\]", block.text, flags=re.S):
                _add_equation(doc, block.text[2:-2])
            else:
                paragraph = doc.add_paragraph()
                _add_docx_inline(paragraph, block.text)
        elif block.kind == "code":
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.22)
            paragraph.paragraph_format.right_indent = Inches(0.16)
            paragraph.paragraph_format.space_before = Pt(4)
            paragraph.paragraph_format.space_after = Pt(8)
            for index, line in enumerate(block.text.splitlines()):
                if index:
                    paragraph.add_run().add_break()
                run = paragraph.add_run(line or " ")
                run.font.name = "Consolas"
                run.font.size = Pt(8.5)
                run.font.color.rgb = RGBColor(35, 55, 61)
            shading = OxmlElement("w:shd")
            shading.set(qn("w:fill"), "F1F5F6")
            paragraph._p.get_or_add_pPr().append(shading)
        elif block.kind == "table":
            _add_docx_table(doc, block.rows)
        elif block.kind == "image":
            alt, relative = block.text.split("\n", 1)
            image_path = (SOURCE.parent / relative).resolve()
            if not image_path.is_file():
                raise FileNotFoundError(f"Referenced figure is missing: {image_path}")
            paragraph = doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.keep_with_next = True
            shape = paragraph.add_run().add_picture(str(image_path), width=Inches(6.1))
            shape._inline.docPr.set("descr", alt)
        elif block.kind == "quote":
            paragraph = doc.add_paragraph()
            paragraph.paragraph_format.left_indent = Inches(0.28)
            paragraph.paragraph_format.right_indent = Inches(0.2)
            paragraph.paragraph_format.space_before = Pt(4)
            paragraph.paragraph_format.space_after = Pt(9)
            _add_docx_inline(paragraph, block.text)
            for run in paragraph.runs:
                run.italic = True
                run.font.color.rgb = RGBColor(58, 88, 97)
        elif block.kind in ("bullet_list", "number_list"):
            style_name = "List Bullet" if block.kind == "bullet_list" else "List Number"
            for (item,) in block.rows:
                paragraph = doc.add_paragraph(style=style_name)
                paragraph.paragraph_format.space_after = Pt(2)
                _add_docx_inline(paragraph, item)

    doc.core_properties.title = title
    doc.core_properties.subject = subtitle
    doc.core_properties.author = "Däniel Ebrahimzadeh Esfahani"
    doc.core_properties.keywords = (
        "Earth observation, Sentinel, Kvarken, remote sensing, data engineering"
    )
    doc.save(DOCX_PATH)


def _block_html(block: Block) -> str:
    if block.kind == "heading":
        level = min(block.level, 6)
        lesson_class = (
            ' class="lesson-heading"' if level == 1 and block.text.startswith("Lesson ") else ""
        )
        return f"<h{level}{lesson_class}>{_html_inline(latex_to_text(block.text))}</h{level}>"
    if block.kind == "paragraph":
        if re.fullmatch(r"\\\[.*?\\\]", block.text, flags=re.S):
            equation = latex_to_text(block.text[2:-2])
            return f'<div class="equation">{html.escape(equation).replace(chr(10), "<br>")}</div>'
        return f"<p>{_html_inline(block.text)}</p>"
    if block.kind == "code":
        return f"<pre><code>{html.escape(block.text)}</code></pre>"
    if block.kind == "table":
        headers = block.rows[0]
        entries = []
        for row in block.rows[1:]:
            first = row[0] if row else ""
            details = [
                f"<strong>{_html_inline(headers[index])}:</strong> {_html_inline(value)}"
                for index, value in enumerate(row[1:], start=1)
                if value
            ]
            if first:
                label = f"<strong>{_html_inline(first)}</strong>"
            elif details:
                label, details = details[0], details[1:]
            else:
                label = ""
            content = "<br>".join(([label] if label else []) + details)
            entries.append(f'<p class="table-row">{content}</p>')
        return '<div class="table-text">' + "".join(entries) + "</div>"
    if block.kind == "image":
        alt, relative = block.text.split("\n", 1)
        image_path = (SOURCE.parent / relative).resolve()
        if not image_path.is_file():
            raise FileNotFoundError(f"Referenced figure is missing: {image_path}")
        image_src = html.escape(image_path.relative_to(ROOT).as_posix(), quote=True)
        return (
            f'<figure><img src="{image_src}" '
            f'alt="{html.escape(alt, quote=True)}">'
            f"<figcaption>{html.escape(alt)}</figcaption></figure>"
        )
    if block.kind == "quote":
        return f"<blockquote>{_html_inline(block.text)}</blockquote>"
    if block.kind == "bullet_list":
        return "<ul>" + "".join(f"<li>{_html_inline(row[0])}</li>" for row in block.rows) + "</ul>"
    if block.kind == "number_list":
        return "<ol>" + "".join(f"<li>{_html_inline(row[0])}</li>" for row in block.rows) + "</ol>"
    return ""


PDF_CSS = """
@page { size: A4; margin: 0; }
body { font-family: sans-serif; font-size: 9.2pt; line-height: 1.38; color: #24343a; }
h1 { color: #13485a; font-size: 21pt; margin: 17pt 0 8pt; }
h1.lesson-heading { font-size: 23pt; -mupdf-keep-with-next: true; }
h2 { color: #176b87; font-size: 16pt; margin: 15pt 0 7pt; -mupdf-keep-with-next: true; }
h3 { color: #176b87; font-size: 11.5pt; margin: 11pt 0 5pt; -mupdf-keep-with-next: true; }
p { margin: 0 0 6pt; }
a { color: #176b87; text-decoration: underline; }
strong { color: #203c46; }
code { font-family: monospace; color: #23545f; }
pre { font-family: monospace; font-size: 7.8pt; background-color: #f1f5f6;
      border: 0.5pt solid #d7e2e5; padding: 7pt; }
.equation { text-align: center; font-family: sans-serif; font-size: 10.2pt;
            color: #13485a; margin: 7pt 0 10pt; }
.math-inline { font-family: sans-serif; color: #13485a; }
.table-text { margin: 5pt 0 10pt; font-size: 8.4pt; }
.table-row { border-left: 2pt solid #66a4b4; padding: 3pt 5pt; margin: 2pt 0 5pt; }
figure { text-align: center; margin: 9pt 0 11pt; }
img { max-width: 470pt; max-height: 520pt; }
figcaption { color: #52676e; font-size: 8pt; margin-top: 3pt; }
blockquote { color: #3a5861; background-color: #f1f5f6;
              border-left: 2pt solid #66a4b4; padding: 6pt 9pt; margin: 7pt 0; }
li { margin-bottom: 3pt; }
"""


def _html_document(content: str) -> str:
    content = content.replace("—", "–")
    return (
        '<!doctype html><html><head><meta charset="utf-8"></head><body>'
        + content
        + "</body></html>"
    )


def _render_story(writer, story: pymupdf.Story, *, page_start: int) -> int:
    page_number = page_start
    content_rect = pymupdf.Rect(
        MARGIN_X,
        MARGIN_TOP + 18,
        PAGE.width - MARGIN_X,
        PAGE.height - MARGIN_BOTTOM - 18,
    )
    while True:
        more, filled = story.place(content_rect)
        page = writer.begin_page(PAGE)
        story.draw(page)
        header = pymupdf.Story(
            html="<p>KVARKEN THESIS · LEARN THE SCIENCE AND ENGINEERING</p>",
            user_css="p { font-family: sans-serif; font-size: 7.5pt; color: #63787f; }",
        )
        header.place(pymupdf.Rect(MARGIN_X, 12, PAGE.width - MARGIN_X, 38))
        header.draw(page)
        footer = pymupdf.Story(
            html=f"<p>{page_number}</p>",
            user_css=(
                "p { font-family: sans-serif; font-size: 8pt; color: #63787f; text-align: center; }"
            ),
        )
        footer.place(
            pymupdf.Rect(MARGIN_X, PAGE.height - 34, PAGE.width - MARGIN_X, PAGE.height - 10)
        )
        footer.draw(page)
        writer.end_page()
        page_number += 1
        if not more:
            break
        if more and filled[3] <= content_rect.y0 + 0.1:
            raise RuntimeError("PDF layout made no progress on a page")
    return page_number


def build_pdf(title: str, subtitle: str, body: str) -> None:
    blocks = parse_markdown(body)
    cover = (
        '<div style="padding-top:125pt;text-align:center">'
        f'<h1 style="font-size:30pt">{html.escape(title)}</h1>'
        f'<p style="font-size:16pt;color:#176b87;margin-top:18pt">{html.escape(subtitle)}</p>'
        '<p style="margin-top:34pt"><em>Educational derivative · Version 1.0 · '
        "26 October 2026</em></p>"
        '<p style="margin-top:18pt">Based on the MSc thesis by Däniel Ebrahimzadeh Esfahani</p>'
        '<p style="margin-top:120pt"><strong>A beginner-to-advanced guide to Earth observation, '
        "data engineering, and the Kvarken case study</strong></p></div>"
    )
    writer = pymupdf.DocumentWriter(str(PDF_PATH))
    cover_story = pymupdf.Story(
        html=_html_document(cover), user_css=PDF_CSS, archive=pymupdf.Archive(str(ROOT))
    )
    page_number = _render_story(writer, cover_story, page_start=1)
    contents = "".join(_block_html(block) for block in blocks)
    story = pymupdf.Story(
        html=_html_document(contents),
        user_css=PDF_CSS,
        archive=pymupdf.Archive(str(ROOT)),
    )
    _render_story(writer, story, page_start=page_number)
    writer.close()


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    source = SOURCE.read_text(encoding="utf-8")
    title, subtitle, body_lines = _source_lines(source)
    body = "\n".join(body_lines)
    build_docx(title, subtitle, body)
    build_pdf(title, subtitle, body)
    print(f"Created {DOCX_PATH.relative_to(ROOT)}")
    print(f"Created {PDF_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
