# Actual eastern-Kvarken satellite application: 19 October 2026

## Scientific status

Actual satellite pixels were acquired and processed. Evaluation is **agreement with a
selective, independent-sensor optical proxy**, not field accuracy. Ice precision is only
23.53%; the candidate map must not be called validated total sea-ice extent.
No CSC processing or authenticated CDSE download occurred.

## Inputs and traceability

- Sentinel-1A IW GRDH VV/VH, ascending orbit 37230 / relative 58, 30 March 2021,
  16:06:12 UTC. RTC item:
  `S1A_IW_GRDH_1SDV_20210330T160559_20210330T160624_037230_046288_rtc`.
- Four Sentinel-2A L2A tiles T34VER/T34VEQ/T34VDR/T34VDQ, orbit R122,
  31 March 2021 10:00:21 UTC; B03/B08/B11 and SCL, baseline N0212.
- ESA WorldCover 2021 v200 N63E021/N63E018/N60E021/N60E018, static mask only.
- [Exact configuration](case_config.json), [captured actual scene metadata](captured_scenes.json),
  [original acquisition manifest](acquisition_manifest.json) and
  [supplemental native-mask manifest](quality_mask_manifest.json).

Acquisition used public Planetary Computer STAC and officially issued temporary SAS tokens.
The collection documentation says an account is required for RTC; anonymous token issuance
and actual TIFF range reads nevertheless succeeded during this run. This is observed access,
not a promise of future availability or an authentication bypass.
Tokens/signed URLs were not persisted. Large input windows remain in ignored
`data/seaice_20261019/`, with 22 original aligned windows and 12 native-class fraction windows.
Checksums identify retained derived windows, **not full original SAFE packages**.
Source licensing/attribution is recorded in [the source-license record](source_licenses.json).

## Method

1. EPSG:4326 rectangle `(20.5,62.8,22.5,63.8)` covers eastern Kvarken, not the whole strait.
2. Align to EPSG:32634, 100 m. Average radar linear gamma-zero before conversion to dB.
   Provider Catalyst supplies RTC; processor version and thermal/border-noise treatment
   were not independently verified.
3. Aggregate **native** WorldCover class indicators. Require water fraction ≥0.999999,
   retain the largest eight-connected component, then erode by a 300 m square radius.
4. Optical B03/B08/B11/SCL and native coverage fractions use one common tile owner.
   Water: SCL6, NIR<0.04, green<0.10. Snow ice: SCL11, NDSI>0.4, green>0.15, NIR>0.10.
   Each label requires ≥99% native SCL class fraction; other cells abstain.
5. Fit VV/VH equal-prior linear discriminant with 5% isotropic covariance shrinkage.
6. Use fixed 10 km checkerboard blocks, excluding 1 km on each block edge.
   Do not tune against held-out results. Report all blocks, even single-class blocks.
7. Persist rasters/maps/results; replay five actual scene records through existing
   provenance, catalog reopening and loopback API checks. This is captured metadata replay.

### Results

Exact [results JSON](results.json) is authoritative; [metrics CSV](metrics.csv) is a compact view.

| Quantity | Recorded result |
|---|---:|
| Valid buffered radar-water support | 5,952.79 km² |
| Held-out water / snow-ice cells | 84,846 / 3,546 |
| Confusion rows reference water/ice, columns candidate water/ice | `[[74641,10205],[406,3140]]` |
| Ordinary / balanced agreement | 88.00% / 88.26% |
| Ice precision / recall / F1 | 23.53% / 88.55% / 37.18% |
| Always-water ordinary / balanced agreement | 95.99% / 50.00% |
| Candidate ice area | 1,219.28 km² |
| Candidate ice without any optical proxy label | 795.91 km² (65.28%) |
| Same held-out support: reference / candidate ice area | 35.46 / 133.45 km² |
| Offset sensitivity −1 / 0 / +1 | 2,313.58 / 1,219.28 / 695.59 km² |

The baseline outperforms ordinary agreement; the model's positive precision is poor.
The 17.90-hour sensor mismatch, selected bright-ice reference, missing optical coverage,
wind-roughened water, incidence effects and annual retrospective mask limit interpretation.
Sensitivity is not a confidence interval. UTM projected cell areas are not geodesic areas.
The 31 held-out blocks are spatial clusters, not 88,392 independent field observations.

### Actual figures

- [Radar VV input](sar_vv.png), [VV/VH pair](sar_input.png).
- [Independent optical input](optical_input.png); grey is missing data.
- [Selective proxy reference](reference.png), [candidate classes](candidate.png),
  [held-out agreement](agreement.png), [overview](classification_validation.png).

All are generated from recorded pixels, not screenshots or image-model synthesis.
Plotting/processing code was AI-assisted; the thesis appendix records representative prompts.
Sources: ESA/Copernicus, Catalyst, Microsoft Planetary Computer and ESA WorldCover.

## Reproduction (PowerShell, repository root)

```powershell
python -m pip install -e ".[dev,science]"
python -m kvarken_eo.case_study --config docs\research\20261019\case_config.json --inputs-dir data\seaice_reproduction --output-dir outputs\seaice_reproduction
python -m kvarken_eo.case_study --inputs-dir data\seaice_reproduction --output-dir outputs\seaice_repeated --reuse-inputs
```

Choose fresh directories. Initial acquisition is networked; reuse validates hashes and is
offline apart from a loopback API probe. Interrupted acquisition can be explicitly resumed
with `--resume-acquisition` and the same configuration. A complete acquisition is immutable.
To extend an old cache that predates native masks, explicitly add `--prepare-quality-masks`
once; interrupted mask preparation verifies receipts before reusing completed windows.

The [local pipeline report](local_pipeline_run.json) is a sanitized copy: private hostname
is redacted and the original report digest is retained. Full originals and georeferenced
rasters remain under ignored `outputs/seaice_20261019_delivery/`.
Executed-source hashes and NumPy/Rasterio/GDAL/Matplotlib/SciPy versions are recorded.
Git was dirty during execution; the old HEAD alone is not the executed science implementation.
Do not expect timing, timestamps or catalog/provenance bytes to reproduce bitwise.

The initial pre-review output is retained separately in ignored storage. Its headline values
are superseded because review identified mixed-tile references, lost small islands and
incomplete single-class reporting. No historical synthetic/fallback artifacts were overwritten.
