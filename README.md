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
| `docs/metadata-schema.md` | The metadata schema: the archive's record format (v4.0) and each attribute |
| `docs/qaqc-protocol.md` | What is checked, what blocks, who resolves it, and the weekly archive audit |
| `docs/submitting-data.md` | How to contribute a survey: the portal wizard, and SFTP for large deliveries |
| `schema/ncdp-metadata-schema-v4.csv` | **Current.** The archive record format, 302 columns in order |
| `schema/ncdp-metadata-schema-v4.json` | The same, machine-readable, plus the 28 `Record …` columns generated on Gadi |
| `schema/ncdp-metadata-schema-v3.csv` / `.json` | Schema v3.1 (119 attributes), superseded by v4.0, kept for existing tools |
| `schema/ncdp-qc-thresholds-v3.json` | Numeric QA/QC thresholds |
| `templates/ancillary_template.csv` | **Use this one.** Empty metadata CSV with the v4.0 columns. One per survey, as `<YYYYMMDD-Location>_ancillary.csv` |
| `templates/L0_metadata_template.csv` | The v3.1 attributes only, kept for existing tools |

## Versioning

The schema is versioned independently of this repository. `v4.0` is current.
A change that adds a field is a minor version; one that renames, removes or
reorders a field is a major version, because the archive's existing CSVs are
keyed on those exact header strings.

`schema/ncdp-metadata-schema-v3.*` were generated from `portal/schema.py` in
the intake portal. Do not hand-edit the generated files.

v4.0 (`schema/ncdp-metadata-schema-v4.*`, `templates/ancillary_template.csv`)
is the archive's record format, taken from the archive itself
(`portal/ancillary_columns.py` in the intake portal, identical to
`gadi/ancillary_columns.py` used on Gadi). Every v3.1 attribute keeps its
name and its provenance; CI checks that the v4.0 CSV, JSON and template list
the same columns and that none of the v3.1 attributes is missing. To
regenerate the template from the intake repository:

```
python3 -c "import csv,sys; from portal.schema import ANCILLARY_FIELDS as c; csv.writer(sys.stdout, lineterminator='\n').writerow(c)" > ../ncdp-standards/templates/ancillary_template.csv
```

## Licence

Documentation and schema: [CC BY 4.0](LICENSE). Survey data itself is licensed
per-survey; see each record's `License` field.

## Contact

National Coastal Drone Programme — ncdp@deakin.edu.au
