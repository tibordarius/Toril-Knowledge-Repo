from pathlib import Path

from toril_knowledge.pipeline import Section, parse_markdown, semantic_chunks


def test_parser_tracks_headings_and_pages(tmp_path: Path):
    path = tmp_path / "book.md"
    path.write_text(
        "Intro text\n\n# Cities\n<!-- page: 10 -->\nOverview.\n\n## Waterdeep\n<!-- page: 11 -->\nHarbor text.\n",
        encoding="utf-8",
    )
    sections = parse_markdown(path)
    assert sections[0].heading == "(preamble)"
    assert sections[1].heading == "Cities"
    assert sections[1].page_start == 10
    assert sections[2].heading == "Cities > Waterdeep"
    assert sections[2].page_start == 11


def test_semantic_chunking_groups_small_sections():
    sections = [
        Section("A", "a" * 400, 1, 1),
        Section("B", "b" * 400, 2, 2),
        Section("C", "c" * 400, 3, 3),
    ]
    chunks = semantic_chunks(
        sections,
        "book",
        "book.md",
        max_chars=1000,
        min_chars=700,
        overlap=50,
    )
    assert len(chunks) == 2
    assert chunks[0].page_start == 1
    assert chunks[0].page_end == 2
