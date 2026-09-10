# NCDP Data Standards

Data standards, metadata schema and templates for the **National Coastal Drone
Programme** — a nationally coordinated archive of UAV coastal survey data,
coordinated by Deakin University and funded by AuScope (NCRIS).

Everything here is the authoritative version. The intake portal at
[ncdp.auscope.org.au](https://ncdp.auscope.org.au) links to this repository
rather than hosting copies, so what you download is always current.

## Contents

| Path | What it is |
|---|---|
| `docs/data-structure.md` | Archive hierarchy and the L0–L4 processing levels |
| `docs/naming-convention.md` | File and directory naming rules |
| `docs/metadata-schema.md` | The 117-attribute survey schema, field by field |
| `docs/qaqc-protocol.md` | What is checked, what blocks, and who resolves it |
| `docs/submitting-data.md` | How to contribute a survey |
| `schema/ncdp-metadata-schema-v3.csv` | The schema as a table |
| `schema/ncdp-metadata-schema-v3.json` | The schema, machine-readable |
| `schema/ncdp-qc-thresholds-v3.json` | Numeric QA/QC thresholds |
| `templates/L0_metadata_template.csv` | Empty CSV with the exact canonical headers |

## Versioning

The schema is versioned independently of this repository. `v3.0` is current.
A change that adds a field is a minor version; one that renames, removes or
reorders a field is a major version, because the archive's existing CSVs are
keyed on those exact header strings.

`schema/` is generated from `portal/schema.py` in the intake portal, which is
the single source of truth. Do not hand-edit the generated files — change
`schema.py` and regenerate, or the portal and the standard will disagree.

## Licence

Documentation and schema: [CC BY 4.0](LICENSE). Survey data itself is licensed
per-survey; see each record's `License` field.

## Contact

National Coastal Drone Programme — ncdp@deakin.edu.au
