"""Preview simple overlapping chunks for RAG experiments."""

from __future__ import annotations

import argparse
from bisect import bisect_right
import json
from pathlib import Path


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    compact: list[str] = []
    blank = False
    for line in lines:
        if not line:
            if not blank:
                compact.append("")
            blank = True
        else:
            compact.append(line)
            blank = False
    return "\n".join(compact).strip()


def make_chunks(text: str, chunk_size: int, overlap: int) -> list[tuple[int, int, str]]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[tuple[int, int, str]] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        window = text[start:end]
        if end < len(text):
            cut = max(window.rfind("\n\n"), window.rfind("。"), window.rfind(". "))
            if cut > chunk_size * 0.5:
                end = start + cut + 1
                window = text[start:end]
        chunk = window.strip()
        if chunk:
            chunks.append((start, end, chunk))
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks


def line_offsets(text: str) -> list[int]:
    offsets: list[int] = []
    pos = 0
    for line in text.splitlines(keepends=True):
        offsets.append(pos)
        pos += len(line)
    return offsets or [0]


def markdown_headings(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    pos = 0
    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append((pos, stripped.lstrip("#").strip()))
        pos += len(line)
    return headings


def section_at(headings: list[tuple[int, str]], offset: int) -> str:
    section = "root"
    for heading_offset, title in headings:
        if heading_offset > offset:
            break
        section = title
    return section


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--chunk-size", type=int, default=900)
    parser.add_argument("--overlap", type=int, default=120)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    text = normalize_text(in_path.read_text(encoding="utf-8"))
    chunks = make_chunks(text, args.chunk_size, args.overlap)
    offsets = line_offsets(text)
    headings = markdown_headings(text)

    with out_path.open("w", encoding="utf-8") as f:
        for idx, (start, end, chunk) in enumerate(chunks):
            record = {
                "id": f"{in_path.stem}-{idx:04d}",
                "source": str(in_path),
                "section": section_at(headings, start),
                "chunk_index": idx,
                "line_start": bisect_right(offsets, start),
                "line_end": bisect_right(offsets, max(start, end - 1)),
                "text": chunk,
                "preview": chunk[:160].replace("\n", " "),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(json.dumps({"chunks": len(chunks), "output": str(out_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
