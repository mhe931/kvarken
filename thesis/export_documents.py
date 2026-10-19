"""Export this canonical LaTeX manuscript using the official Word template."""

import argparse
import re
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

FIGURES = (
    "Actual Sentinel-1A VV",
    "Independent Sentinel-2A",
    "Selective optical proxy reference:",
    "Scene-specific SAR candidate classes,",
    "Held-out optical-reference agreement",
)
FIGURE_DESCRIPTIONS = (
    "Sentinel-1A VV gamma-zero radar backscatter in eastern Kvarken on 30 March 2021. "
    "Grey tones show measured backscatter, not an ice classification; patterns can also "
    "reflect wind, incidence angle and residual preprocessing effects.",
    "Independent Sentinel-2A false-colour optical observation of eastern Kvarken, "
    "approximately 17.90 hours after the radar acquisition. Bright snow-covered ice "
    "and dark water support selective proxy labels, not field ground truth. "
    "Black areas lack usable coverage.",
    "Selective optical proxy reference on the analysed water domain: white snow-ice "
    "labels, blue dark-water labels, unlabelled water and excluded land/coastal areas. "
    "The proxy does not label all ice types or establish total sea-ice extent.",
    "Scene-specific SAR candidate map, with white ice candidates and blue water "
    "candidates within the screened domain. Candidate ice covers 1,219.28 square "
    "kilometres; 65.28 percent has no optical label. This is not validated total ice extent.",
    "Held-out spatial-block agreement map comparing SAR candidates with selective "
    "optical labels. Green cells agree and brown cells disagree; other cells are "
    "unlabelled or excluded. Ice precision is 23.53 percent against this proxy.",
)
TABLES = (
    "Research questions, primary evidence,",
    "Frozen 256-scene synthetic experiment baseline.",
    "Held-out confusion matrix.",
    "Held-out proxy agreement.",
)


def _field(paragraph, instruction: str) -> None:
    for tag in ("begin", "separate", "end"):
        run = paragraph.add_run()
        marker = OxmlElement("w:fldChar")
        marker.set(qn("w:fldCharType"), tag)
        run._r.append(marker)
        if tag == "begin":
            text = OxmlElement("w:instrText")
            text.set(qn("xml:space"), "preserve")
            text.text = " " + instruction + " "
            run._r.append(text)
        elif tag == "separate":
            paragraph.add_run("Update field")


def _prefix(paragraph, text: str) -> None:
    run = paragraph.add_run(text)
    paragraph._p.insert(1 if paragraph._p.pPr is not None else 0, run._r)


def format_document(path: Path) -> dict:
    document = Document(path)
    document.core_properties.title = (
        "Design and Implementation of a Hybrid Earth Observation Data Infrastructure"
    )
    document.core_properties.author = "Daniel Ebrahimzadeh Esfahani"
    document.core_properties.last_modified_by = "AI-assisted manuscript export"
    paragraphs = document.paragraphs
    abstract_start = next(
        (i for i, p in enumerate(paragraphs) if p.text.startswith("UNIVERSITY OF VAASA")), None
    )
    abstract_end = next(
        (i for i, p in enumerate(paragraphs) if p.text.startswith("Keywords:")), None
    )
    if abstract_start is None or abstract_end is None or abstract_start >= abstract_end:
        raise ValueError("canonical abstract and keywords are required")
    for i, paragraph in enumerate(paragraphs):
        drawings = paragraph._p.xpath(".//wp:docPr")
        if not drawings:
            continue
        caption = next((p.text for p in paragraphs[i + 1 :] if p.text.strip()), "")
        for prefix, description in zip(FIGURES, FIGURE_DESCRIPTIONS, strict=True):
            if caption.startswith(prefix):
                for drawing in drawings:
                    drawing.set("descr", description)
                break
    styles = document.styles
    for name in ("Normal", "Body Text", "Bibliography"):
        if name not in styles:
            continue
        styles[name].font.name = "Calibri"
        styles[name].font.size = Pt(12)
        styles[name].paragraph_format.line_spacing = 1.5
        styles[name].paragraph_format.space_after = Pt(6)
    for level, size in ((1, 16), (2, 14), (3, 12)):
        style = styles[f"Heading {level}"]
        style.font.name = "Calibri"
        style.font.size = Pt(size)
        style.font.bold = True
        style.paragraph_format.page_break_before = level == 1
        style.paragraph_format.keep_with_next = True
        if style.element.pPr is not None:
            number = style.element.pPr.find(qn("w:numPr"))
            if number is not None:
                style.element.pPr.remove(number)
    front = styles.add_style("Front Matter", 1)
    front.base_style = styles["Heading 1"]
    for section in document.sections:
        section.page_width, section.page_height = Cm(21), Cm(29.7)
        section.top_margin = section.bottom_margin = Cm(3)
        section.left_margin = section.right_margin = Cm(3)
        section.header_distance = Cm(1.5)
        section.different_first_page_header_footer = True
        header = section.header.paragraphs[0]
        header.clear()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _field(header, "PAGE")
        for run in header.runs:
            run.font.name, run.font.size = "Calibri", Pt(11)
        for footer in (section.footer, section.first_page_footer, section.first_page_header):
            for paragraph in footer.paragraphs:
                paragraph.clear()
    for i, paragraph in enumerate(paragraphs):
        if i < abstract_start:
            if not paragraph.text and not paragraph._p.xpath(".//w:drawing"):
                paragraph._p.getparent().remove(paragraph._p)
                continue
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.line_spacing = 1
            suppress = OxmlElement("w:suppressAutoHyphens")
            paragraph._p.get_or_add_pPr().append(suppress)
            if paragraph.text.startswith(("Master", "School", "Major", "Supervisor")):
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            size = 12
            if paragraph.text == "Daniel Ebrahimzadeh Esfahani":
                size = 16
                paragraph.paragraph_format.space_before = Pt(81)
            elif paragraph.text.startswith("Design and Implementation"):
                size = 20
                paragraph.paragraph_format.space_before = Pt(20)
            elif paragraph.text.startswith("for Research"):
                size = 14
                paragraph.paragraph_format.space_after = Pt(35)
            elif paragraph.text == "Vaasa 2026":
                paragraph.paragraph_format.space_before = Pt(230)
            for run in paragraph.runs:
                run.font.name, run.font.size = "Calibri", Pt(size)
                run.bold = paragraph.text.startswith("Design and Implementation")
        elif i <= abstract_end:
            paragraph.alignment = (
                WD_ALIGN_PARAGRAPH.LEFT
                if paragraph.text.startswith(("UNIVERSITY", "Keywords:", "Abstract"))
                else WD_ALIGN_PARAGRAPH.JUSTIFY
            )
            paragraph.paragraph_format.line_spacing = 1
            paragraph.paragraph_format.space_after = Pt(2)
            for run in paragraph.runs:
                run.font.name, run.font.size = "Calibri", Pt(11)
    paragraphs[abstract_start].paragraph_format.page_break_before = True
    if document.tables:
        for row in document.tables[0].rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.line_spacing = 1
                    paragraph.paragraph_format.space_after = Pt(0)
                    for run in paragraph.runs:
                        run.font.name, run.font.size = "Calibri", Pt(11)
    for table in document.tables:
        if table.cell(0, 0).text != "ACID":
            continue
        for header in table.rows[0]._tr.xpath("./w:trPr/w:tblHeader"):
            header.getparent().remove(header)
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.line_spacing = 1
                    paragraph.paragraph_format.space_after = Pt(3)
    chapter = section = subsection = 0
    appendix = False
    appendix_letter = ""
    figure_entries, table_entries = [], []
    bookmark_id = (
        max(
            (int(node.get(qn("w:id"))) for node in document.element.xpath(".//w:bookmarkStart")),
            default=0,
        )
        + 1
    )
    for paragraph in paragraphs[abstract_end + 1 :]:
        if paragraph._p.xpath(".//w:drawing"):
            paragraph.paragraph_format.keep_with_next = True
        text = paragraph.text
        if paragraph.style.name == "Heading 1":
            if text in {"Acknowledgements", "Abbreviations"}:
                paragraph.style = front
            elif text == "Disclosure of AI-Assisted Work":
                appendix = True
                appendix_letter = "A"
                section = subsection = 0
                paragraph.style = front
                _prefix(paragraph, "A  ")
            elif appendix:
                appendix_letter = "B"
                section = subsection = 0
                paragraph.style = front
                _prefix(paragraph, "B  ")
            else:
                chapter += 1
                section = subsection = 0
                _prefix(paragraph, f"{chapter}  ")
        elif paragraph.style.name == "Heading 2":
            section += 1
            subsection = 0
            _prefix(paragraph, f"{appendix_letter or chapter}.{section}  ")
        elif paragraph.style.name == "Heading 3":
            subsection += 1
            _prefix(paragraph, f"{appendix_letter or chapter}.{section}.{subsection}  ")
        kind = (
            "Figure" if text.startswith(FIGURES) else "Table" if text.startswith(TABLES) else None
        )
        if kind:
            entries = figure_entries if kind == "Figure" else table_entries
            number = (
                f"6.{len(entries) + 1}"
                if kind == "Figure"
                else ("3.1" if not entries else f"6.{len(entries)}")
            )
            _prefix(paragraph, f"{kind} {number}. ")
            paragraph.paragraph_format.line_spacing = 1
            paragraph.paragraph_format.keep_together = True
            if kind == "Table":
                paragraph.paragraph_format.keep_with_next = True
            for run in paragraph.runs:
                run.font.size = Pt(11)
            bookmark = f"thesis{kind}{bookmark_id}"
            start, end = OxmlElement("w:bookmarkStart"), OxmlElement("w:bookmarkEnd")
            start.set(qn("w:id"), str(bookmark_id))
            start.set(qn("w:name"), bookmark)
            end.set(qn("w:id"), str(bookmark_id))
            paragraph._p.insert(1 if paragraph._p.pPr is not None else 0, start)
            paragraph._p.append(end)
            short_caption = re.split(r"\.(?:\s|$)", text, maxsplit=1)[0]
            entries.append((f"{kind} {number}. {short_caption}", bookmark))
            bookmark_id += 1
    appendix_start = next(
        p for p in document.paragraphs if p.text == "A  Disclosure of AI-Assisted Work"
    )
    references = appendix_start.insert_paragraph_before("References", "Front Matter")
    for paragraph in list(document.paragraphs):
        if paragraph.style.name == "Bibliography":
            appendix_start._p.addprevious(paragraph._p)
    if references.text != "References":
        raise RuntimeError("references heading was not retained")
    anchor = next(p for p in document.paragraphs if p.text == "Acknowledgements")
    contents = anchor.insert_paragraph_before("Contents", "Front Matter")
    outline = OxmlElement("w:outlineLvl")
    outline.set(qn("w:val"), "9")
    contents._p.get_or_add_pPr().append(outline)
    _field(anchor.insert_paragraph_before(), r'TOC \o "1-3" \h \z \u')
    for title, entries in (("Figures", figure_entries), ("Tables", table_entries)):
        heading = anchor.insert_paragraph_before(title, "Front Matter")
        outline = OxmlElement("w:outlineLvl")
        outline.set(qn("w:val"), "9")
        heading._p.get_or_add_pPr().append(outline)
        for text, bookmark in entries:
            paragraph = anchor.insert_paragraph_before(text + "\t")
            paragraph.paragraph_format.tab_stops.add_tab_stop(Cm(15), WD_TAB_ALIGNMENT.RIGHT)
            _field(paragraph, "PAGEREF " + bookmark + r" \h")
    update = OxmlElement("w:updateFields")
    update.set(qn("w:val"), "true")
    document.settings.element.append(update)
    document.save(path)
    return {"figures": len(figure_entries), "tables": len(table_entries)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pandoc", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--csl", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=False)
    reference = args.output_dir.resolve() / "official_reference.docx"
    with ZipFile(args.template) as source, ZipFile(reference, "w", ZIP_DEFLATED) as target:
        for item in source.infolist():
            data = source.read(item.filename)
            if item.filename == "[Content_Types].xml":
                data = data.replace(
                    b"wordprocessingml.template.main+xml", b"wordprocessingml.document.main+xml"
                )
            target.writestr(item, data)
    output = args.output_dir.resolve() / "Thesis_Review_20261019.docx"
    subprocess.run(
        [
            str(args.pandoc.resolve()),
            "main.tex",
            "--from=latex",
            "--to=docx",
            "--citeproc",
            "--bibliography=references.bib",
            "--csl=" + str(args.csl.resolve()),
            "--reference-doc=" + str(reference),
            "-M",
            "title=",
            "-M",
            "author=",
            "-M",
            "date=",
            "--output=" + str(output),
        ],
        cwd=Path(__file__).parent,
        check=True,
    )
    counts = format_document(output)
    if counts != {"figures": 5, "tables": 4}:
        raise ValueError(f"canonical caption inventory changed: {counts}; review export numbering")
    print(output)


if __name__ == "__main__":
    main()
