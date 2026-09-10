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
