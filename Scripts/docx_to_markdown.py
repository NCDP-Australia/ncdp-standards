#!/usr/bin/env python3
"""
Convert a Word document (e.g. the NCDP Field Manual) to a draft page in docs/, with its
images in docs/<name>_media/. The result is a starting point: check headings and tables,
then add the page to publish.yaml (status: stub or provisional until reviewed).

  pip install mammoth
  python Scripts/docx_to_markdown.py "NCDP Field Manual.docx" docs/field-manual.md
"""
import sys
from pathlib import Path

import mammoth


def main(src: str, dest: str) -> None:
    dest = Path(dest)
    media = dest.with_name(dest.stem + "_media")
    media.mkdir(parents=True, exist_ok=True)
    count = {"n": 0}

    def image(img):
        count["n"] += 1
        ext = (img.content_type or "image/png").split("/")[-1].replace("jpeg", "jpg")
        name = f"image{count['n']:03d}.{ext}"
        with img.open() as fh:
            (media / name).write_bytes(fh.read())
        return {"src": f"{media.name}/{name}"}

    with open(src, "rb") as fh:
        res = mammoth.convert_to_markdown(fh, convert_image=mammoth.images.img_element(image))
    dest.write_text(res.value, encoding="utf-8")
    print(f"{dest}: {len(res.value.splitlines())} lines, {count['n']} images in {media}")
    for m in res.messages:
        print("  note:", m)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
