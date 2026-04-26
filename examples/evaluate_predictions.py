"""Evaluate small JSONL prediction files.

Each line may contain:

{
  "id": "case-001",
  "prediction": "...",
  "answer": "...",
  "must_have": ["term A", "term B"],
  "bad_patterns": ["wrong term"]
}

The metrics are intentionally simple. They are useful for regression checks,
not for replacing a full benchmark suite.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def normalize(text: Any) -> str:
    return " ".join(str(text or "").lower().split())


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    path = Path(args.input)
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError(f"line {line_no}: record must be an object")
            rows.append(record)

    exact = 0
    must_have_total = 0
    must_have_hit = 0
    bad_pattern_total = 0
    bad_pattern_hit = 0
    prediction_lengths: list[int] = []
    failures: list[dict[str, Any]] = []

    for record in rows:
        prediction_raw = str(record.get("prediction", ""))
        prediction = normalize(prediction_raw)
        answer = normalize(record.get("answer", ""))
        prediction_lengths.append(len(prediction_raw))

        if answer and prediction == answer:
            exact += 1

        missing_terms = []
        for term in as_list(record.get("must_have")):
            must_have_total += 1
            if normalize(term) in prediction:
                must_have_hit += 1
            else:
                missing_terms.append(term)

        triggered_bad_patterns = []
        for term in as_list(record.get("bad_patterns")):
            bad_pattern_total += 1
            if normalize(term) in prediction:
                bad_pattern_hit += 1
                triggered_bad_patterns.append(term)

        if missing_terms or triggered_bad_patterns:
            failures.append(
                {
                    "id": record.get("id"),
                    "missing_terms": missing_terms,
                    "bad_patterns": triggered_bad_patterns,
                }
            )

    count = len(rows)
    result = {
        "count": count,
        "exact_match": round(exact / count, 4) if count else None,
        "must_have_hit_rate": round(must_have_hit / must_have_total, 4)
        if must_have_total
        else None,
        "bad_pattern_rate": round(bad_pattern_hit / bad_pattern_total, 4)
        if bad_pattern_total
        else None,
        "avg_prediction_chars": round(sum(prediction_lengths) / count, 2) if count else None,
        "failures": failures[:20],
    }

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()

