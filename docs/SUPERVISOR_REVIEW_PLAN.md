# Supervisor review plan: 22 October 2026

## Current review checkpoint

On 22 October, the user supplied a detailed revision brief attributed to Professor Ali Nadir
Arslan's latest comments. The original email or annotated manuscript was not present in the
repository, so this plan records the supplied brief without inventing an email date or
quoting unseen comments. The [review-response matrix](THESIS_REVIEW_RESPONSE_20261022.md)
maps that brief to the source; its page references are historical until the current source
has been rebuilt.

GitHub Actions run 67 compiled an earlier 22 October source revision with XeLaTeX/Biber and
uploaded a 69-page CI review PDF. The contents/list pages, numbering, cross-reference markers,
Figure 4.1, the five scientific figures and Appendix B were inspected for that revision.
Since then, the branch has added the comparative platform review, a CSC student-workflow
diagram and evidence table, and abbreviation updates. These changes have not yet been compiled
or paginated. Python and the TeX toolchain are unavailable in the current workspace; static
source checks pass, but they do not replace the test suite or a fresh build.

Edge Personal opened the existing Google Doc and displayed a saved-to-Drive status and a
recent author edit attribution. After refresh, the content area rendered blank. No text or
graphics were edited or verified, no replacement Doc was created, and the supervisor's
access has not been confirmed.

The existing CSC demonstration remains the verified five-record metadata/provenance/catalog/
regional-query/loopback-API prototype. Raster processing remains local. No new acquisition,
CSC deployment, Turnitin submission, Osuva submission or email was made during this checkpoint.

## Received requirements and present status

The user supplied Professor Ali Nadir Arslan's feedback: infrastructure description alone
is insufficient; demonstrate one actual satellite application with workflow in Chapter 5,
maps/results/evaluation in Chapter 6. The user also supplied his recommendation for an
actual CSC run, preferably cPouta. Original email dates and mail delivery are not verified
here. Cem Özcan is proposed as reviewer; acceptance is not confirmed.

An authentic Sentinel-1 case with independent Sentinel-2 proxy comparison has run locally.
Its classifier has low positive precision and must not be called validated total ice extent.
CSC metadata/provenance/catalog/API execution is now verified, with unchanged scientific
classifier results. The shared Google Doc has not been synchronized.

Final verification after the author's reported transfer still exported the old shared
42-page manuscript, without current scientific/CSC markers. A reload and cache-bypassed
request confirmed the mismatch; author clarification/transfer is necessary.
The [current candidate](../outputs/thesis_verified_review_20261019/Thesis_Submission_Candidate_20261019.pdf)
passes independent local veraPDF PDF/A-3A validation. Figure alternative text, link
descriptions and tab order were improved without changing visible pages. Full PDF/UA-1
conformance is not claimed: its identification requirement fails, and human
reading-order/screen-reader checks and scientific author review remain open.
See [the evidence](research/20261019/README.md) and
[the full delivery report and email draft](THESIS_DELIVERY_REPORT_20261019.md).

## Immediate sequence

1. Complete personal author review of the revised manuscript, figures, references and disclosure.
2. MyCSC and Google browser access recovered on 19 October. Project **2021696** has
   cPouta enabled and 30,000 Cloud BUs. Actual remote replay completed at **17:29:43 UTC**,
   exit zero; output/source hashes and local/remote validation match.
   Review the [recorded demonstration](CSC_DEMONSTRATION.md) and
   [evidence](research/20261019/csc_execution_evidence.json). Temporary VMs/IP were released.
3. The existing Google Doc opened under Edge Personal but rendered blank after refresh on
   22 October. Preserve the same document ID and permissions when synchronization is possible,
   and verify saved content by reopening it.
4. Email the revised DOCX/PDF to **Dear Professor Arslan,**, signed **Däniel**, explicitly
   identifying the scientific limits and whether CSC execution has actually been completed.
   The report contains a draft only; no email was sent and no meeting is requested.
5. Obtain written scientific/structural feedback. Do not infer approval from software tests,
   document exports or the existence of a shared link.
6. Obtain supervisor authorization for Turnitin, then authorization for Osuva after the
   report has been reviewed. Follow the programme/Education Services instructions.

## Deadline and administrative boundary

The user's urgent working deadline is **23 October 2026** for the intended December graduation.
The individual submission/assessment deadline could not be publicly verified; the relevant
Jolla timetable requires authenticated access. Confirm it immediately with the supervisor
and Education Services. The public 18 December graduation event is not proof of an individual
degree-completion deadline. No graduation, reviewer approval or submission is guaranteed.

The October--December proposal recorded at the 5 October checkpoint is superseded.
Actual feedback received after this revision must be recorded with its date and source;
do not record drafted correspondence as sent.

## Canonical document

Repository source: [the modular manuscript](../thesis/main.tex).
Existing shared native Google Doc (not synchronized or verified on 22 October):
https://docs.google.com/document/d/1oq5FtrWh4Yb3yd2NBtUS0OgNO2jtuDUMqzVz0085lEE/edit

Do not create a replacement Doc or change supervisor permissions.
