from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .router import route_text


@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    id: str
    heading: str
    text: str
    relevant: frozenset[str]
    forbidden: frozenset[str] = frozenset()
    k: int = 6
    source_profile: str | None = None


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    case_id: str
    predicted: tuple[str, ...]
    relevant: frozenset[str]
    precision_at_k: float
    recall_at_k: float
    forbidden_hits: tuple[str, ...]


def load_benchmarks(path: str | Path) -> list[BenchmarkCase]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = data.get("cases", data)
    return [
        BenchmarkCase(
            id=item["id"],
            heading=item.get("heading", ""),
            text=item["text"],
            relevant=frozenset(item["relevant"]),
            forbidden=frozenset(item.get("forbidden", [])),
            k=int(item.get("k", 6)),
            source_profile=item.get("source_profile"),
        )
        for item in cases
    ]


def evaluate_case(case: BenchmarkCase) -> BenchmarkResult:
    routes = route_text(case.heading, case.text, layer="domain", top_k=case.k)
    predicted = tuple(route.pack_id for route in routes)
    predicted_set = set(predicted)
    true_positives = len(predicted_set.intersection(case.relevant))
    precision = true_positives / max(1, len(predicted))
    recall = true_positives / max(1, len(case.relevant))
    forbidden_hits = tuple(pack_id for pack_id in predicted if pack_id in case.forbidden)
    return BenchmarkResult(
        case_id=case.id,
        predicted=predicted,
        relevant=case.relevant,
        precision_at_k=precision,
        recall_at_k=recall,
        forbidden_hits=forbidden_hits,
    )


def evaluate_benchmarks(cases: Iterable[BenchmarkCase]) -> dict:
    results = [evaluate_case(case) for case in cases]
    if not results:
        return {
            "cases": [],
            "macro_precision_at_k": 0.0,
            "macro_recall_at_k": 0.0,
            "forbidden_hits": 0,
        }
    return {
        "cases": [
            {
                "case_id": result.case_id,
                "predicted": list(result.predicted),
                "relevant": sorted(result.relevant),
                "precision_at_k": round(result.precision_at_k, 4),
                "recall_at_k": round(result.recall_at_k, 4),
                "forbidden_hits": list(result.forbidden_hits),
            }
            for result in results
        ],
        "macro_precision_at_k": round(
            sum(result.precision_at_k for result in results) / len(results), 4
        ),
        "macro_recall_at_k": round(
            sum(result.recall_at_k for result in results) / len(results), 4
        ),
        "forbidden_hits": sum(len(result.forbidden_hits) for result in results),
    }
