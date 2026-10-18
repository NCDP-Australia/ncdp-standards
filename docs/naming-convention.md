# Naming convention

## Survey directories

```
<YYYYMMDD>-<SiteName>
```

`YYYYMMDD` is the **acquisition** date, not the processing or submission date.
`SiteName` is the site's name in the NCDP site list (`sites.csv`), CamelCase
with no spaces, punctuation or underscores; it is also the name of the
location folder the survey sits in. The portal suggests the nearest existing
site from the imagery's position; a new site is added to the list before its
first survey is archived.

```
20240115-PortFairy
20250601-Warrnambool
```

Multi-day campaigns use the first acquisition date.

### The directory date is an identifier, not an authority

**The authoritative acquisition date is the `Date` field in
`<id>_ancillary.csv`, recorded in local time.** The `YYYYMMDD` in a directory
name identifies the survey; it is not the source of truth for when the survey
was flown.

For 103 historical surveys the two differ by one day, and in every verified case
the CSV is correct. The cause is a UTC-versus-local conversion in the original
bulk import: an afternoon flight in AEST/AEDT has a UTC timestamp on the same
calendar day, a morning flight has one on the previous day, and the import took
the UTC date.

The directory names are deliberately **not** being corrected. Every product
filename, STAC item id and archive path derives from the directory name, so
renaming would break all of them to fix a label that nothing reads as data. The
catalogue, STAC records and all indicators already read the CSV date.

Worth knowing when you:

* compare a directory name against a flight log — expect ±1 day on older surveys
* join surveys to tide, wave or weather records — use the CSV `Date`, always
* write a new import — derive the directory date from the **local** date


## Product files

```
<YYYYMMDD>_<SiteName>_<Product>[-<CRS>][-<Height>][-cleaned].<ext>
```

`<Product>` is one of `Orthomosaic`, `DSM`, `PointCloud`.

```
20240115_PortFairy_Orthomosaic.tif
20240115_PortFairy_DSM.tif
20240115_PortFairy_PointCloud.las
```

When the delivered file name states the coordinate system, it is kept as
tokens after the product type, and so is a cleaned DSM's `cleaned`:

```
20240115 _Port-Fairy_DSM_GDA94_Z54_AHD09_cleaned.tif  ->  20240115_PortFairy_DSM-GDA94Z54-AHD09-cleaned.tif
```

| Token | Meaning |
|---|---|
| `GDA94Z54`, `GDA94Z55`, ... | GDA94 / MGA zone (EPSG:28354, 28355, ...) |
| `GDA2020Z50`, `GDA2020Z55`, ... | GDA2020 / MGA zone (EPSG:7850, 7855, ...) |
| `WGS84Z54`, ... | WGS 84 / UTM zone, southern hemisphere (EPSG:32754, ...) |
| `AHD09` | heights in AHD, derived with AUSGeoid09 (as delivered) |
| `AHD` | heights in AHD, derived with AUSGeoid2020 |
| `cleaned` | the contributor's cleaned DSM, archived beside the uncleaned one |

The name must agree with the file: the zone in the name with the CRS the
raster is tagged with, and `Orthomosaic` / `DSM` with what the file holds
(`gadi/product_types.py` reports any file where they differ).

**One file per product, at its native resolution.** A resampled copy of a
product delivered beside it (VCMP's `..._cleaned_1m` next to `..._cleaned`) is
not archived; only the native-resolution file is kept. A product delivered at
one resolution only is kept, and no resolution goes into its name.

The product type is recognised from the name: `ortho` (or Propeller's
`GeoTIFF` export) is the orthomosaic, `DSM`/`DSN`/`DEM` the DSM, `.las`/`.laz`
the point cloud. Sidecars (`.aux.xml`, `.ovr`, `.tfw`) are renamed with their
product.

Multi-part outputs append a part token before the extension:

```
20240115_PortFairy_PointCloud_part_1.las
20240115_PortFairy_PointCloud_part_2.las
```

**Products are renamed automatically.** Portal submissions are renamed at
intake, and SFTP deliveries when `sftp_restructure.py` arranges them; both
record the mapping (`renames.json` for the portal, the batch's `plan.csv` for
SFTP), so naming is correct by construction and the Gadi QA/QC pipeline does
not rename again — doing so would break the audit trail.

Other delivered files keep their names: crop polygons (VCMP's
`..._crop_GDA94_Z55.DXF/.KML`) go to L4 as the area of interest, and GCP files,
logs and reports keep the contributor's names in their L0 folders.

## L3 products

L3 is the analysis-ready level: **GDA2020 / MGA, heights in AHD (AUSGeoid2020),
Cloud-Optimised GeoTIFF, cleaned, cropped to the survey boundary.** Names carry
the target datum and zone, and every DSM carries `AHD`:

```
20240115_PortFairy_Orthomosaic-GDA2020Z54.tif
20240115_PortFairy_DSM-GDA2020Z54-AHD.tif
20240115_PortFairy_DSM-GDA2020Z54-AHD-cleaned.tif
```

On the way from L2 to L3 a GDA94 or WGS 84 product is shifted to GDA2020, and a
DSM whose heights were derived with AUSGeoid09 (`AHD09`) gets the vertical
correction to AUSGeoid2020: the change in ellipsoidal height from the GDA94 to
GDA2020 transformation minus the change in geoid undulation between the two
models (Δh − ΔN), taken at the grid point nearest the survey's centre
(per-site table first, else the national ~1′ grid; typically −0.12 to +0.21 m
along the coast). A product delivered in GDA2020 with AUSGeoid2020 heights is
copied as is, and its DSM gains the `AHD` token. So `AHD09` never appears in
L3; existing L3 DSMs named `-AHD09` were renamed to `-AHD` on 18 October 2026
(their heights had already been corrected; only the names changed).

This is the only stage that alters a product filename after intake.

## Metadata record

```
<YYYYMMDD>-<SiteName>_ancillary.csv      in L0/L0Ancillary/
```

Its `Project Identifier` is the survey folder name, and its `Date`, `Location`
and `Region` match the survey folder, the location folder and the state
folder. The weekly archive audit reports any survey where they disagree.

## Case and characters

Directory and file names use ASCII letters, digits, hyphen and underscore only.
Extensions are lower case on output (`.tif`, not `.TIF`), though inputs in any
case are accepted and normalised. Raw imagery keeps its original camera-assigned
filename — those are evidence of acquisition order and are never renamed.
