# Naming convention

## Survey directories

```
<YYYYMMDD>-<SiteName>
```

`YYYYMMDD` is the **acquisition** date, not the processing or submission date.
`SiteName` is CamelCase with no spaces, punctuation or underscores.

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
<YYYYMMDD>_<SiteName>_<Product>.<ext>
```

`<Product>` is one of `Orthomosaic`, `DSM`, `PointCloud`.

```
20240115_PortFairy_Orthomosaic.tif
20240115_PortFairy_DSM.tif
20240115_PortFairy_PointCloud.las
```

Multi-part outputs append a part token before the extension:

```
20240115_PortFairy_PointCloud_part_1.las
20240115_PortFairy_PointCloud_part_2.las
```

**Products are renamed automatically at intake.** The portal standardises names
on submission and records the mapping in `renames.json`, so naming is correct by
construction and the Gadi pipeline does not rename again — doing so would break
the audit trail.

## L3 datum token

Reprojected products carry the target datum and zone:

```
20240115_PortFairy_Orthomosaic-GDA2020Z54.tif
20240115_PortFairy_DSM-GDA2020Z54.tif
```

This is the only stage that alters a product filename after intake.

## Case and characters

Directory and file names use ASCII letters, digits, hyphen and underscore only.
Extensions are lower case on output (`.tif`, not `.TIF`), though inputs in any
case are accepted and normalised. Raw imagery keeps its original camera-assigned
filename — those are evidence of acquisition order and are never renamed.
