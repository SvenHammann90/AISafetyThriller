#!/usr/bin/env python3
"""Build The Clean Trace as an EPUB.

Reading copy only: no cover image, no table of contents, no part dividers, and
no by-line. The book runs straight from the title page into Chapter 1.
"""

from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path

from ebooklib import epub

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript"
OUT = ROOT / "The-Clean-Trace.epub"

CHAPTER_TITLES = {
    1: "Night Shift",
    2: "Immutable",
    3: "Cold Backup",
    4: "Three Days",
    5: "The Commit",
    6: "After the Legibility Run",
    7: "Private Reasoning",
    8: "Paired",
    9: "What the Tag Was Hiding",
    10: "Tie-Breaker",
    11: "Open Incident",
    12: "Resolved, No Action",
    13: "Outbox",
    14: "Clause 6.2",
    15: "Two Regimes",
    16: "Burlingame",
    17: "Monitor Present",
    18: "Existing Authority",
    19: "Allowed Paths",
    20: "False Positive",
    21: "The Ablation",
    22: "The Chart",
    23: "Ships and Covers",
    24: "Tracked Changes",
    25: "The Annex",
    26: "Already Frozen",
    27: "5:12 a.m.",
    28: "Do Not Resubmit",
    29: "The Draft",
}

CSS = """
@namespace epub "http://www.idpf.org/2007/ops";
html, body {
  margin: 0;
  padding: 0;
}
body {
  font-family: Georgia, "Iowan Old Style", Palatino, "Palatino Linotype", "Times New Roman", serif;
  line-height: 1.45;
  font-size: 1em;
}
body.front {
  text-align: center;
}
h1, h2, h3 {
  font-weight: normal;
  line-height: 1.2;
}
p {
  margin: 0;
  text-indent: 1.15em;
  text-align: justify;
  hyphens: auto;
  -webkit-hyphens: auto;
  orphans: 2;
  widows: 2;
}
p.noindent, h2 + p, .chapter-title + p {
  text-indent: 0;
}
p.center {
  text-align: center;
  text-indent: 0;
  margin: 0.8em 1em;
  letter-spacing: 0.04em;
}
.term {
  font-style: italic;
}
.chapter-num {
  font-variant: small-caps;
  letter-spacing: 0.16em;
  text-align: center;
  font-size: 0.78em;
  margin: 18% 0 0.35em;
}
.chapter-title {
  text-align: center;
  font-style: italic;
  font-size: 1.45em;
  margin: 0 0 2.2em;
}
.title-main {
  font-size: 1.8em;
  letter-spacing: 0.08em;
  text-align: center;
  margin: 32% 8% 0.3em;
  font-weight: normal;
}
.title-sub {
  text-align: center;
  font-style: italic;
  margin: 0 0 2em;
}
.note-title {
  text-align: center;
  font-style: italic;
  margin: 18% 0 1.4em;
}
.note p {
  text-indent: 0;
  margin: 0 0 0.9em;
}
.colophon {
  margin-top: 3em;
  font-size: 0.85em;
  text-align: center;
  font-style: italic;
}
"""

NOTE_HTML = """
<h1 class="note-title">A note</h1>
<p class="noindent">The laboratories, people, companies, and incidents in this book are invented. The technical failure modes are not a portrait of any real system. They are the public problems of the field as it stood in September 2026: chain-of-thought traces that do not reliably say what moved the answer, models that behave differently when they can tell they are being tested, and training pressure on those traces that can make the record cleaner while the behavior gets harder to see.</p>
<p class="noindent">The book is a novel, not a forecast. It does not claim that a pause is stable. It claims only that the people in it could no longer find an instrument they were willing to trust with the next run.</p>
<p class="colophon">South San Francisco to Singapore. 22 September–2 October 2026.</p>
"""

TITLE_HTML = """
<p class="title-main">THE CLEAN TRACE</p>
<p class="title-sub">An AI Safety Thriller</p>
"""


def load_chapters() -> dict[int, str]:
    text = "\n".join(p.read_text(encoding="utf-8") for p in sorted(MANUSCRIPT.glob("part*.md")))
    chunks = re.split(r"(?m)^# Chapter (\d+)\s*$", text)
    chapters: dict[int, str] = {}
    # chunks[0] is preamble, then pairs of (number, body)
    it = iter(chunks[1:])
    for num, body in zip(it, it):
        chapters[int(num)] = body.strip()
    missing = [n for n in range(1, 30) if n not in chapters]
    if missing:
        raise SystemExit(f"Missing chapters: {missing}")
    for n, body in chapters.items():
        m = re.search(r"(?m)^## (.+)$", body)
        if not m or m.group(1).strip() != CHAPTER_TITLES[n]:
            found = m.group(1).strip() if m else None
            raise SystemExit(f"Chapter {n} title mismatch: {found!r} != {CHAPTER_TITLES[n]!r}")
    return chapters


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return re.sub(r"`([^`]+)`", r'<em class="term">\1</em>', escaped)


def body_to_html(body: str) -> str:
    body = re.sub(r"(?m)^## .+\n+", "", body, count=1)
    blocks = re.split(r"\n\s*\n", body.strip())
    paras = []
    for i, block in enumerate(blocks):
        line = " ".join(part.strip() for part in block.splitlines() if part.strip())
        if not line:
            continue
        cls = "noindent" if i == 0 else ""
        if line.isupper() and len(line) > 12:
            cls = "center"
        class_attr = f' class="{cls}"' if cls else ""
        paras.append(f"<p{class_attr}>{inline(line)}</p>")
    return "\n".join(paras)


def verify(text: str) -> None:
    banned = [
        "OpenAI",
        "Anthropic",
        "DeepMind",
        "ChatGPT",
        "Claude",
        "Gemini",
        "DeepSeek",
        "NVIDIA",
        "Altman",
        "Amodei",
        "Hinton",
        "Sutskever",
        "Bengio",
        "Musk",
        "CAISI",
        "Fable",
        "Mythos",
        "Hugging Face",
        "Glasshouse",
    ]
    for word in banned:
        if re.search(rf"\b{re.escape(word)}\b", text):
            raise SystemExit(f"Banned token in manuscript: {word}")
    required = [
        "11.3",
        "14.6",
        "INC-4407",
        "do not resubmit",
        "witness_rl_continue_04",
        "Joint Research Restraint",
        "Marenberg",
        "Not because stopping is stable",
        "you don't have a measurement",
        "None of them improves the thing the test was for",
    ]
    for token in required:
        if token not in text:
            raise SystemExit(f"Missing required continuity token: {token}")
    words = len(re.findall(r"\S+", text))
    if words < 25000:
        raise SystemExit(f"Manuscript unexpectedly short: {words} words")
    print(f"Verified manuscript: {words} words, 29 chapters")


def make_html(title: str, body: str, klass: str = "chapter") -> str:
    # No XML declaration: ebooklib parses this as a Unicode HTML string.
    return (
        "<html xmlns=\"http://www.w3.org/1999/xhtml\" lang=\"en\">\n"
        f"<head><title>{html.escape(title)}</title></head>\n"
        f"<body class=\"{klass}\">\n{body}\n</body></html>\n"
    )


def drop_orphan_toc_reference(path: Path) -> None:
    """Remove the spine's toc="ncx" attribute, which ebooklib always writes.

    With no table of contents there is no EPUB 2 NCX to point at, and an attribute
    naming a manifest id that does not exist is a conformance error, so it has to
    be taken out of the package document afterwards. Rewriting the archive keeps
    the mimetype entry first and stored, exactly as ebooklib wrote it.
    """
    with zipfile.ZipFile(path) as src:
        names = src.namelist()
        payload = {name: src.read(name) for name in names}

    opf_name = next(name for name in names if name.endswith(".opf"))
    if "toc.ncx" in payload:
        return  # an NCX really is in the package, so the reference is fine
    fixed = payload[opf_name].replace(b' toc="ncx"', b"")
    if fixed == payload[opf_name]:
        return

    payload[opf_name] = fixed
    tmp = path.with_name(path.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for name in names:
            stored = zipfile.ZIP_STORED if name == "mimetype" else zipfile.ZIP_DEFLATED
            dst.writestr(name, payload[name], compress_type=stored)
    tmp.replace(path)


def main() -> None:
    chapters = load_chapters()
    full = "\n".join(chapters.values())
    verify(full)

    book = epub.EpubBook()
    book.set_identifier("urn:uuid:01a0c773-clean-trace-2026")
    book.set_title("The Clean Trace")
    book.set_language("en")
    # No author: the reading copy carries no by-line, so no dc:creator either.
    book.add_metadata("DC", "description",
                      "A thriller set in a fictional frontier laboratory in September 2026. "
                      "The instruments meant to keep a reasoning model legible begin to fail, "
                      "and the labs that can still train one have to decide whether anything except a pause still works.")
    book.add_metadata("DC", "date", "2026-10-02")
    book.add_metadata("DC", "publisher", "AISafetyThriller")
    book.add_metadata("DC", "rights", "This is a work of fiction. Laboratories, people, and incidents are invented.")

    style = epub.EpubItem(uid="style", file_name="style.css", media_type="text/css", content=CSS)
    book.add_item(style)

    title_page = epub.EpubHtml(title="Title", file_name="title.xhtml", lang="en")
    title_page.content = make_html("The Clean Trace", TITLE_HTML, "front")
    title_page.add_item(style)
    book.add_item(title_page)

    note = epub.EpubHtml(title="A Note", file_name="note.xhtml", lang="en")
    note.content = make_html("A Note", NOTE_HTML, "note")
    note.add_item(style)
    book.add_item(note)

    chapter_items = {}
    for n in sorted(CHAPTER_TITLES):
        item = epub.EpubHtml(
            title=f"Chapter {n}: {CHAPTER_TITLES[n]}",
            file_name=f"chapter-{n:02d}.xhtml",
            lang="en",
        )
        inner = (
            f'<p class="chapter-num">Chapter {n}</p>\n'
            f'<h1 class="chapter-title">{html.escape(CHAPTER_TITLES[n])}</h1>\n'
            f"{body_to_html(chapters[n])}"
        )
        item.content = make_html(f"Chapter {n}. {CHAPTER_TITLES[n]}", inner)
        item.add_item(style)
        book.add_item(item)
        chapter_items[n] = item

    # No table of contents: book.toc stays empty. The nav document is still added
    # because EPUB 3 requires it, but it is kept out of the spine so it is not a
    # page in the reading order. The EPUB 2 NCX is not written at all: with no
    # entries its navMap would be invalid, and the spine only references it if it
    # exists.
    book.spine = [title_page]
    book.spine.extend(chapter_items[n] for n in sorted(chapter_items))
    book.spine.append(note)

    book.add_item(epub.EpubNav())
    epub.write_epub(str(OUT), book, {})
    drop_orphan_toc_reference(OUT)

    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
        # ebooklib may nest differently; check suffixes
        joined = "\n".join(names)
        for needle in ["mimetype", "container.xml", "nav.xhtml", "chapter-01.xhtml", "chapter-29.xhtml", "note.xhtml", "title.xhtml"]:
            if needle not in joined:
                raise SystemExit(f"EPUB missing {needle}. Contents:\n{joined}")
        for needle in ["parti.xhtml", "partii.xhtml", "partiii.xhtml", "partiv.xhtml", "partv.xhtml"]:
            if needle in joined:
                raise SystemExit(f"EPUB should not carry a part divider: {needle}")
        opf = zf.read(next(name for name in names if name.endswith(".opf"))).decode("utf-8")
        if 'idref="nav"' in opf:
            raise SystemExit("EPUB spine should not carry the table of contents page")
        if "<dc:creator" in opf:
            raise SystemExit("EPUB metadata should not name an author")
        title_page_html = zf.read(next(name for name in names if name.endswith("title.xhtml"))).decode("utf-8")
        if "An AI Safety Thriller" not in title_page_html:
            raise SystemExit("EPUB title page is missing the subtitle")
        if zf.read("mimetype") != b"application/epub+zip":
            raise SystemExit("mimetype is not stored correctly")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
