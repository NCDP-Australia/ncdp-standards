# Changelog

## 2026-10 — archive record format, layout and audit

No schema attribute is renamed, removed or reordered, so schema v3.1 stands.

- **Archive record format.** New `templates/ancillary_template.csv`: the
  archive's per-survey metadata file (`<YYYYMMDD-Location>_ancillary.csv`),
  302 columns. It holds every v3.1 attribute under the same name, plus the
  archive's per-flight (`Flight 1…20 …`), sensor, ground-control EPSG and
  product-detail columns and `End Date`. From 2026-10-02 the portal writes new
  submissions in this format, so new surveys and archived ones share one header;
  the per-flight columns are filled from the imagery. The 119-column
  `L0_metadata_template.csv` is kept for existing tools.
- **Two archive roots.** Open surveys are published from `/g/data/mm91/NCDP`;
  everything else stays in `/g/data/mm91/admin`.
- **Raw imagery** sits in `L0/L0Raw/L0RGB/<flight folder>`; a contributor's
  crop polygon is the survey's area of interest (L4).
- **Product names** keep a coordinate system or ground resolution stated in
  the delivered name (`_DSM-GDA94Z54_1m`); Propeller's GeoTIFF export is
  recognised as the orthomosaic.
- **Site names** come from the NCDP site list (`sites.csv`).
- **SFTP deliveries** are arranged into the archive layout on Gadi
  (`sftp_restructure.py`), and promoted only when they pass the audit.
- **Weekly archive audit** (`archive_audit.py`) of structure, names, metadata
  and data across both roots.
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
