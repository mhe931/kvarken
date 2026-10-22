import re
from pathlib import Path


def test_abstract_meets_text_and_keyword_guidelines():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "00_abstract.tex"
    manuscript = source.read_text(encoding="utf-8")
    abstract = manuscript.split(r"\textbf{Abstract}\par", 1)[1].split(
        r"\par\medskip\noindent\textbf{Keywords:}", 1
    )[0]

    word_count = len(re.findall(r"\b[\w-]+\b", abstract))
    assert 400 <= word_count <= 450
    assert not re.search(r"(?<!\\)%", abstract)
    specific_results = ("23.53", "88.00", "95.99", "1,219.28", "795.91", "17.90")
    assert not any(result in abstract for result in specific_results)
    assert not re.search(r"\\cite\w*\{", abstract)

    keyword_section = manuscript.split(r"\textbf{Keywords:}", 1)[1]
    keywords = keyword_section.split(r"\endgroup", 1)[0].strip().split(";")
    assert 5 <= len(keywords) <= 8


def test_methodology_reports_four_evaluation_layers():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "03_methodology.tex"
    manuscript = source.read_text(encoding="utf-8")

    assert "Evaluation has four layers." in manuscript


def test_platform_review_covers_requested_services_and_ecosystems():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "02_background.tex"
    manuscript = source.read_text(encoding="utf-8")

    for platform in (
        "Copernicus Data Space Ecosystem",
        "Google Earth Engine",
        "Microsoft Planetary Computer",
        "CREODIAS",
        "openEO",
        "Pangeo",
        "Open Data Cube",
        "NASA",
        "Digital Earth Australia",
        "EarthCODE programme",
        "Planet Insights Platform",
        "UP42",
        "Open Data Registry",
    ):
        assert platform in manuscript

    assert r"\begin{longtable}" in manuscript
    for citation in (
        "cdse-quotas",
        "gee-paper",
        "openeo-paper",
        "pangeo-paper",
        "odc-home",
    ):
        assert citation in manuscript


def test_csc_student_workflow_labels_demonstrated_and_proposed_stages():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "09_education_innovation.tex"
    manuscript = source.read_text(encoding="utf-8")

    for stage in (
        "Student onboarding",
        "CSC environment and access setup",
        "Catalogue discovery",
        "EO Catalogue discovery",
        "Dataset selection",
        "Data retrieval or remote access",
        "Processing and analysis",
        "Provenance recording",
        "Result storage",
        "Reproduction by another student",
    ):
        assert stage in manuscript
    assert "not tested" in manuscript
    assert r"\begin{tikzpicture}" in manuscript


def test_abbreviations_include_used_terms_and_omit_unused_entries():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "00_abbreviations.tex"
    manuscript = source.read_text(encoding="utf-8")

    for acronym in (
        "CSC",
        "ESA",
        "F1",
        "GDAL",
        "GPU",
        "I/O",
        "IP",
        "JSON",
        "NASA",
        "ODC",
        "OData",
        "REST",
        "RQ",
        "S3",
        "SAS",
        "SNAP",
        "SQL",
        "SSH",
        "UTF-8",
    ):
        assert f"{acronym} &" in manuscript
    for unused in ("JSONL", "LDA", "ROI"):
        assert f"{unused} &" not in manuscript
    abbreviations = re.findall(r"(?m)^([A-Za-z0-9/-]+|WGS 84)\s*&", manuscript)
    assert abbreviations == sorted(abbreviations, key=str.casefold)
    assert len(abbreviations) == len(set(abbreviations))


def test_every_bibliography_entry_is_cited_and_every_citation_resolves():
    thesis = Path(__file__).parents[1] / "thesis"
    bibliography = (thesis / "references.bib").read_text(encoding="utf-8")
    entries = set(re.findall(r"@\w+\{([^,]+),", bibliography))
    citations = set()
    for source in thesis.rglob("*.tex"):
        manuscript = source.read_text(encoding="utf-8")
        for group in re.findall(r"\\cite\w*\*?\{([^}]+)\}", manuscript):
            citations.update(key.strip() for key in group.split(","))

    assert citations <= entries
    assert entries <= citations


def test_latex_enables_multipage_comparison_table():
    source = Path(__file__).parents[1] / "thesis" / "main.tex"
    manuscript = source.read_text(encoding="utf-8")

    assert r"\usepackage{longtable}" in manuscript


def test_cdse_bearer_header_example_is_complete_and_uses_placeholder():
    source = Path(__file__).parents[1] / "thesis" / "chapters" / "02_background.tex"
    manuscript = source.read_text(encoding="utf-8")

    assert r"\texttt{Authorization: Bearer <access\_token>}" in manuscript
