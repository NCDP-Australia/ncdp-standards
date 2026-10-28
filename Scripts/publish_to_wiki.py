#!/usr/bin/env python3
"""
Publish the locked revision of the NCDP Data Standards and Procedures to the GitHub Wiki
(after the APPN Field Protocols and Pipelines model).

The repository holds working drafts (docs/*.md). The wiki holds the locked revision,
generated from publish.yaml:
  - each page copied to <wiki>/<wiki_page>.md with a "Locked revision" banner under its title;
  - links between manifest pages rewritten to wiki links; links to other repository files
    (schema/, templates/) rewritten to that file at the release tag;
  - images in <doc>_media/ copied to <wiki>/media/<wiki_page>/;
  - Home.md, _Sidebar.md, _Footer.md and a Changelog page generated;
  - docs/STATUS.md (in the repository) regenerated from the manifest.

Usage (from the repository root):
  python Scripts/publish_to_wiki.py --check          # validate publish.yaml only (used by CI)
  python Scripts/publish_to_wiki.py --dry-run        # show what would change in the wiki
  python Scripts/publish_to_wiki.py                  # write into ../ncdp-standards.wiki
  python Scripts/publish_to_wiki.py --wiki DIR       # another wiki checkout
  python Scripts/publish_to_wiki.py --pdf            # also PDFs into releases/Rev<revision>/ (pandoc + weasyprint)

Needs PyYAML; --pdf needs pandoc and weasyprint on PATH.
"""
from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REV_RE = re.compile(r"^\d+\.\d{2}[a-z]?$")
STATUSES = {"adopted": "Adopted", "provisional": "Provisional", "stub": "Stub"}
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")


def rev_key(r: str):
    m = re.match(r"^(\d+)\.(\d{2})([a-z]?)$", r)
    return (int(m.group(1)), int(m.group(2)), m.group(3)) if m else (0, 0, "")


def load_manifest() -> dict:
    return yaml.safe_load((ROOT / "publish.yaml").read_text(encoding="utf-8"))


def check(man: dict) -> list[str]:
    errs = []
    rev = str(man.get("revision", ""))
    if not REV_RE.match(rev):
        errs.append(f"revision {rev!r} is not MAJOR.YYx (e.g. 5.01, 5.01a)")
    cats = man.get("categories") or []
    seen = set()
    for p in man.get("pages") or []:
        src = ROOT / p.get("source", "")
        if not src.is_file():
            errs.append(f"{p.get('source')}: file not found")
        w = p.get("wiki_page", "")
        if not re.fullmatch(r"[A-Za-z0-9-]+", w) or w in seen or w in ("Home", "Changelog"):
            errs.append(f"{p.get('source')}: wiki_page {w!r} missing, duplicated or reserved")
        seen.add(w)
        if p.get("category") not in cats:
            errs.append(f"{p.get('source')}: category {p.get('category')!r} not in categories")
        if p.get("status") not in STATUSES:
            errs.append(f"{p.get('source')}: status {p.get('status')!r} not one of {sorted(STATUSES)}")
        lr = str(p.get("last_revised", ""))
        if not REV_RE.match(lr) or (REV_RE.match(rev) and rev_key(lr) > rev_key(rev)):
            errs.append(f"{p.get('source')}: last_revised {lr!r} invalid or later than revision {rev}")
    if man.get("home_intro") and not (ROOT / man["home_intro"]).is_file():
        errs.append(f"home_intro {man['home_intro']} not found")
    return errs


def page_map(man: dict) -> dict:
    """Repository path (posix, relative) -> wiki page name."""
    return {Path(p["source"]).as_posix(): p["wiki_page"] for p in man["pages"]} | {"CHANGELOG.md": "Changelog"}


def rewrite_links(text: str, src: Path, man: dict, pages: dict, media_dir: str | None) -> str:
    tag = "v" + man["revision"]
    blob = f"https://github.com/{man['repository']}/blob/{tag}/"

    def sub(m):
        bang, label, target, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            return m.group(0)
        path, _, frag = target.partition("#")
        rel = (src.parent / path).resolve()
        try:
            relp = rel.relative_to(ROOT).as_posix()
        except ValueError:
            return m.group(0)
        if bang and media_dir and "_media/" in relp:
            return f"{bang}[{label}](media/{media_dir}/{Path(relp).name}{title})"
        if relp in pages:
            return f"[{label}]({pages[relp]}{'#' + frag if frag else ''})"
        return f"{bang}[{label}]({blob}{relp}{'#' + frag if frag else ''}{title})"
    return LINK_RE.sub(sub, text)


def banner(man: dict, p: dict) -> str:
    st = STATUSES[p["status"]]
    note = f" · {p['note']}" if p.get("note") else ""
    return (f"> **Locked revision {man['revision']}** ({man['revision_date']}) · status: **{st}** · "
            f"page last revised in {p['last_revised']} · "
            f"[draft and history](https://github.com/{man['repository']}/blob/main/{p['source']}){note}\n")


def render_page(man: dict, p: dict, pages: dict) -> str:
    src = ROOT / p["source"]
    text = src.read_text(encoding="utf-8")
    lines = text.splitlines()
    body = lines[1:] if lines and lines[0].startswith("# ") else lines
    out = f"# {p['title']}\n\n{banner(man, p)}\n" + "\n".join(body).lstrip("\n") + "\n"
    return rewrite_links(out, src, man, pages, p["wiki_page"])


def render_home(man: dict) -> str:
    intro = (ROOT / man["home_intro"]).read_text(encoding="utf-8").strip() if man.get("home_intro") else ""
    doi = man["concept_doi"]
    out = [f"# NCDP Data Standards and Procedures\n",
           f"> **Locked revision {man['revision']}** ({man['revision_date']}) · metadata schema v{man['schema_version']} · "
           f"[cite (DOI {doi})](https://doi.org/{doi}) · [Changelog](Changelog)\n", intro, ""]
    for cat in man["categories"]:
        ps = [p for p in man["pages"] if p["category"] == cat]
        if not ps:
            continue
        out += [f"## {cat}\n", "| Page | Status | Last revised |", "|---|---|---|"]
        out += [f"| [{p['title']}]({p['wiki_page']}) | {STATUSES[p['status']]}"
                f"{' — ' + p['note'] if p.get('note') else ''} | {p['last_revised']} |" for p in ps]
        out.append("")
    out += ["## How to cite\n",
            f"Cite the revision you followed. The concept DOI [{doi}](https://doi.org/{doi}) always resolves to the "
            "latest; each revision has its own DOI on its Zenodo record and GitHub release.\n"]
    return "\n".join(out)


def render_sidebar(man: dict) -> str:
    out = ["**[Home](Home)**", ""]
    for cat in man["categories"]:
        ps = [p for p in man["pages"] if p["category"] == cat]
        if ps:
            out.append(f"**{cat}**")
            out += [f"- [{p['title']}]({p['wiki_page']})" for p in ps]
            out.append("")
    out += ["[Changelog](Changelog)", "", f"_Revision {man['revision']}_"]
    return "\n".join(out) + "\n"


def render_footer(man: dict) -> str:
    return (f"NCDP Data Standards and Procedures · revision {man['revision']} ({man['revision_date']}) · "
            f"[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) · "
            f"[doi:{man['concept_doi']}](https://doi.org/{man['concept_doi']}) · ncdp@deakin.edu.au\n")


def render_status(man: dict) -> str:
    out = ["# Document status\n",
           f"_Generated from `publish.yaml` by `Scripts/publish_to_wiki.py` — do not edit by hand._\n",
           f"Current revision: **{man['revision']}** ({man['revision_date']}); metadata schema v{man['schema_version']}.\n",
           "| Page | Category | Status | Last revised | Source |", "|---|---|---|---|---|"]
    out += [f"| {p['title']} | {p['category']} | {STATUSES[p['status']]}{' — ' + p['note'] if p.get('note') else ''} "
            f"| {p['last_revised']} | `{p['source']}` |" for p in man["pages"]]
    return "\n".join(out) + "\n"


def build(man: dict, dest: Path) -> list[str]:
    """Write every wiki file into dest; return the relative paths written."""
    pages = page_map(man)
    written = []

    def put(rel, text):
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        (dest / rel).write_text(text, encoding="utf-8")
        written.append(rel)
    for p in man["pages"]:
        put(f"{p['wiki_page']}.md", render_page(man, p, pages))
        media = ROOT / p["source"].replace(".md", "_media")
        if media.is_dir():
            for f in media.iterdir():
                if f.is_file():
                    (dest / "media" / p["wiki_page"]).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dest / "media" / p["wiki_page"] / f.name)
                    written.append(f"media/{p['wiki_page']}/{f.name}")
    put("Home.md", render_home(man))
    put("_Sidebar.md", render_sidebar(man))
    put("_Footer.md", render_footer(man))
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    put("Changelog.md", rewrite_links(changelog, ROOT / "CHANGELOG.md", man, pages, None))
    return written


def make_pdfs(man: dict, built: Path) -> Path:
    out = ROOT / "releases" / f"Rev{man['revision']}"
    out.mkdir(parents=True, exist_ok=True)
    css = ROOT / "Scripts" / "pdf.css"
    for p in man["pages"]:
        md = built / f"{p['wiki_page']}.md"
        pdf = out / f"NCDP_{p['wiki_page']}_Rev{man['revision']}.pdf"
        cmd = ["pandoc", str(md), "-o", str(pdf), "--pdf-engine=weasyprint", "--resource-path", str(built),
               "--metadata", f"pagetitle=NCDP — {p['title']}"]
        if css.is_file():
            cmd += ["--css", str(css)]
        subprocess.run(cmd, check=True)
        print(f"pdf  {pdf.relative_to(ROOT)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki", type=Path, default=ROOT.parent / "ncdp-standards.wiki")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pdf", action="store_true")
    args = ap.parse_args()
    man = load_manifest()
    errs = check(man)
    if errs:
        print("publish.yaml has problems:\n  " + "\n  ".join(errs))
        return 1
    if args.check:
        print(f"publish.yaml ok: revision {man['revision']}, {len(man['pages'])} pages")
        return 0
    (ROOT / "docs" / "STATUS.md").write_text(render_status(man), encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        written = build(man, tmp)
        if args.dry_run or not args.wiki.is_dir():
            if not args.wiki.is_dir() and not args.dry_run:
                print(f"wiki checkout {args.wiki} not found; clone it first (see README). Dry run instead.")
            for rel in written:
                old = args.wiki / rel
                state = "new" if not old.exists() else ("same" if filecmp.cmp(old, tmp / rel, shallow=False) else "changed")
                print(f"{state:8} {rel}")
        else:
            for rel in written:
                (args.wiki / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tmp / rel, args.wiki / rel)
            print(f"wrote {len(written)} files into {args.wiki} (revision {man['revision']}); review, commit and push there")
        if args.pdf:
            make_pdfs(man, tmp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
