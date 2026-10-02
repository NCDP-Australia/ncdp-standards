# NCDP QA/QC protocol

One protocol, two engines. The Nirin VM validates a submission's *content* at
the moment it is offered; Gadi validates that it *arrived intact* and that the
pixels agree with what the processing report claims. Both engines emit the same
check shape — `{id, category, label, status, detail}` rolling up as
any `fail` → `fail`, any `warn` → `review`, else `pass` — so a survey's two QC
records concatenate into one continuous audit trail with no translation layer.

This document is the operator-facing statement of that protocol: what is
checked, what blocks, who resolves it, and where the record lives.

---

## Governing principle

**Only things that make data unusable or unfindable block.** Everything else
flags and flows through.

A block means a human must act before the data can be archived. Blocking on
something recoverable — a missing okta reading, an unparsable scanned PDF —
turns the QA gate into an obstacle that operators route around, and routed-around
gates protect nothing. The cost of a permissive gate is a review queue; the cost
of a strict one is partners who stop submitting.

Concretely, five things block at intake:

| Blocks | Why |
|---|---|
| Missing critical metadata | The survey can't be found, attributed or licensed |
| Invalid contact email | Nobody to resolve a later problem with |
| Executable/script files | Security — never enters the archive |
| Unrecognised file types | Unknown content shouldn't be archived blind |
| Truncated transfer (Gadi) | The data is simply not there |

Everything else — thresholds, missing products, empty buckets, resolution
disagreements, missing overviews — is a warning.

---

## Stage 0 — Client side (browser)

No gating. The wizard collects metadata and offers a report-first step that
pre-fills fields from the Propeller PDF. Deliberately no client-side validation
beyond HTML `required` attributes: the server is the only authority, and a
client that gates would just have to be re-checked anyway.

---

## Stage 1 — Intake QC (VM, `portal/qc.py`)

Runs at `POST /submit`, after tus uploads land and before anything moves toward
gdata. Operates on the three-bucket staging layout:

```
<submission>/raw/          raw imagery (folder or zip)
<submission>/report/*.pdf  processing report
<submission>/products/     ortho / DSM / point cloud
```

### Bucket and file checks

| Check | Verdict | Note |
|---|---|---|
| `bucket_raw` / `bucket_report` / `bucket_products` | warn if empty | All three expected, none mandatory |
| `prod_ortho`, `prod_dsm`, `prod_pointcloud` | warn if absent | Detected by filename pattern |
| `prod_tif_ext` | warn | Ortho/DSM should be GeoTIFF |
| `report_pdf` | warn | Report should be `.pdf` |
| `raw_imagery` | warn | `.jpg`/`.tif` expected in raw |
| `image_count` | warn | Uploaded count vs report count, 2% or 2-image slack |
| `no_empty` | warn | Zero-byte files |
| `l2_looks_cleaned` | warn | Files named "cleaned" uploaded as L2 (original); they belong in L3. Archived as uploaded |
| `resampled_copy` | warn | A resampled copy beside the native-resolution product (e.g. `_1m`): not archived, only the native file is kept |
| **`no_executables`** | **fail** | `.exe .dll .bat .ps1 .hta .lnk .so .iso .docm .xlsm` and others |
| **`known_types`** | **fail** | Anything outside the allowlist — held, not discarded. The allowlist includes imagery, GeoTIFF/LAS/LAZ, reports, CSV/TXT, KML/KMZ, shapefiles, GeoJSON, DXF (crop polygons) and GNSS logs (RINEX `.obs`/`.26o`/`.rnx`/`.crx`, `.ubx`, `.sbf`, `.t02`/`.t04`, `.rtcm`, `.MRK`) |

The type check is an **allowlist**, not a denylist. A denylist can only block
what was thought of in advance; inverting it means an unexpected extension gets
a human look rather than a free pass. Extensionless files pass, since raw flight
logs commonly have none.

### Metadata checks

**Critical (block):** `site_name`, `region`, `acquisition_date`,
`point_of_contact`, `access_level`. Plus `meta_email` — the contact address must
parse.

**Recommended (warn):** purpose, description, license, organisation, airframe,
airframe type, pilot in command, camera angle, UTC offset, cloud cover okta,
wind speed, GCPs used, processing software, coordinate system.

### Threshold checks

Values are taken from the parsed report where available, falling back to
operator-entered metadata, else `na`. **A breach warns, it does not block** — a
survey that misses a target is still a survey worth archiving, flagged so the
team can decide.

Thresholds live in `portal/qc_thresholds.json` and are read at submission time,
so editing that file changes the protocol without a code deploy:

| Threshold | Value | Direction |
|---|---|---|
| `min_source_images` | 100 | floor |
| `target_gsd_max_cm` | 5 | limit |
| `bundle_adj_total_error_max_m` | 0.5 | limit |
| `bundle_adj_z_error_max_m` | 0.3 | limit |
| `bundle_adj_xy_error_max_m` | 0.3 | limit |
| `gcp_rms_total_error_max_m` | 0.5 | limit |
| `gcp_max_individual_error_m` | 0.3 | limit |
| `gcp_dem_total_error_max_m` | 0.5 | limit |
| `max_dsm_nodata_voids_pct` | 5 | limit |
| `min_point_cloud_density_ppm2` | 50 | floor |
| `max_poor_quality_images` | 5 | limit |
| `max_fair_quality_images_pct` | 15 | limit |
| `max_unaligned_images` | 0 | limit |

### Naming

`qc.standardise_products()` renames products to
`YYYYMMDD_Site_Product[-CRS].ext` before promotion and writes `renames.json`.
A coordinate system stated in the delivered name is kept
(`..._DSM_GDA94_Z54_AHD09_cleaned.tif` → `..._DSM-GDA94Z54.tif`), and
Propeller's `..._GeoTIFF_...` export is recognised as the orthomosaic. One file
per product: a resampled copy delivered beside the native-resolution product
(`..._cleaned_1m`) is not archived, and is listed in `not_archived.json`.
Naming is therefore correct by construction, and **Gadi must not rename
again** — doing so would break the audit trail. Only the L2→L3 reprojection
stage touches names, appending the datum token.

### Routing

- `fail` → `/data/review/<user>/<stamp>-<id>`, operator and team emailed, item
  appears in the admin review queue
- `review` (warnings only) or `pass` → `/data/landing/portal/...`, into the AV
  gate

---

## Stage 2 — Security gate (VM, ClamAV)

Not QA — a security control, and independent of the QC verdict. `av-sweep.sh`
scans everything settled in the landing zone for at least 2 minutes. Clean files
move to `/data/clean`; infected files move to `/data/quarantine` and never
reach gdata.

Two properties worth knowing:

- **Fail-safe by construction.** The promoter only ever reads `/data/clean`, so
  anything the sweep hasn't cleared simply never leaves the VM.
- **A release is a QC override, never a security bypass.** Releasing an item
  from the review queue puts it back into the landing zone, so it still passes
  through the scan.

`clamd` is tuned to 25G `MaxFileSize`/`MaxScanSize`/`StreamMaxLength`. The
defaults (25M/100M) would have silently skipped every survey raster while still
reporting clean — verify this after any VM rebuild.

---

## Stage 3 — Archive QA/QC (Gadi, `ncdp-gadi-qaqc`)

Seven independently runnable stages, resumable, with a per-submission ledger.
Passed stages skip on re-run, so a job killed by walltime resumes where it
stopped.

| Stage | Does | Blocks on |
|---|---|---|
| 1 `verify` | Generates the manifest the transfer lacks (sha256 for products and sidecars, size/mtime for bulk imagery); corner-read truncation test | Truncated transfer, missing bucket |
| 2 `scrape` | Report → `report_values.json`, reusing the portal's own parse | — |
| 3 `structure` | Builds the L0–L3 tree by hardlink (same filesystem, so no extra quota) | Unresolvable location |
| 4 `rasterqc` | Pixels vs report: GSD, extent, nodata voids, CRS, overviews; derives footprint | Undefined CRS |
| 5 `reproject` | Drives `L2_to_L3.py` — GDA2020, datum token appended | — |
| — *promote* | `os.rename` into the published hierarchy: atomic, so a survey never appears half-built | — |
| 6 `metadata` | Completes the canonical row (boundary corners, area, per-product GSD/EPSG, vertical CRS, RMSE, verdict) into `L0Ancillary/L0_metadata.csv` **and** the master catalogue CSV | — |
| 7 `stac` | Discovery record with `ncdp:` properties | — |

Two conventions carried from the design:

**Measured beats reported.** Where stage 4 reads a value from the pixels it
wins; the reported value is kept alongside as `*_reported` so the disagreement
survives into the catalogue rather than being quietly resolved.

**Incoming is read-only in spirit.** Nothing is written back into a submission
directory; derived artefacts go to `work/<id>/_derived/`.

---

## SFTP deliveries

Bulk deliveries over SFTP get Stage 2 and Stage 3 but not the portal's Stage 1:
there is no metadata form or bucket check. In its place, on Gadi:

1. **Restructure** (`sftp_restructure.py`). Partners upload one folder per
   survey with its metadata CSV. The tool works out each survey's id, state,
   location (from the NCDP site list) and access level, builds the archive
   layout, names the products as above (resampled copies stay behind), and
   writes the metadata CSV with the archive's full set of columns and the
   survey's identity (the partner's original is kept). A survey with an unknown site
   or no date is **blocked** until fixed; files it cannot place stay in the
   holding folder. Plan (dry run) → apply into staging (with undo) → promote.
2. **Promotion is gated by the archive audit** (next section): only staged
   surveys without errors move into the archive.
3. The Gadi QA/QC pipeline (raster checks, reprojection) is then run over the
   promoted surveys.

SFTP accounts still go to institutional partners only. See the NCDP SFTP guide
and `SFTP-AND-DRAIN.md`.

---

## Stage 4 — Weekly archive audit (Gadi, `archive_audit.py`)

Read-only, every week (`archive_audit.pbs`, queued with `qsub -a`), over the
whole archive and the SFTP staging area. It checks, per survey: folder name and
place; the archive layout (`L0/L0Raw/L0RGB/<flight>`,
`L0/L0Ancillary/<id>_ancillary.csv`, L2, L3, L4); the metadata record (one row,
with the archive's full set of columns (schema v4.0); Project Identifier, Date,
Location, Region and Access Level agree with where the survey sits); raw
imagery, orthomosaic and DSM; product names and resampled copies. Across the
archive: duplicate survey ids, site records that count the wrong number of
surveys, and catalogue entries with no survey (or surveys missing from the
catalogue).

| Severity | Meaning | Examples |
|---|---|---|
| error | Breaks the catalogue, the records or publication | wrong place or name, missing or contradicting metadata, a survey stored where its access level does not allow, duplicate id |
| warn | Incomplete or non-standard | no raw imagery, no orthomosaic or DSM, product names, resampled copies, layout, metadata columns missing |
| info | Worth knowing | Record columns not generated yet |

The report lists every issue with the survey's path, and a summary is copied
to the catalogue folder the portal reads. It also lists SFTP holding folders
still waiting to be restructured. Fixes to existing surveys are made with
`archive_fix.py` (metadata columns, resampled copies), dry run first and
reversible.

---

## Where the record lives

Six sidecars are written at intake and preserved verbatim in `L0Ancillary` —
the submission record is part of the archive, not scaffolding:

| Artefact | Contents |
|---|---|
| `metadata.json` | Wizard form dict, snake_case — all pipeline logic reads this |
| `L0_metadata.csv` | One row in the archive format (`templates/ancillary_template.csv`); archived as `<id>_ancillary.csv` |
| `qc_report.json` | Portal verdict under **`overall`** (not `verdict`) |
| `report_parsed.json` | Portal's PDF parse (`values`, `text_values`) |
| `report_extract.txt` | Raw extracted PDF text |
| `renames.json` | `{original: standardised}` |

Gadi adds `ledger.json` per submission and appends to `events.jsonl`, which is
what feeds the QA audit-log sheet in the NCDP QC workbook.

---

## Operator procedures

**Daily.** Check the review queue at `/review`. Each item shows its failed
checks, metadata and file list.

**Releasing an item.** Only after the underlying issue is understood. Release
puts it back through the AV scan, so a release is never a security decision —
but it *is* a statement that the QC failure was acceptable, and it is recorded
against your account.

**Changing a threshold.** Edit `portal/qc_thresholds.json`, restart
`mm91-portal`. Record why in the change log; the thresholds derive from the
`NCDP_Processing_QC` workbook and the two should not drift apart.

**Adding a check.** Add to `portal/qc.py` (intake) or the relevant Gadi stage.
Default to `warn`. Promoting a check to `fail` needs a stated reason under the
governing principle above.

**A partner disputes a verdict.** The full check list is in `qc_report.json` in
their submission's `L0Ancillary`, with the observed value and the limit for
every threshold. Start there.
