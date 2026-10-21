from pathlib import Path

import pytest

docx = pytest.importorskip("docx")

from thesis.export_documents import (  # noqa: E402
    _insert_architecture_diagram,
    format_document,
)


def test_document_has_continuous_pages_numbered_chapters_and_references_before_appendix(tmp_path):
    path = tmp_path / "review.docx"
    document = docx.Document()
    document.add_paragraph("Däniel Ebrahimzadeh Esfahani")
    document.add_paragraph("Vaasa 2026")
    document.add_paragraph("UNIVERSITY OF VAASA")
    document.add_table(rows=1, cols=2)
    document.add_paragraph("Abstract")
    document.add_paragraph("Abstract text.")
    document.add_paragraph("Keywords: Earth Observation")
    document.add_heading("Acknowledgements", 1)
    document.add_paragraph("I would like to thank my parents for their support.")
    document.add_heading("Abbreviations", 1)
    abbreviations = document.add_table(rows=2, cols=2)
    abbreviations.cell(0, 0).text = "ACID"
    abbreviations.cell(0, 1).text = "Atomicity, Consistency, Isolation, and Durability"
    abbreviations.cell(1, 0).text = "API"
    abbreviations.cell(1, 1).text = "Application Programming Interface"
    abbreviations.rows[0]._tr.get_or_add_trPr().append(docx.oxml.OxmlElement("w:tblHeader"))
    document.add_heading("Introduction", 1)
    document.add_heading("Motivation", 2)
    document.add_heading("System Architecture", 1)
    document.add_paragraph(
        "Provider-to-application architecture and subsystem boundaries. The metadata path "
        "is distinct from the raster case-study path."
    )
    document.add_heading("Evaluation", 1)
    document.add_picture(str(Path(__file__).parents[1] / "thesis" / "assets" / "uwasa-logo.jpg"))
    document.add_paragraph(
        "Sentinel-2A Level-2A false-colour observation from 31 March 2021, "
        "approximately 17.90 hours later. Details."
    )
    for caption in (
        "Selective Sentinel-2 optical proxy labels for dark water and snow-covered ice.",
        "Scene-specific SAR candidate classes derived from Sentinel-1 observations.",
        "Held-out agreement between thesis-derived radar candidates and optical labels.",
    ):
        document.add_picture(
            str(Path(__file__).parents[1] / "thesis" / "assets" / "uwasa-logo.jpg")
        )
        document.add_paragraph(caption)
    document.add_paragraph("Research questions, primary evidence, and claim boundaries.")
    document.add_paragraph("Held-out confusion matrix. Details.")
    document.add_heading("Disclosure of AI-Assisted Work", 1)
    document.add_paragraph("AI disclosure.")
    document.styles.add_style("Bibliography", 1)
    document.add_paragraph("Verified source.", style="Bibliography")
    empty_figure_table = docx.oxml.OxmlElement("w:tbl")
    table_properties = docx.oxml.OxmlElement("w:tblPr")
    table_style = docx.oxml.OxmlElement("w:tblStyle")
    table_style.set(docx.oxml.ns.qn("w:val"), "FigureTable")
    table_properties.append(table_style)
    empty_figure_table.append(table_properties)
    empty_figure_table.append(docx.oxml.OxmlElement("w:tblGrid"))
    document._element.body.append(empty_figure_table)
    document.save(path)
    format_document(path)
    saved = docx.Document(path)
    assert saved.core_properties.title == (
        "Design and Implementation of a Hybrid Earth Observation Data Infrastructure"
    )
    assert saved.core_properties.author == "Däniel Ebrahimzadeh Esfahani"
    assert "17.90 hours" in saved.inline_shapes[0]._inline.docPr.get("descr", "")
    assert "not field ground truth" in saved.inline_shapes[0]._inline.docPr.get("descr", "")
    descriptions = [shape._inline.docPr.get("descr", "") for shape in saved.inline_shapes]
    assert "Grey areas lack usable coverage" in descriptions[0]
    assert "pale-cyan snow-ice" in descriptions[1]
    assert "grey water without a label and white excluded" in descriptions[1]
    assert "pale-cyan ice candidates" in descriptions[2]
    assert "white areas are excluded" in descriptions[2]
    assert "Green cells agree and red cells disagree" in descriptions[3]
    text = [paragraph.text for paragraph in saved.paragraphs]
    assert "1  Introduction" in text
    assert "1.1  Motivation" in text
    assert any(
        p.text.startswith("Figure 4.1. Provider-to-application architecture")
        for p in saved.paragraphs
    )
    assert (
        text.index("References")
        < text.index("Verified source.")
        < text.index("A  Disclosure of AI-Assisted Work")
    )
    assert not any(p.text == "Abstract" and p.style.name == "Heading 1" for p in saved.paragraphs)
    assert saved.sections[0].different_first_page_header_footer
    assert "PAGE" in saved.sections[0].header._element.xml
    assert saved.styles["Normal"].font.name == "Calibri"
    assert saved.styles["Normal"].font.size.pt == 12
    assert any(
        p.text.startswith("Figure 6.1. Sentinel-2A Level-2A false-colour observation")
        and "PAGEREF" in p._p.xml
        for p in saved.paragraphs
    )
    assert next(
        p
        for p in saved.paragraphs
        if p.text.startswith("Table 6.1. Held-out confusion") and "PAGEREF" not in p._p.xml
    ).paragraph_format.keep_with_next
    assert not saved.tables[1].rows[0]._tr.xpath("./w:trPr/w:tblHeader")
    assert saved.tables[1].cell(1, 1).paragraphs[0].paragraph_format.line_spacing == 1


def test_document_formatting_rejects_a_missing_abstract(tmp_path):
    path = tmp_path / "invalid.docx"
    docx.Document().save(path)
    with pytest.raises(ValueError, match="abstract"):
        format_document(path)


def test_document_describes_the_cover_logo(tmp_path):
    path = tmp_path / "cover.docx"
    document = docx.Document()
    document.add_picture(str(Path(__file__).parents[1] / "thesis" / "assets" / "uwasa-logo.jpg"))
    document.add_paragraph("UNIVERSITY OF VAASA")
    document.add_paragraph("Keywords: Earth Observation")
    document.add_heading("Acknowledgements", 1)
    document.add_heading("Disclosure of AI-Assisted Work", 1)
    document.save(path)

    format_document(path)

    saved = docx.Document(path)
    assert saved.inline_shapes[0]._inline.docPr.get("descr") == "University of Vaasa logo"


def test_architecture_diagram_replaces_the_empty_pandoc_placeholder(tmp_path):
    path = tmp_path / "architecture.docx"
    document = docx.Document()
    document.add_paragraph("The architecture is shown in Figure 4.1.")
    document.add_paragraph("Figure 4.1. Provider-to-application architecture\tUpdate field")
    document.add_paragraph(
        "Figure 4.1. Provider-to-application architecture and subsystem boundaries."
    )
    placeholder = document.add_table(rows=1, cols=1)
    placeholder._tbl.remove(placeholder.rows[0]._tr)
    document.add_paragraph("Appendix content follows.")
    document.save(path)

    _insert_architecture_diagram(path)

    saved = docx.Document(path)
    diagram = next(table for table in saved.tables if len(table.rows) == 11)
    assert len(diagram.rows) == 11
    text = [row.cells[0].text for row in diagram.rows]
    assert text[0].startswith("Provider\n")
    assert text[1] == "↓"
    assert "EOScene" in text[4]
    assert text[9] == "↓"
    assert text[10].startswith("Scientific application\n")
    body = list(saved.element.body)
    assert body.index(diagram._tbl) < body.index(
        next(
            p._p
            for p in saved.paragraphs
            if p.text.startswith("Figure 4.1. ") and "Update field" not in p.text
        )
    )
    assert body.index(diagram._tbl) < body.index(
        next(p._p for p in saved.paragraphs if p.text == "Appendix content follows.")
    )
