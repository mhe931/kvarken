from pathlib import Path

import pytest

docx = pytest.importorskip("docx")

from thesis.export_documents import format_document  # noqa: E402


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
    document.add_picture(str(Path(__file__).parents[1] / "thesis" / "assets" / "uwasa-logo.jpg"))
    document.add_paragraph(
        "Independent Sentinel-2A input, approximately 17.90 hours later. Details."
    )
    for caption in (
        "Selective optical proxy reference: details.",
        "Scene-specific SAR candidate classes, details.",
        "Held-out optical-reference agreement details.",
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
        p.text.startswith(
            "Figure 6.1. Independent Sentinel-2A input, approximately 17.90 hours later"
        )
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
