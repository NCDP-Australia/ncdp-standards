# Archive structure and processing levels

## Directory hierarchy

Surveys are archived at NCI under project `mm91`, in one of two roots:

```
/g/data/mm91/NCDP/<State>/<Location>/<YYYYMMDD-Location>/    published (Open) surveys, served through THREDDS
/g/data/mm91/admin/<State>/<Location>/<YYYYMMDD-Location>/   everything not public: Restricted, or not yet released
```

`<State>` is the full name (`Victoria`, not `VIC`). `<Location>` is the site's
name from the NCDP site list (`sites.csv` in the metadata registries), written
without spaces or punctuation (`PortFairy`). The survey folder repeats it after
the acquisition date. A new site is added to the site list before its first
survey is archived.

Folders whose name contains `_superseded_` are earlier intakes of a survey that
was later replaced. They are kept for the record but never checked, catalogued
or published.

## Processing levels

Every survey directory contains level folders. Not all levels exist for every
survey — L4 in particular is produced only where there is a derived product.

| Level | Contents | Produced by |
|---|---|---|
| **L0** | Raw, unprocessed data (images, flight logs) and everything describing it | Contributor |
| **L1** | Intermediate processing steps (e.g. thermal or multispectral calibration). Empty for most surveys | Contributor |
| **L2** | Uncleaned processed data (DSM, orthomosaic, point cloud) exactly as the processing software produced it, in the **source** CRS | Contributor's processing software |
| **L3** | Cleaned data (manually edited L2: cropped, noise or water removed), in **GDA2020 + AHD** as Cloud-Optimised GeoTIFF | Contributor, or the Gadi pipeline from L2 |
| **L4** | Model outputs derived from the data (results, indicators), and the survey's area of interest (AoI), including a contributor's crop polygon | Analysis |

Contributors say which level their processed data is by uploading it into the
matching step of the submission wizard. At least one of L2 or L3 is required
for a processed survey.

**How L3 is produced:**

- **Only L2 supplied** — the Gadi pipeline reprojects it to GDA2020 + AHD and
  writes Cloud-Optimised GeoTIFFs into L3.
- **Cleaned data supplied** — that is the survey's L3. If it is already in
  GDA2020 / MGA with AHD heights, the pipeline only converts it to COG and adds
  the datum token to the file name. Otherwise it is archived as delivered and
  held for the NCDP team to reproject before publication.

### L0 sub-folders

```
L0/
  L0Raw/L0RGB/<flight folder>/   raw imagery, one folder per flight, with the drone's MRK/PPK files
  L0GCPs/                        ground control and check points
  L0FlightLogs/                  flight logs, base-station RINEX/PPK
  L0Planning/                    mission plans
  L0Ancillary/                   <YYYYMMDD-Location>_ancillary.csv and the submission record
```

| Folder | Contents |
|---|---|
| `L0Raw/L0RGB/<flight>` | Raw RGB imagery as captured, one sub-folder per flight (e.g. the drone's own `DJI_..._001` folder, or `Flight_01`). Camera file names are never changed. The drone's `.MRK` and PPK files stay with their images |
| `L0Planning` | Mission plans, flight path files |
| `L0GCPs` | Ground control and check-point coordinates (CSV/TXT), including every AeroPoints export for Propeller surveys |
| `L0FlightLogs` | Flight logs, base-station RTK/PPK observation files (RINEX, `.obs`, `.ubx` ...) |
| `L0Ancillary` | Metadata CSV, processing report, QC record |

### L0Ancillary — the submission record

Six artefacts are preserved verbatim. The submission record is part of the
archive, not scaffolding:

| File | Contents |
|---|---|
| `<YYYYMMDD-Location>_ancillary.csv` | The survey's metadata record: one header row and one data row in the archive format (`templates/ancillary_template.csv`). Arrives from the portal as `L0_metadata.csv` |
| `metadata.json` | The submitted form, snake_case keys |
| `qc_report.json` | Intake QC verdict under `overall` |
| `report_parsed.json` | Values parsed from the processing report |
| `report_extract.txt` | Raw extracted report text |
| `renames.json` | `{original: standardised}` filename mapping |

## Coordinate reference systems

**Keep the source CRS in L2. L3 is GDA2020 horizontally and AHD vertically,
as Cloud-Optimised GeoTIFF.** The original is never overwritten, so a
reprojection can always be re-derived or audited. L3 filenames carry the datum
token (see the naming convention).

Vertical CRS is recorded separately from horizontal — an orthomosaic in
GDA2020 / MGA Zone 54 and a DSM on AHD is a normal combination and both must be
stated explicitly.

## What does not go in the archive

Executables and scripts are rejected at intake and never enter the archive.
Personally identifying information should not appear in imagery or metadata;
contributors confirm this at submission. Processing project files (`.psx`,
`.p4d`), zip archives and other files with no place in the levels above are
not archived.

## Keeping the archive consistent

These rules are written down once, in machine-readable form, in
`gadi/archive_spec.py` in the intake repository, and the tools below read them
from there:

- **Portal submissions** are named and arranged at intake (see the naming
  convention) and laid out on Gadi by the QA/QC pipeline.
- **SFTP deliveries** are arranged by `sftp_restructure.py`: partners upload one
  folder per survey with its metadata CSV, and the tool sets the survey id,
  builds this layout, names the products and keeps the partner's original CSV
  beside the archive one. Surveys move into the archive only when they pass
  the audit.
- **A weekly audit** (`archive_audit.py`) checks every survey in both roots:
  folder names and places, this layout, the metadata record (one row; its
  Project Identifier, Date, Location, Region and Access Level agree with where
  the survey sits), raw imagery, orthomosaic and DSM, product names, duplicate
  ids, site records and the catalogue. It changes nothing; its report lists
  what needs fixing.
