# Archive structure and processing levels

## Directory hierarchy

Surveys are archived at NCI under project `mm91`:

```
/g/data/mm91/admin/<State>/<Location>/<YYYYMMDD-SiteName>/
```

`<State>` is the full name (`Victoria`, not `VIC`). `<Location>` is the stable
place name; `<SiteName>` within the survey directory may be more specific.

## Processing levels

Every survey directory contains level folders. Not all levels exist for every
survey — L4 in particular is produced only where there is a derived product.

| Level | Contents | Produced by |
|---|---|---|
| **L0** | Raw acquisition and everything describing it | Contributor |
| **L1** | Reserved | — |
| **L2** | Analysed products in the **source** CRS | Contributor's processing software |
| **L3** | Cleaned and reprojected to **GDA2020** | Gadi pipeline |
| **L4** | Derived/decision-ready products | Analysis |

### L0 sub-folders

| Folder | Contents |
|---|---|
| `L0Raw` | Raw imagery as captured |
| `L0Planning` | Mission plans, flight path files |
| `L0GCPs` | Ground control point coordinates and observations |
| `L0FlightLogs` | Flight logs, RTK/PPK observation files |
| `L0Ancillary` | Metadata CSV, processing report, QC record |

### L0Ancillary — the submission record

Six artefacts are preserved verbatim. The submission record is part of the
archive, not scaffolding:

| File | Contents |
|---|---|
| `<id>_ancillary.csv` / `L0_metadata.csv` | One row under the canonical headers |
| `metadata.json` | The submitted form, snake_case keys |
| `qc_report.json` | Intake QC verdict under `overall` |
| `report_parsed.json` | Values parsed from the processing report |
| `report_extract.txt` | Raw extracted report text |
| `renames.json` | `{original: standardised}` filename mapping |

## Coordinate reference systems

**Keep the source CRS in L2. Reproject to GDA2020 in L3.** The original is never
overwritten, so a reprojection can always be re-derived or audited. L3 filenames
carry the datum token (see the naming convention).

Vertical CRS is recorded separately from horizontal — an orthomosaic in
GDA2020 / MGA Zone 54 and a DSM on AHD is a normal combination and both must be
stated explicitly.

## What does not go in the archive

Executables and scripts are rejected at intake and never enter the archive.
Personally identifying information should not appear in imagery or metadata;
contributors confirm this at submission.
