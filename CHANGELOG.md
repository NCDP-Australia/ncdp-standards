# Changelog

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
