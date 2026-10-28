# NCDP Data Standards and Procedures

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23127540.svg)](https://doi.org/10.5281/zenodo.23127540)

Data standards, metadata schema, templates and procedures for the **National Coastal Drone
Program**: a nationally coordinated archive of UAV coastal survey data, coordinated by Deakin
University and funded by AuScope (NCRIS). The intake portal at
[ncdp.auscope.org.au](https://ncdp.auscope.org.au) links here rather than hosting copies.

**This repository holds the working drafts.** The **locked, published revision** is on the
[Wiki](https://github.com/NCDP-Australia/ncdp-standards/wiki), regenerated from the drafts by
`Scripts/publish_to_wiki.py` when a revision is released. Every release is archived on Zenodo with
its own DOI and PDF snapshots of every page.

| Where | What it holds | How it changes |
|---|---|---|
| This repository | Drafts for the next revision; schema files and templates | Pull requests |
| [Wiki](https://github.com/NCDP-Australia/ncdp-standards/wiki) | The current locked revision (read-only for users) | Regenerated on release |
| [Releases](https://github.com/NCDP-Australia/ncdp-standards/releases) / Zenodo | Every revision, citable, with PDFs | One per revision |

## Contents

| Path | What it is |
|---|---|
| `docs/field-manual.md` | The NCDP Field Manual: equipment, mission planning, flying a survey, upload, checklists and forms (images in `docs/field-manual_media/`) |
| `docs/data-structure.md` | Archive hierarchy and the L0–L4 processing levels |
| `docs/naming-convention.md` | File and directory naming rules |
| `docs/metadata-schema.md` | The metadata schema: the archive's record format (v5.0) and each attribute |
| `docs/submitting-data.md` | How to contribute a survey: the portal wizard, and SFTP for large deliveries |
| `docs/qaqc-protocol.md` | What is checked, what blocks, who acts on each finding, the weekly archive audit |
| `docs/indicators.md` | The L4 coastal change indicators, the erosion warning, hotspots and site reports |
| `docs/STATUS.md` | Generated status of every page (from `publish.yaml`) |
| `schema/ncdp-metadata-schema-v5.csv` / `.json` | **Current** archive record format, 131 columns (+ 28 generated `Record …`) |
| `schema/ncdp-metadata-schema-v4.*`, `-v3.*` | Superseded schema versions, kept for existing tools |
| `schema/ncdp-qc-thresholds-v3.json` | Numeric QA/QC thresholds |
| `templates/ancillary_template.csv` | **Use this one.** Empty v5.0 metadata CSV, one per survey: `<YYYYMMDD-Location>_ancillary.csv` |
| `templates/L0_metadata_template.csv` | The v3.1 attributes only, kept for existing tools |
| `resources.json`, `news.json` | Feed the portal's Publications and News pages (see CONTRIBUTING.md) |
| `publish.yaml` | Release manifest: revision, pages, status |
| `Scripts/` | `publish_to_wiki.py` (wiki, status, PDFs), `docx_to_markdown.py` (Word → draft page) |

## Versioning

The documents are versioned as **one set**: revision `MAJOR.YYx`, recorded in `publish.yaml`,
stamped on every wiki page and PDF, and used as the release tag (`v5.01`).

| Part | When it changes | Example |
|---|---|---|
| **MAJOR** (number) | The **metadata schema's major version** changes (a column renamed, removed or reordered), or the archive layout changes so that existing surveys or tools must be updated. Resets the minor to `00`. | schema v6.0 → revision `6.00` |
| **MINOR** (`.YY`, two digits) | Something a contributor, operator or user **does differently**, or new scope: a procedure, a check, a threshold, an indicator method, a new page, a schema field added. Drops any patch letter. | `5.01` → `5.02` |
| **PATCH** (letter) | Nothing anyone does changes: wording, corrections of typos, formatting, figures, clarifying existing intent. | `5.01` → `5.01a` |

**Minor or patch?** Ask: *would someone who followed the previous revision need to do anything
differently, or re-check data or results they already have?* Yes → minor. No → patch.

The **metadata schema** keeps its own version (`schema_version` in `publish.yaml`, now 5.0): it
changes only when the record format changes, which is always a minor (field added) or a major
(field renamed, removed or reordered) revision of the set. The schema files are generated from the
intake portal (`portal/ancillary_columns.py`); do not hand-edit them, and CI checks that the v5.0 CSV,
JSON and template agree.

Every revision is recorded in `CHANGELOG.md` (published as the wiki's Changelog page). Minor revisions
are announced to partners; patch revisions need no announcement.

## Document status

The authoritative status of each page is in `publish.yaml` and the generated `docs/STATUS.md`:
**adopted** (reviewed and locked for the revision), **provisional** (in use; named parameters may still
change in a minor revision) or **stub** (being written). Each page records the revision in which it last
changed (`last_revised`).

## Contributing changes

Use **fork → branch → pull request**; you do not need write access.

1. Fork the repository on GitHub, clone your fork, and add this repository as `upstream`.
2. Create a branch (`git checkout -b fix-naming-example`) and edit the **draft** in `docs/` (never
   the wiki: it is regenerated). Keep one logical change per pull request.
3. Commit, push to your fork, and open a pull request against `main`. Say what changed and why, and
   whether it is a **minor** or a **patch** change in the sense above.
4. Before merging, the maintainers update `last_revised` for the changed pages in `publish.yaml` (to
   the next revision) and add a line to `CHANGELOG.md` under *Unreleased*.

To add a publication or a news item for the portal, see `CONTRIBUTING.md`.

To start a page from a Word document (e.g. the Field Manual):

```bash
# needs pandoc and Pillow (LibreOffice optional, converts EMF drawings)
python Scripts/docx_to_markdown.py "NCDP_Field_Manual.docx" docs/field-manual.md --title "NCDP Field Manual"
```
then check the result and add it to `publish.yaml` (`status: stub` or `provisional` until reviewed).
When the Word original is updated, rerun the same command and commit the changes; the diff shows exactly
what changed in the manual.

## Releasing a revision

A release is cut by pushing a tag; GitHub Actions does the rest (`.github/workflows/release.yml`):
it checks that the tag matches `publish.yaml`, publishes the pages to the wiki, renders a PDF of every
page, and creates the GitHub release with the PDFs and the changelog section as notes. Zenodo then
archives the release and mints its version DOI under the concept DOI.

1. Set `revision` and `revision_date` in `publish.yaml`; check every changed page's `last_revised`.
2. In `CHANGELOG.md`, rename *Unreleased* to `Revision 5.02 — YYYY-MM-DD`.
3. Update `version` and `date-released` in `CITATION.cff`.
4. Preview locally (optional): `pip install pyyaml && python Scripts/publish_to_wiki.py --dry-run`.
5. Merge to `main`, then tag and push:
   ```bash
   git tag -a v5.02 -m "Revision 5.02" && git push origin v5.02
   ```
6. Check the release page and the Zenodo record; the new version DOI appears on Zenodo within minutes.

To publish by hand instead (e.g. a first time): clone the wiki next to this repository
(`git clone https://github.com/NCDP-Australia/ncdp-standards.wiki.git ../ncdp-standards.wiki`), run
`python Scripts/publish_to_wiki.py` (add `--pdf` for PDFs into `releases/`, needs pandoc and
weasyprint), review the diff in the wiki checkout, commit and push there, then create the release.

## How to cite

Nuyts, S., Allan, B., Ierodiaconou, D., & National Coastal Drone Program (NCDP). NCDP Data Standards
and Procedures (revision 5.01). Zenodo. https://doi.org/10.5281/zenodo.23127540

The concept DOI always resolves to the latest revision; cite the version DOI of the revision you
followed (on its Zenodo record and GitHub release). GitHub's "Cite this repository" button (from
`CITATION.cff`) gives the citation in APA and BibTeX.

## Licence

Documentation and schema: [CC BY 4.0](LICENSE). Survey data is licensed per survey; see each record's
`License` field.

## Contact

National Coastal Drone Program — ncdp@deakin.edu.au
