"""Clean small SFT JSONL files and write a quality report.

Supported input schemas:

1. {"messages": [{"role": "user", "content": "..."}, ...]}
2. {"instruction": "...", "input": "...", "output": "..."}

This script is deliberately conservative. It is meant for early project
sanity checks before you run TRL/PEFT training.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


VALID_ROLES = {"system", "user", "assistant"}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).replace("\u3000", " ").split())


def instruction_to_messages(record: dict[str, Any]) -> list[dict[str, str]]:
    instruction = normalize_text(record.get("instruction"))
    extra_input = normalize_text(record.get("input"))
    output = normalize_text(record.get("output"))

    user_parts = [part for part in [instruction, extra_input] if part]
    user_text = "\n\n".join(user_parts)
    return [
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": output},
    ]


def normalize_messages(record: dict[str, Any]) -> tuple[list[dict[str, str]] | None, str | None]:
    if "messages" in record:
        raw_messages = record["messages"]
        if not isinstance(raw_messages, list):
            return None, "messages_not_list"

        messages: list[dict[str, str]] = []
        for item in raw_messages:
            if not isinstance(item, dict):
                return None, "message_not_object"
            role = normalize_text(item.get("role"))
            content = normalize_text(item.get("content"))
            if role not in VALID_ROLES:
                return None, "invalid_role"
            messages.append({"role": role, "content": content})
    elif "instruction" in record and "output" in record:
        messages = instruction_to_messages(record)
    else:
        return None, "unsupported_schema"

    if not messages:
        return None, "empty_messages"
    if not any(msg["role"] == "user" for msg in messages):
        return None, "missing_user"
    if not any(msg["role"] == "assistant" for msg in messages):
        return None, "missing_assistant"
    if any(not msg["content"] for msg in messages):
        return None, "empty_content"

    last_role = None
    for msg in messages:
        role = msg["role"]
        if role == last_role and role != "system":
            return None, "repeated_role"
        last_role = role

    return messages, None


def fingerprint(messages: list[dict[str, str]]) -> str:
    payload = json.dumps(messages, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--min-chars", type=int, default=8)
    parser.add_argument("--max-chars", type=int, default=8000)
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    report_path = Path(args.report)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    counters: dict[str, int] = {
        "total": 0,
        "kept": 0,
        "duplicate": 0,
        "too_short": 0,
        "too_long": 0,
        "json_error": 0,
    }
    reject_reasons: dict[str, int] = {}
    lengths: list[int] = []

    with in_path.open("r", encoding="utf-8") as src, out_path.open("w", encoding="utf-8") as dst:
        for line_no, line in enumerate(src, start=1):
            line = line.strip()
            if not line:
                continue

            counters["total"] += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                counters["json_error"] += 1
                reject_reasons["json_error"] = reject_reasons.get("json_error", 0) + 1
                continue

            if not isinstance(record, dict):
                reject_reasons["record_not_object"] = reject_reasons.get("record_not_object", 0) + 1
                continue

            messages, reason = normalize_messages(record)
            if reason is not None or messages is None:
                key = reason or "unknown"
                reject_reasons[key] = reject_reasons.get(key, 0) + 1
                continue

            total_chars = sum(len(msg["content"]) for msg in messages)
            if total_chars < args.min_chars:
                counters["too_short"] += 1
                reject_reasons["too_short"] = reject_reasons.get("too_short", 0) + 1
                continue
            if total_chars > args.max_chars:
                counters["too_long"] += 1
                reject_reasons["too_long"] = reject_reasons.get("too_long", 0) + 1
                continue

            digest = fingerprint(messages)
            if digest in seen:
                counters["duplicate"] += 1
                reject_reasons["duplicate"] = reject_reasons.get("duplicate", 0) + 1
                continue
            seen.add(digest)

            dst.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
            counters["kept"] += 1
            lengths.append(total_chars)

    report = {
        **counters,
        "reject_reasons": reject_reasons,
        "length_chars": {
            "min": min(lengths) if lengths else None,
            "max": max(lengths) if lengths else None,
            "mean": round(sum(lengths) / len(lengths), 2) if lengths else None,
        },
        "input": str(in_path),
        "output": str(out_path),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

