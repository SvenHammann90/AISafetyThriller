#!/usr/bin/env python3
"""Build The Clean Trace as an EPUB. No cover image."""

from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path

from ebooklib import epub

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript"
OUT = ROOT / "The-Clean-Trace.epub"

PARTS = [
    ("Part I", "The Green Board", range(1, 7)),
    ("Part II", "The Residue", range(7, 12)),
    ("Part III", "The Session", range(12, 17)),
    ("Part IV", "The Cures", range(17, 24)),
    ("Part V", "The Restraint", range(24, 30)),
]

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
p.noindent, h2 + p, .chapter-title + p, .part-kicker + p {
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
.part-kicker {
  font-variant: small-caps;
  letter-spacing: 0.18em;
  text-align: center;
  font-size: 0.78em;
  margin: 28% 0 0.4em;
}
.part-title {
  text-align: center;
  font-style: italic;
  font-size: 1.6em;
  margin: 0;
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
.title-author {
  text-align: center;
  letter-spacing: 0.12em;
  font-variant: small-caps;
  margin-top: 2.5em;
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
nav#toc ol {
  list-style: none;
  padding-left: 0;
}
nav#toc li {
  margin: 0.35em 0;
}
.toc-part {
  margin-top: 1.1em;
  font-variant: small-caps;
  letter-spacing: 0.08em;
  font-size: 0.85em;
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
<p class="title-sub">A novel</p>
<p class="title-author">Sven Hammann</p>
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


def main() -> None:
    chapters = load_chapters()
    full = "\n".join(chapters.values())
    verify(full)

    book = epub.EpubBook()
    book.set_identifier("urn:uuid:01a0c773-clean-trace-2026")
    book.set_title("The Clean Trace")
    book.set_language("en")
    book.add_author("Sven Hammann")
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
    part_items = {}
    for part_label, part_title, nums in PARTS:
        pid = part_label.lower().replace(" ", "")
        part = epub.EpubHtml(title=f"{part_label}: {part_title}", file_name=f"{pid}.xhtml", lang="en")
        part.content = make_html(
            part_title,
            f'<p class="part-kicker">{html.escape(part_label)}</p>\n'
            f'<h1 class="part-title">{html.escape(part_title)}</h1>',
            "front",
        )
        part.add_item(style)
        book.add_item(part)
        part_items[part_label] = part
        for n in nums:
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

    toc = [epub.Link("title.xhtml", "Title", "title")]
    for part_label, part_title, nums in PARTS:
        toc.append(
            (
                epub.Section(f"{part_label} — {part_title}"),
                [chapter_items[n] for n in nums],
            )
        )
    toc.append(epub.Link("note.xhtml", "A Note", "note"))
    book.toc = toc

    book.spine = ["nav", title_page]
    for part_label, _, nums in PARTS:
        book.spine.append(part_items[part_label])
        book.spine.extend(chapter_items[n] for n in nums)
    book.spine.append(note)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(str(OUT), book, {})

    with zipfile.ZipFile(OUT) as zf:
        names = zf.namelist()
        required = ["mimetype", "META-INF/container.xml", "EPUB/nav.xhtml", "EPUB/title.xhtml", "EPUB/chapter-01.xhtml", "EPUB/chapter-29.xhtml", "EPUB/note.xhtml"]
        # ebooklib may nest differently; check suffixes
        joined = "\n".join(names)
        for needle in ["mimetype", "container.xml", "nav.xhtml", "chapter-01.xhtml", "chapter-29.xhtml", "note.xhtml", "title.xhtml"]:
            if needle not in joined:
                raise SystemExit(f"EPUB missing {needle}. Contents:\n{joined}")
        if zf.read("mimetype") != b"application/epub+zip":
            raise SystemExit("mimetype is not stored correctly")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
