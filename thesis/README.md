# Canonical manuscript and review exports

The canonical content is [main.tex](main.tex), the modular chapters and [references.bib](references.bib).
Exports are **review drafts**, not supervisor approval or university acceptance.
See [the delivery report](../docs/THESIS_DELIVERY_REPORT_20261019.md).

## PDF source build

The manuscript uses Calibri when installed and Carlito otherwise. Local authoritative review
exports used installed Calibri; CI uses Carlito for a reproducible smoke build, not proof of
official-font compliance. Margins are 3 cm, body 12 pt/1.5 spacing, abstract 11 pt/single.
Arabic numbering is continuous from counted/unprinted cover 1 to abstract 2.
The bibliography uses BibLaTeX APA and Biber.

With TeX Live:

```powershell
Set-Location thesis
xelatex -interaction=nonstopmode -halt-on-error main.tex
biber main
xelatex -interaction=nonstopmode -halt-on-error main.tex
xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Local validation also used Tectonic 0.17.0 with Biber 2.17 on `PATH` in the same process.
Its bundle uses BibLaTeX 3.17; choose a matching Biber version rather than editing BCF versions.
Generated PDFs/auxiliary files are not committed.

## Official-template Word export

Sources:

- [University June 2025 DOTX](https://www.uwasa.fi/sites/default/files/2025-06/Word_template_ENG_VY_06_2025_5.dotx)
- [August 2026 guidelines](https://www.uwasa.fi/sites/default/files/2026-08/Writing_Guidelines_ENG_VY_08_2026_0.docx)
- [APA CSL](https://github.com/citation-style-language/styles/blob/master/apa.csl)

The logo in [assets/uwasa-logo.jpg](assets/uwasa-logo.jpg) is extracted from image1 in the
official template and cropped only to remove white margins. It is university identity,
not an AI-generated illustration; do not reuse it to imply university approval.

Install `.[documents]`, provide the downloaded official DOTX, APA CSL and Pandoc executable,
and choose a new output directory:

```powershell
python -m pip install -e ".[documents]"
python thesis\export_documents.py --pandoc C:\Tools\pandoc.exe --template C:\Downloads\Word_template_ENG_VY_06_2025_5.dotx --csl C:\Downloads\apa.csl --output-dir outputs\new_thesis_review
```

This reads the canonical LaTeX, uses official Word styles/page geometry, formats the cover
and abstract, numbers headings/captions, places references before appendices and creates
native TOC/page fields. It does not update the remote Google Doc or render Word by itself.
Open the result in Word, update fields/contents and repaginate before PDF export. Actual
Word 16.0 rendering and PDF/A export were exercised locally. PDF/A conformance and final
accessibility still need independent validation; a requested export option is not a validator.

Do not edit an export as a second canonical manuscript. Reapply substantive corrections to
the modular source. The existing shared native Google Doc must retain its ID and permissions;
synchronization must be verified separately from the local export. Browser access recovered;
the old shared manuscript was read successfully but lacks the revised scientific results.

Both export paths set PDF/document title and author metadata. For Osuva, the metadata
title excludes the cover subtitle. Verify these fields in the actually rendered PDF;
metadata, tags and an archival export option alone do not establish accessibility or
independently validated PDF/A conformance.

The exporter assigns alternative descriptions to the five scientific maps, preserving
the distinction between radar candidates, optical proxy agreement and field truth.
When rendering in Word, set each hyperlink's screen tip to its visible text. Word can
still omit descriptions for figure/table page-reference links and omit structure-based
page tab order. Check the actual PDF with an independent validator; a subsequent local
annotation-only remediation must retain full link labels, preserve all page pixels/text
and title/author metadata, and be revalidated for PDF/A. Retain both the original and
remediated bytes and their checksums.

The final-verification candidate passed local veraPDF 1.30.3 PDF/A-3A validation. It is
not certified PDF/UA-1: the identification requirement remains unsatisfied, and automated
checks cannot replace human reading-order, screen-reader and alternative-text review.
See the [delivery report](../docs/THESIS_DELIVERY_REPORT_20261019.md) for the exact candidate,
validation reports and remaining approvals.
