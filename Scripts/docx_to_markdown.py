#!/usr/bin/env python3
"""
Convert a Word document (e.g. the NCDP Field Manual) to a draft page in docs/, with its
images in docs/<name>_media/. Uses pandoc, which keeps tables (as HTML where cells are
merged). Then tidies the result for the wiki:
  - drops the Word table of contents (the wiki has the headings) and empty headings;
  - flattens and shrinks images (longest side <= 1600 px; large opaque PNGs -> JPEG);
    EMF/WMF drawings are converted to PNG with LibreOffice when it is installed;
  - turns Word image sizes (inches) into pixel widths;
  - repairs e-mail links that Word stored as SharePoint paths;
  - gives the page a "# Title" heading if it has none.
Check headings and tables afterwards, then add the page to publish.yaml.

  python Scripts/docx_to_markdown.py "NCDP_Field_Manual.docx" docs/field-manual.md --title "NCDP Field Manual"

Needs pandoc and Pillow; LibreOffice optional (for EMF/WMF).
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

MAX_PX = 1600


def convert(src: Path, dest: Path, title: str | None) -> None:
    media = dest.with_name(dest.stem + "_media")
    if media.exists():
        shutil.rmtree(media)
    media.mkdir(parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        subprocess.run(["pandoc", str(src), "-t", "gfm", "--wrap=none", f"--extract-media={tmp}",
                        "-o", str(tmp / "out.md")], check=True)
        md = (tmp / "out.md").read_text(encoding="utf-8")
        renamed = {}
        for f in sorted((tmp / "media").glob("*")) if (tmp / "media").is_dir() else []:
            out = media / f.name
            if f.suffix.lower() in (".emf", ".wmf"):
                if shutil.which("soffice"):
                    subprocess.run(["soffice", "--headless", "--convert-to", "png", "--outdir", str(tmp), str(f)],
                                   check=False, capture_output=True)
                    png = tmp / (f.stem + ".png")
                    if png.is_file():
                        f, out = png, media / png.name
                else:
                    print(f"  {f.name}: EMF/WMF left as is (install LibreOffice to convert)")
            if f.suffix.lower() in (".png", ".jpg", ".jpeg"):
                im = Image.open(f)
                if max(im.size) > MAX_PX:
                    im.thumbnail((MAX_PX, MAX_PX))
                opaque = im.mode in ("RGB", "L", "P") and "transparency" not in im.info
                if f.suffix.lower() == ".png" and opaque and f.stat().st_size > 400_000:
                    out = media / (f.stem + ".jpg")
                    im.convert("RGB").save(out, "JPEG", quality=85, optimize=True)
                elif out.suffix.lower() in (".jpg", ".jpeg"):
                    im.convert("RGB").save(out, "JPEG", quality=85, optimize=True)
                else:
                    im.save(out, optimize=True)
            else:
                shutil.copy2(f, out)
            renamed[f"media/{Path(f.name).stem}"] = out.name
        # image paths: <tmp>/media/imageN.ext -> <name>_media/<new name>
        def path_sub(m):
            stem = Path(m.group(1)).stem
            return f"{media.name}/{renamed.get('media/' + stem, Path(m.group(1)).name)}"
        md = re.sub(re.escape(str(tmp)) + r"/(media/[^\s\"')]+)", path_sub, md)
        # Word sizes in inches -> pixel width (96 dpi); GitHub ignores style attributes
        md = re.sub(r'style="width:([\d.]+)in;height:[\d.]+in"',
                    lambda m: f'width="{round(float(m.group(1)) * 96)}"', md)
        # e-mail links Word stored as SharePoint paths
        md = re.sub(r'https://[^"\s)]*?/([\w.+-]+@[\w-]+\.[\w.]+)', r"mailto:\1", md)
        # drop the Word table of contents (up to the next level-1 heading) and empty headings
        md = re.sub(r"^# Table of Contents\n.*?(?=^# )", "", md, flags=re.S | re.M)
        md = re.sub(r"^#+\s*$\n", "", md, flags=re.M)
        if title and not md.lstrip().startswith("# "):
            md = f"# {title}\n\n" + md
        dest.write_text(md, encoding="utf-8")
    size = sum(p.stat().st_size for p in media.iterdir()) / 1e6
    print(f"{dest}: {len(md.splitlines())} lines; {len(list(media.iterdir()))} images ({size:.1f} MB) in {media}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("docx", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("--title")
    a = ap.parse_args()
    convert(a.docx, a.dest, a.title)
