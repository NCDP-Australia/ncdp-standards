# Adding a resource

The NCDP Resources page (https://ncdp.auscope.org.au/resources) is generated
from **`resources.json` in this repository**. The portal fetches it over HTTPS
and caches it for 15 minutes, so a merged change is live within the quarter
hour — no server access needed.

## Add a journal article that uses NCDP data

Append to `resources.json`:

```json
{
  "category": "Journal articles using NCDP data",
  "title": "Full paper title",
  "doi": "10.1016/j.coastaleng.2026.104xxx",
  "description": "Author et al. (2026), Journal Name. One line on what it used NCDP data for."
}
```

Prefer `doi` over `url`: DOIs resolve permanently, publisher URLs do not. Both
work — `doi` is validated against the DOI pattern and anything else is dropped.

## Entry forms

| Form | Renders as |
|---|---|
| `"doi": "10.xxxx/yyy"` | Link via doi.org |
| `"url": "https://..."` | Any external link (http/https only) |
| `"repo": "ncdp-standards", "path": "docs/x.md"` | GitHub blob view |
| `"repo": "...", "path": "...", "raw": true` | Direct download |
| `"file": "x.pdf"` | Served from the catalogue directory on Gadi |

## Categories

Displayed in this order; anything else sorts last.

1. Guides and templates
2. Data standards
3. Journal articles using NCDP data
4. Method references
5. Reports
6. Datasets
7. Links

To change the order, edit `order` in `portal/catalogue.py` in the
`mm91-nirin-intake` repository.

## Before committing

```bash
python3 -c "import json; d=json.load(open('resources.json')); print(len(d['resources']), 'entries')"
```

Invalid JSON means the portal silently falls back to its cached copy, so the
page will look unchanged rather than broken — check the count.
