# Changelog

## Schema v4.0 — 2026-10: archive record format, layout and audit

v4.0 is the archive's record format. Every v3.1 attribute keeps its name and
provenance; the column order is the archive's, so this is a major version.

- **Archive record format.** `schema/ncdp-metadata-schema-v4.csv/.json` and
  `templates/ancillary_template.csv`: the archive's per-survey metadata file
  (`<YYYYMMDD-Location>_ancillary.csv`), 302 columns. Added to v3.1: the
  per-flight columns `Flight 1…20` (local and UTC start/end, images,
  dewarping, speed, sensor angle, height), `Airframe 1`, `Airframe 2` and
  `End Date`. The 28 `Record …` columns that Gadi generates after them are
  documented in the JSON (`generated_fields`). From 2026-10-02 the portal
  writes new submissions in this format, with the per-flight columns filled
  from the imagery; the archived surveys are brought to the same columns.
  v3.1 files are kept for existing tools.
- **Published archive** at `/g/data/mm91/NCDP/<State>/<Location>/<YYYYMMDD-Location>/`.
- **Raw imagery** sits in `L0/L0Raw/L0RGB/<flight folder>`; a contributor's
  crop polygon is the survey's area of interest (L4).
- **Product names** keep a coordinate system stated in the delivered name
  (`_DSM-GDA94Z54`); Propeller's GeoTIFF export is recognised as the
  orthomosaic.
- **One file per product, at its native resolution.** Resampled copies (e.g.
  `_cleaned_1m` beside `_cleaned`) are not archived; new warning
  `resampled_copy`.
- **Site names** come from the NCDP site list (`sites.csv`).
- **SFTP deliveries** are arranged into the archive layout on Gadi
  (`sftp_restructure.py`), and promoted only when they pass the audit.
- **Weekly archive audit** (`archive_audit.py`) of structure, names, metadata
  and data across the archive; `archive_fix.py` for fixes to existing surveys.
- **Intake QC:** `.dxf` accepted (crop polygons); RINEX and other GNSS logs
  recognised; new warning `l2_looks_cleaned`.
- **Portal wizard:** files first, survey details last; date, site, state,
  airframe and flight table read from the imagery; ground-control files read
  in the browser; coordinate system chosen from lists in the processed-data
  step; the submission box turns amber while handing over and green when the
  page can be closed.

## Schema v3.1

- Raw-only submissions: a contributor may, by arrangement with the NCDP team,
  deliver raw imagery for the programme to process.
- Two attributes appended (orders 118–119), so anything reading the first 117
  columns by position is unaffected:
  - `Submission Type` — `processed` | `raw-only`. What the contributor
    delivered; fixed at submission and never changed.
  - `Processing State` — `processed` | `awaiting-processing` |
    `archived-only`. Where the survey is now; moves to `processed` when the
    programme's products are added to the same survey.
- `Flying Height (m)`, `Image Overlap` and `Image Sidelap` gain form keys:
  entered in the wizard for raw-only submissions, where no report exists to
  parse them from.
- Records without `Submission Type` (everything before 3.1) are `processed`.
  No backfill is required.
- A raw-only survey that has been processed by the programme records the
  contributor as producer and the programme as processor (`Data processing
  person and/or institution`, and STAC `providers` roles).

## Schema v3.0

- 117 canonical attributes.
- Provenance model formalised: manual / report / exif / carried / derived.
- Lineage uses a core-plus-conditionals structure, with optional clauses for
  GCP method and RMSE, ICP accuracy, and GDA2020 reprojection.
- Access levels extended to include `Metadata-Only`.
