# Changelog

Every revision of the NCDP Data Standards and Procedures, newest first. From revision 5.01 the
documents are versioned as one set (`MAJOR.YYx`, see README); earlier entries are the metadata schema
releases, whose major number the set continues.

## Unreleased

(Add changes here; rename to the revision when it is released.)

## Revision 5.01 — 2026-10-28: published wiki, intake triage, indicator methods

**Minor revision** (procedures changed; schema unchanged at v5.0).

- **Field Manual on the wiki** (`field-manual.md`, converted from the Word original with
  `Scripts/docx_to_markdown.py`): equipment, mission planning (grid, linear and oblique missions on the
  DJI Matrice 4 Enterprise), conducting a survey, data upload, additional capture techniques, incident
  reporting, the appendix checklists, logs, risk assessment and the quick reference sheet.
- **Versioning and publication.** The documents are versioned as one set (`5.01`), published as a
  locked revision on the GitHub Wiki with a PDF of every page, and released on Zenodo with a DOI per
  revision (`publish.yaml`, `Scripts/publish_to_wiki.py`, `.github/workflows/release.yml`).
- **QA/QC: who acts on a finding** (`qaqc-protocol.md`, `submitting-data.md`). Findings are grouped
  as *fix* (contributor; held), *check* (contributor; archived), *information* and *team*. The
  contributor's email lists only their part; the team gets every finding. Admin → Intake → Actions
  lets the team accept a finding or ask the contributor about it.
- **QA/QC: unrecognised file types no longer block.** `known_types` is a warning for the team; they
  travel with the survey unless removed. Executables and scripts still block.
- **QA/QC: new check `report_empty`.** A processing report that is only empty files counts as missing
  (contributor to check).
- **New page: coastal change indicators** (`indicators.md`, provisional): P1/P2/S4 basis, S1/S2/S5/S6,
  C1/C2/C4/C5, the **reference stretch** for record-wide values (core transects valid on ≥ 60 % of
  dates, runs ≥ 100 m, dates covering ≥ 80 %), the D1 erosion warning, D2 hotspots with the ends-and-gaps
  rule (90 m window ≥ 75 % filled, ≥ 90 m from ends and gaps) and per-location **set-aside stretches**
  (river mouths), and the site reports.

## Schema v5.0 — 2026-10-14: per-flight values packed

- **Per-flight columns packed.** The 180 columns `Flight 1…20` × nine fields
  (local and UTC start/end, images, dewarping, speed, sensor angle, height)
  are now nine columns, `Flight <field>`, each holding one value per flight in
  flight order, separated by `; ` (`Flight Images` = `412; 398; 405`). The
  record goes from 302 to 131 columns (159 with the generated `Record …`
  columns), and the 20-flight limit is gone. Nothing else changed: every
  other column keeps its name, provenance and order.
- In the Victorian archive about three quarters of the old per-flight cells
  were empty (surveys average four to seven flights), and one survey already
  used all 20 slots.
- `schema/ncdp-metadata-schema-v5.csv/.json` and
  `templates/ancillary_template.csv` updated; v4.0 files kept. The archive's
  CSVs were converted on Gadi (`pack_flights.py`); the NCDP tools read both
  layouts.

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
