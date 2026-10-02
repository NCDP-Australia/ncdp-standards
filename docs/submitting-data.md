# Submitting a survey

## Who can submit

Anyone with UAV coastal survey data over the Australian coastline. Register at
[ncdp.auscope.org.au/register](https://ncdp.auscope.org.au/register); the NCDP
team approves accounts before upload is enabled. Browsing and downloading data
needs no account.

Sign-in is by one-time emailed link — there is no password to manage or lose.

An institutional email address is preferred over a personal one, because the
contact recorded against a survey is what lets someone follow up on the data
years later.

## What to prepare

The wizard asks for the files first and the survey details last, because most
details are read from the files. For a processed survey the steps are
**1 processing report → 2 upload data → 3 survey details**; for raw imagery only,
**1 upload → 2 survey details**.

| Step | Contents | Archived in |
|---|---|---|
| **Processing report** | From Propeller, Pix4D or Agisoft, as PDF | `L0/L0Ancillary` |
| **Raw imagery** | As captured, one folder per flight, with the drone's MRK/PPK files | `L0/L0Raw/L0RGB/<flight>` |
| **Ground control files** | GCP and check-point coordinates as CSV/TXT, PPK image positions. For Propeller, every AeroPoints export. Required unless no GCPs were used | `L0/L0GCPs` |
| **GNSS logs** | Base-station RINEX (`.obs`, `.26o`, `.rnx`, `.crx`), `.ubx`, `.sbf`, Trimble `.t02/.t04`, `.rtcm` | `L0/L0FlightLogs` |
| **Processed data** | Upload into the level that matches what you have — at least one of L2 or L3, and say which coordinate system it is in (datum, grid zone, heights; filled from the report or the file names where they say it): | |
| · L1 Intermediate | In-between processing steps, e.g. thermal or multispectral calibration. Most surveys have none | `L1` |
| · L2 Original | DSM, orthomosaic, point cloud exactly as the software produced them | `L2` |
| · L3 Cleaned | The same after your own manual editing (cropped, noise or water removed). State its coordinate system; GDA2020 / MGA with AHD heights is ready to publish | `L3` |
| **Crop polygon** | Optional: a crop / area-of-interest polygon (`.kml`, `.dxf`, `.geojson`, shapefile), uploaded with the processed data | with the products |

If you upload only L2, NCDP produces the L3 copy (GDA2020, AHD heights,
cloud-optimised) for you.

Upload the report **first**. The wizard parses it and pre-fills roughly a third
of the metadata, including the processing software, the coordinate system and
the number of GCPs. Your files are read in your browser as well:

- **Imagery:** acquisition date, the nearest existing NCDP site (within 5 km),
  state, airframe, flying height above take-off, camera angle and forward/side
  overlap, with a table of the individual flights.
- **Ground control files:** GCP and check-point counts, check points recognised
  by their labels, and the coordinate systems (AeroPoints exports).
- **Product file names:** the coordinate system, when the name states it.

Values you type are never overwritten by what the files say; when the two
disagree, the wizard tells you and offers the value from the files.

## What you type

Around 13 fields plus identifiers. Everything else is parsed from the report,
read from EXIF, derived at NCI, or carried forward from your last submission.

The five that must be present: location, acquisition date, region, point of
contact and access level.

## Upload behaviour

Uploads are resumable. A dropped connection mid-transfer resumes rather than
restarting, which matters at 10–20 GB per survey.

When you press **Submit for QA/QC**, the submission box turns **amber** while
the last files are handed over to the server: keep the tab open. It turns
**green** once the server has everything. You can then close the page: the
checks run on the server, and the result arrives by email and under *My
submissions*.

## Large deliveries and backlogs (SFTP)

For historical backlogs or many surveys at once, don't use the web portal:
contact the team about an SFTP account. You upload one folder per survey, each
with its metadata CSV (`templates/ancillary_template.csv`), in agreed batches.
NCDP's tools then arrange every survey into the archive structure and name the
files, so you don't need to. The NCDP SFTP guide covers the set-up on Mac,
Windows and Ubuntu.

## Raw imagery only

If you have flown a survey but not processed it, the programme can process it
for you, as capacity allows. The wizard asks at the top: *I have processed
this survey* or *Raw imagery only*. For a large or urgent job, email
[ncdp@deakin.edu.au](mailto:ncdp@deakin.edu.au) first.

Choose *Raw imagery only* and the wizard drops the report and processed-data
steps. What to upload:

| What | Why |
|---|---|
| **The full image set** (required) | It is the whole delivery. A raw-only submission with no imagery is held. |
| **Flight / GNSS logs** — `.MRK`, `.obs`, `.nav`, `.rtk` | Allow PPK positioning. Imagery alone can be processed; with logs it can be processed *well*. |
| **GCP coordinates** — a CSV or TXT with a point name and three coordinates per row | Needed if you laid ground control. The filename does not matter. Without the file the programme cannot use your control points. |

And three fields that matter more than usual, because there is no report to
read them from: flying height, forward overlap and side overlap. Approximate
values are fine.

The wizard reads the first image as soon as you choose the folder, and fills in
the **acquisition date** (and flying height, when the imagery records it) from
the frames themselves. If what it finds disagrees with what you typed, it says
so and offers the date from the imagery — worth taking, unless you know the
camera clock is wrong.

The five required fields are the same as for any submission.

### What happens to a raw-only survey

1. QA/QC checks the imagery itself: that it is there, that there is enough of
   it, that the frames carry GPS positions and that the capture date matches
   the one on the form.
2. It is archived at NCI as a survey in its own right. It is **not published**
   in the public catalogue while it is awaiting processing: an entry with
   nothing downloadable helps nobody. The NCDP team can see it, and you can ask
   us about it by quoting your submission reference.
3. When the programme has processed it, the orthomosaic, DSM and point cloud
   are added to **the same survey** — not a new one — and it then appears in
   the catalogue like any other processed survey.

The record keeps both contributions: the imagery is yours (recorded as the
producer), the products are the programme's (recorded as the processor).
`Submission Type` stays `raw-only` permanently so that distinction is never
lost; `Processing State` records where the survey is now.

## Access level

Every survey is either **Open** or **Restricted**.

- **Open** — everything is published: orthomosaic, DSM, point cloud and the
  map preview.
- **Restricted** — for places covered by a prior data agreement. The
  survey is archived in full, but only the **DSM** and an
  **uncoloured point cloud** are published; the orthomosaic, the raw imagery
  and any preview made from them are not. Export the point cloud without
  colour: at drone densities a coloured point cloud shows almost as much as
  the orthomosaic.

The portal checks each survey's location against the areas covered by these
agreements. If you submit a survey from such an area as Open, you'll see a
warning, and until the NCDP team has reviewed the access level with you, it
is published as Restricted. Nothing is lost either way: everything you upload
is archived, and the access level can be changed after review.

## What happens next

1. Automated QA/QC runs on the server; you get an email with the outcome.
2. The data is virus-scanned and transferred to NCI.
3. The Gadi pipeline verifies integrity, restructures into L0–L3, checks the
   pixels against the report, and generates catalogue and STAC records.
4. Your survey appears on the public map. Open surveys are published from
   `/g/data/mm91/NCDP`; Restricted ones are kept in `/g/data/mm91/admin` and
   published in part (see Access level).
5. A weekly audit keeps checking every archived survey's structure, names,
   metadata and data; if it finds a problem with yours, the team may contact
   you.

## If your submission is held

Only five things block: missing critical metadata, an invalid contact email,
executable files, unrecognised file types, or a truncated transfer. For a
raw-only submission a sixth also blocks: no raw imagery. Everything
else — a missing okta reading, a threshold slightly out — flags for review and
still proceeds.

If held, the email lists exactly which checks failed. The team reviews held
submissions and will follow up.

## Licensing

CC BY 4.0 is the programme default under the NCOF framework. Other licences are
supported; record yours in the `License` field.
