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
| `docs/metadata-schema.md` | The survey attributes contributors fill, field by field (schema v3.1) |
| `docs/qaqc-protocol.md` | What is checked, what blocks, who resolves it, and the weekly archive audit |
| `docs/submitting-data.md` | How to contribute a survey: the portal wizard, and SFTP for large deliveries |
| `schema/ncdp-metadata-schema-v3.csv` | The schema as a table |
| `schema/ncdp-metadata-schema-v3.json` | The schema, machine-readable |
| `schema/ncdp-qc-thresholds-v3.json` | Numeric QA/QC thresholds |
| `templates/ancillary_template.csv` | **Use this one.** Empty metadata CSV in the archive's record format: every schema attribute plus the per-flight, sensor, ground-control and product-detail columns (302 columns). One per survey, as `<YYYYMMDD-Location>_ancillary.csv` |
| `templates/L0_metadata_template.csv` | The schema v3.1 attributes only (119 columns), kept for existing tools |

## Versioning

The schema is versioned independently of this repository. `v3.1` is current.
A change that adds a field is a minor version; one that renames, removes or
reorders a field is a major version, because the archive's existing CSVs are
keyed on those exact header strings.

`schema/` is generated from `portal/schema.py` in the intake portal, which is
the single source of truth. Do not hand-edit the generated files — change
`schema.py` and regenerate, or the portal and the standard will disagree.

`templates/ancillary_template.csv` is the archive's record format, taken from
the archive itself (`portal/ancillary_columns.py` in the intake portal). It
contains every schema attribute under the same name, so the schema files above
still describe each of its fields; the extra columns are filled by NCDP from
the files. To regenerate it from the intake repository:

```
python3 -c "import csv,sys; from portal.schema import ANCILLARY_FIELDS as c; csv.writer(sys.stdout, lineterminator='\n').writerow(c)" > ../ncdp-standards/templates/ancillary_template.csv
```

## Licence

Documentation and schema: [CC BY 4.0](LICENSE). Survey data itself is licensed
per-survey; see each record's `License` field.

## Contact

National Coastal Drone Programme — ncdp@deakin.edu.au
