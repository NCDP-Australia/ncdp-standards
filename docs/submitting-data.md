# Submitting a survey

## Who can submit

Anyone with UAV coastal survey data over the Australian coastline. Register at
[ncdp.auscope.org.au/register](https://ncdp.auscope.org.au/register); the NCDP
team approves accounts before upload is enabled.

Sign-in is by one-time emailed link — there is no password to manage or lose.

An institutional email address is preferred over a personal one, because the
contact recorded against a survey is what lets someone follow up on the data
years later.

## What to prepare

Three things, uploaded as three buckets:

| Bucket | Contents |
|---|---|
| **Raw** | Raw imagery as captured, folder or zip |
| **Report** | Processing report from Propeller, Pix4D or Agisoft, as PDF |
| **Products** | Orthomosaic, DSM, point cloud |

Upload the report **first**. The wizard parses it and pre-fills roughly a third
of the metadata, which is the difference between a five-minute submission and a
half-hour one.

## What you type

Around 13 fields plus identifiers. Everything else is parsed from the report,
read from EXIF, derived at NCI, or carried forward from your last submission.

The five that must be present: location, acquisition date, region, point of
contact and access level.

## Upload behaviour

Uploads are resumable. A dropped connection mid-transfer resumes rather than
restarting, which matters at 10–20 GB per survey. Leave the tab open until all
three buckets report complete.

For historical backlogs of multiple terabytes, don't use the web portal —
contact the team about an SFTP delivery.

## Raw imagery only

If you have flown a survey but not processed it, the programme can process it
for you. This is **by arrangement**: email
[ncdp@deakin.edu.au](mailto:ncdp@deakin.edu.au) first. Once the team has
enabled it for your account, the wizard shows a choice at the top: *I have
processed this survey* or *Raw imagery only*.

Choose *Raw imagery only* and the wizard drops the report and products steps.
What to upload:

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
- **Restricted** — for places covered by an agreement with a Traditional
  Owner group. The survey is archived in full, but only the **DSM** and an
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

1. Automated QA/QC runs immediately; you get an email with the outcome.
2. The data is virus-scanned and transferred to NCI.
3. The Gadi pipeline verifies integrity, restructures into L0–L3, checks the
   pixels against the report, and generates catalogue and STAC records.
4. Your survey appears on the public map.

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
