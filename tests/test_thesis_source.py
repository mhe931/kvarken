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
