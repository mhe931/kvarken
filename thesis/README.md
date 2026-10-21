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

The 22 October source revision compiled successfully in
[GitHub Actions run 67](https://github.com/mhe931/kvarken/actions/runs/39684054300). The
69-page artifact was inspected for contents/list pagination, figure/table numbering,
cross-references and figure rendering. CI uses Carlito as a fallback font. This is a review
build, not an official-template Word export or independently validated PDF/A/accessibility
submission file.

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
python thesis\export_documents.py --pandoc C:\Tools\pandoc.exe --template C:\Downloads\Word_template_ENG_VY_06_2025_5.dotx --csl C:\Downloads\apa.csl --output-dir outputs\thesis_review_20261022
```

This reads the canonical LaTeX, uses official Word styles/page geometry, formats the cover
and abstract, numbers headings/captions, places references before appendices and creates
native TOC/page fields for chapters and sections. Pandoc does not render the TikZ architecture
figure into DOCX, so the exporter replaces its empty placeholder with an editable, styled
six-stage flow diagram. It does not update the remote Google Doc or render Word by itself.

The current 22 October DOCX was generated and structurally checked, including heading styles,
caption numbering, the architecture flow diagram, figure descriptions and document metadata.
Word updated its contents, figure/table lists and page-reference fields, then rendered an
82-page review PDF. The diagram was visually verified at its Chapter 4 caption (page 29);
the contents, scientific figures, evaluation tables and Appendix B were also inspected.
The 19 October Word/PDF candidate was rendered and its historical PDF/A validation is not
evidence for this revised source. PDF/A conformance and current accessibility still need
independent validation; a requested export option is not a validator.

Do not edit an export as a second canonical manuscript. Reapply substantive corrections to
the modular source. The existing shared native Google Doc must retain its ID and permissions; synchronization
must be verified separately from the local export. The 19 October delivery record documents
the previous saved-content mismatch. On 22 October the existing document was reopened under
the author's signed-in account and showed a saved-to-Drive status and prior supervisor edit
attribution. Revised content was not synchronized or verified; do not claim that the shared
document is current.

Both export paths set PDF/document title and author metadata. For Osuva, the metadata
title excludes the cover subtitle. Verify these fields in the actually rendered PDF;
metadata, tags and an archival export option alone do not establish accessibility or
independently validated PDF/A conformance.

The exporter assigns alternative descriptions to the scientific figures, preserving
the distinction between radar candidates, optical proxy agreement and field truth.
When rendering in Word, set each hyperlink's screen tip to its visible text. Word can
still omit descriptions for figure/table page-reference links and omit structure-based
page tab order. Check the actual PDF with an independent validator; a subsequent local
annotation-only remediation must retain full link labels, preserve all page pixels/text
and title/author metadata, and be revalidated for PDF/A. Retain both the original and
remediated bytes and their checksums.

The 19 October final-verification candidate passed local veraPDF 1.30.3 PDF/A-3A validation.
That candidate predates the 22 October source revisions and does not validate a PDF generated
from the current manuscript. No current-source PDF/A or accessibility validation is claimed.
The earlier candidate was not certified PDF/UA-1: its identification requirement remained
unsatisfied, and automated checks did not replace human reading-order, screen-reader and
alternative-text review. See the [delivery report](../docs/THESIS_DELIVERY_REPORT_20261019.md)
for the historical candidate and validation reports.
