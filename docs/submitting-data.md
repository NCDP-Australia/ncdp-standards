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

## What happens next

1. Automated QA/QC runs immediately; you get an email with the outcome.
2. The data is virus-scanned and transferred to NCI.
3. The Gadi pipeline verifies integrity, restructures into L0–L3, checks the
   pixels against the report, and generates catalogue and STAC records.
4. Your survey appears on the public map.

## If your submission is held

Only five things block: missing critical metadata, an invalid contact email,
executable files, unrecognised file types, or a truncated transfer. Everything
else — a missing okta reading, a threshold slightly out — flags for review and
still proceeds.

If held, the email lists exactly which checks failed. The team reviews held
submissions and will follow up.

## Licensing

CC BY 4.0 is the programme default under the NCOF framework. Other licences are
supported; record yours in the `License` field.
