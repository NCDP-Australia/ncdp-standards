# Metadata schema v3.0

117 attributes describing a survey. This is the single vocabulary shared
by the submission wizard, `metadata.json`, the QA/QC engines, the archived CSV
and the STAC records — so that no translation layer is needed anywhere between
them.

Generated from `portal/schema.py`. The header strings are exact: the archive's
CSVs and the STAC generator key on them character for character, so treat any
change as a schema version bump.

## Provenance

Each field is filled by exactly one party. This is what makes a 117-field schema
tractable for a contributor: only 23 are typed by hand.

| Provenance | Count | Filled by |
|---|---|---|
| `manual` | 23 | The contributor, in the wizard |
| `report` | 35 | Parsed from the processing report PDF |
| `exif` | 17 | Read from image EXIF during the Gadi build |
| `derived` | 36 | Computed on Gadi (footprints, areas, EPSG, file levels) |
| `carried` | 6 | Copied forward from the contributor's previous survey |

## Required fields

Five fields block submission if missing. They are the minimum needed for a
survey to be found, attributed and licensed:

| Form key | Header |
|---|---|
| `site_name` | `Location` |
| `acquisition_date` | `Date` |
| `region` | `Region` |
| `point_of_contact` | `Point of Contact` |
| `access_level` | `Access Level (...)` |

The contact address must also parse as an email. Everything else warns.

## Access levels

`Open`, `Sensitive`, `Embargoed`, `Restricted`, `Metadata-Only`. Open is the
programme default and the expectation for publicly funded survey work.
`Metadata-Only` publishes the discovery record while withholding the data.

## Carry-forward fields

6 fields are copied from a contributor's previous submission, since
airframe, sensor and organisation rarely change between surveys. They remain
editable — carry-forward is a convenience, not an assertion.

---

## Fields entered manually

| # | Header | Form key | Required |
|---|---|---|---|
| 1 | `Project Identifier` | `project_identifier` | no |
| 2 | `Date` | `acquisition_date` | **yes** |
| 3 | `Location` | `site_name` | **yes** |
| 4 | `Region` | `region` | **yes** |
| 14 | `Description` | `description` | no |
| 15 | `Tags` | `tags` | no |
| 16 | `Access Level (Open, Sensitive, Embargoed, Restricted, Metadata-Only)` | `access_level` | **yes** |
| 42 | `Pilot in Command` | `pilot_in_command` | no |
| 43 | `Flight Crew` | `flight_crew` | no |
| 56 | `Predominant cloud type` | `predominant_cloud_type` | no |
| 57 | `Cloud Cover (OKTA)` | `cloud_cover_okta` | no |
| 58 | `Wind Speed (knots in selectable brackets)` | `wind_speed_knots` | no |
| 59 | `Wind Direction` | `wind_direction` | no |
| 65 | `Were GCPs Used?` | `gcps_used` | no |
| 66 | `Type of Ground Control Points (GCPs)` | `gcp_type` | no |
| 67 | `Number of GCPs` | `number_of_gcps` | no |
| 75 | `Data processing date` | `data_processing_date` | no |
| 82 | `Were ICPs Used?` | `icps_used` | no |
| 83 | `Number of ICPs` | `number_of_icps` | no |
| 114 | `Comments` | `comments` | no |
| 115 | `Associated ancillary data or images (in L0Ancillary folder)` | `ancillary_data` | no |
| 116 | `Did Coastal Management Works Occur Between the Previous Survey and This Survey?` | `coastal_works` | no |
| 117 | `Description of Coastal Management Works` | `coastal_works_desc` | no |

## Fields from the processing report

| # | Header | Form key | Required |
|---|---|---|---|
| 48 | `Image Overlap` | — | no |
| 49 | `Image Sidelap` | — | no |
| 50 | `Estimated Image Resolution` | — | no |
| 60 | `Total Number of RGB Images` | `total_rgb_images` | no |
| 62 | `Image Horizontal Coordinate System` | `coordinate_system` | no |
| 63 | `Image Vertical Coordinate System` | — | no |
| 68 | `GCPs Horizontal Coordinate System` | `gcp_h_crs` | no |
| 69 | `GCPs Horizontal Coordinate EPSG` | — | no |
| 70 | `GCPs Vertical Coordinate System` | `gcp_v_crs` | no |
| 71 | `GCPs Vertical Coordinate EPSG` | — | no |
| 72 | `Data Processing Platform and version` | `data_processing_platform` | no |
| 78 | `Processing x rmse (m)` | `processing_x_rmse_m` | no |
| 79 | `Processing y rmse (m)` | `processing_y_rmse_m` | no |
| 80 | `Processing z rmse (m)` | `processing_z_rmse_m` | no |
| 81 | `Processing overall rmse (m)` | `processing_overall_rmse_m` | no |
| 84 | `ICPs Horizontal Coordinate System` | `icp_h_crs` | no |
| 85 | `ICPs Horizontal Coordinate EPSG` | — | no |
| 86 | `ICPs Vertical Coordinate System` | `icp_v_crs` | no |
| 87 | `ICPs Vertical Coordinate EPSG` | — | no |
| 88 | `ICP x rmse (m)` | — | no |
| 89 | `ICP y rmse (m)` | — | no |
| 90 | `ICP z rmse (m)` | — | no |
| 91 | `ICP overall rmse (m)` | — | no |
| 95 | `Orthomosaic Ground Sample Distance (m)` | — | no |
| 96 | `Orthomosaic horizontal coordinate system` | — | no |
| 97 | `Orthomosaic horizontal coordinate EPSG` | — | no |
| 101 | `DSM Ground Sample Distance (m)` | — | no |
| 102 | `DSM horizontal coordinate system` | — | no |
| 103 | `DSM horizontal coordinate EPSG` | — | no |
| 104 | `DSM vertical coordinate system` | — | no |
| 105 | `DSM vertical coordinate EPSG` | — | no |
| 110 | `Point Cloud horizontal coordinate system` | — | no |
| 111 | `Point Cloud horizontal coordinate EPSG` | — | no |
| 112 | `Point Cloud vertical coordinate system` | — | no |
| 113 | `Point Cloud vertical coordinate EPSG` | — | no |

## Fields from image EXIF

| # | Header | Form key | Required |
|---|---|---|---|
| 21 | `airframe serial number` | — | no |
| 22 | `airframe serial number alternate` | — | no |
| 23 | `Sensor 1 Model` | — | no |
| 24 | `Sensor 1 Serial Number/Identifier` | — | no |
| 25 | `Sensor 1 Data Collection Type` | — | no |
| 26 | `Sensor 1 Resolution (MP)` | — | no |
| 27 | `Sensor 1 FOV` | — | no |
| 28 | `Sensor 1 Focal Length` | — | no |
| 29 | `Sensor 1 Image Height` | — | no |
| 30 | `Sensor 1 Image Width` | — | no |
| 31 | `Sensor 1 Calibration` | — | no |
| 32 | `Sensor 1 Calibration Data (in raw-acquisition-calibration)` | — | no |
| 33 | `Flying Height (m)` | — | no |
| 51 | `Start Time Local` | — | no |
| 52 | `End Time Local` | — | no |
| 54 | `Start Time UTC` | — | no |
| 55 | `End Time UTC` | — | no |

## Fields derived on Gadi

| # | Header | Form key | Required |
|---|---|---|---|
| 5 | `north-east boundary latitude` | — | no |
| 6 | `north-east boundary longitude` | — | no |
| 7 | `north-west boundary latitude` | — | no |
| 8 | `north-west boundary longitude` | — | no |
| 9 | `south-east boundary latitude` | — | no |
| 10 | `south-east boundary longitude` | — | no |
| 11 | `south-west boundary latitude` | — | no |
| 12 | `south-west boundary longitude` | — | no |
| 18 | `Airframe` | — | no |
| 19 | `Airframe Type` | — | no |
| 20 | `Flight Path File` | — | no |
| 34 | `Vertical Height Offset` | — | no |
| 36 | `DOI/ROR` | — | no |
| 37 | `Attribution (Credit Statement)` | — | no |
| 38 | `Attribution RAID` | — | no |
| 39 | `Project Funding` | — | no |
| 44 | `Length of location mapped (km)` | — | no |
| 45 | `Area of location mapped (km2)` | — | no |
| 46 | `Mission Planning Software` | — | no |
| 47 | `Flight Plan` | — | no |
| 53 | `UTC to Local Difference` | — | no |
| 61 | `Total Number of Flights` | — | no |
| 64 | `Sensor Angle` | — | no |
| 74 | `Data processing person and/or institution ID` | — | no |
| 76 | `Data processing area (km2)` | — | no |
| 77 | `Data QA/QC` | — | no |
| 92 | `Orthomosaic File Name` | — | no |
| 93 | `Orthomosaic File Type` | — | no |
| 94 | `Orthomosaic Folder Level` | — | no |
| 98 | `DSM File Name` | — | no |
| 99 | `DSM File Type` | — | no |
| 100 | `DSM Folder Level` | — | no |
| 106 | `Point Cloud File Name` | — | no |
| 107 | `Point Cloud File Type` | — | no |
| 108 | `Point Cloud Folder Level` | — | no |
| 109 | `Point Cloud number of points` | — | no |

## Fields carried forward

| # | Header | Form key | Required |
|---|---|---|---|
| 13 | `Purpose` | `purpose` | no |
| 17 | `License` | `license` | no |
| 35 | `Organisation` | `organisation` | no |
| 40 | `Point of Contact` | `point_of_contact` | **yes** |
| 41 | `Point of Contact ORCID/DOI` | `point_of_contact_orcid` | no |
| 73 | `Data processing person and/or institution` | `data_processing_person` | no |
