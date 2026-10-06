from pathlib import Path

from toril_knowledge.source_inventory import (
    build_source_inventory,
    infer_edition,
    infer_publication_year,
    infer_source_type,
    normalize_source_title,
    product_code,
)


def test_source_metadata_inference():
    assert infer_source_type(
        "1998-04 - Evermeet - Island of the Elves - Elaine Cunningham.md"
    ) == "novel"
    assert infer_publication_year(
        "1998-04 - Evermeet - Island of the Elves - Elaine Cunningham.md"
    ) == 1998
    assert infer_source_type("Forgotten Realms Campaign Setting (11836 3e).md") == "campaign_setting"
    assert infer_edition("Forgotten Realms Campaign Setting (11836 3e).md") == "3e"
    assert product_code("Forgotten Realms Campaign Setting (11836 3e).md") == "11836-3e"


def test_duplicate_suffixes_share_source_key():
    base = normalize_source_title("Volo's Guide to All Things Magical.md")
    assert normalize_source_title("Volo's Guide to All Things Magical copy.md") == base
    assert normalize_source_title("Volo's Guide to All Things Magical (1).md") == base
    assert normalize_source_title("Volo's Guide to All Things Magical_1.md") == base


def test_inventory_deduplicates_by_hash_and_pairs_pdf(tmp_path: Path):
    canonical = tmp_path / "Forgotten Realms Campaign Setting (11836 3e).md"
    duplicate = tmp_path / "Forgotten Realms Campaign Setting (11836 3e) (1).md"
    pdf = tmp_path / "pdfs" / "Forgotten Realms Campaign Setting (11836 3e).pdf"
    pdf.parent.mkdir()

    canonical.write_text("# Calimshan\nImports grain.", encoding="utf-8")
    duplicate.write_text("# Calimshan\nImports grain.", encoding="utf-8")
    pdf.write_bytes(b"%PDF test")

    inventory = build_source_inventory(tmp_path)
    summary = inventory["summary"]
    assert summary["markdown_files"] == 2
    assert summary["pdf_files"] == 1
    assert summary["canonical_markdowns"] == 1
    assert summary["paired_canonical_markdowns"] == 1
    assert summary["exact_duplicate_markdown_groups"] == 1

    md_records = [row for row in inventory["records"] if row["role"] == "markdown"]
    assert sum(row["canonical"] for row in md_records) == 1
    assert {row["duplicate_status"] for row in md_records} == {"canonical", "exact_duplicate"}
    assert all(row["paired_path"] for row in md_records)


def test_title_collision_requires_review(tmp_path: Path):
    first = tmp_path / "Book.md"
    second = tmp_path / "Book copy.md"
    first.write_text("version one", encoding="utf-8")
    second.write_text("version two", encoding="utf-8")

    inventory = build_source_inventory(tmp_path)
    md_records = [row for row in inventory["records"] if row["role"] == "markdown"]
    assert inventory["summary"]["title_collision_markdown_groups"] == 1
    assert not any(row["canonical"] for row in md_records)
    assert all(row["duplicate_status"] == "title_collision_review" for row in md_records)
