"""Small OpenAI-compatible serving benchmark.

This is a teaching benchmark for local vLLM/TGI/SGLang-compatible servers.
It intentionally uses only the Python standard library so it can run in a
fresh environment.

Example:

    vllm serve Qwen/Qwen2.5-0.5B-Instruct

    python examples/benchmark_openai_server.py \
      --model Qwen/Qwen2.5-0.5B-Instruct \
      --prompt "解释一下 KV Cache" \
      --requests 16 \
      --concurrency 4 \
      --max-tokens 128 \
      --stream
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class RequestMetric:
    ok: bool
    latency_s: float
    ttft_s: float | None
    output_chars: int
    error: str | None = None


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return float("nan")
    values = sorted(values)
    idx = min(len(values) - 1, max(0, round((len(values) - 1) * pct)))
    return values[idx]


def post_json(url: str, payload: dict[str, Any], timeout_s: int) -> bytes:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer EMPTY"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        return resp.read()


def run_non_streaming(
    url: str,
    model: str,
    prompt: str,
    max_tokens: int,
    timeout_s: int,
) -> RequestMetric:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
    }
    start = time.perf_counter()
    try:
        raw = post_json(url, payload, timeout_s)
        elapsed = time.perf_counter() - start
        data = json.loads(raw)
        content = data["choices"][0]["message"]["content"]
        return RequestMetric(True, elapsed, None, len(content))
    except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
        return RequestMetric(False, time.perf_counter() - start, None, 0, str(exc))


def run_streaming(
    url: str,
    model: str,
    prompt: str,
    max_tokens: int,
    timeout_s: int,
) -> RequestMetric:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": True,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer EMPTY"},
        method="POST",
    )

    start = time.perf_counter()
    first_token_at: float | None = None
    output_chars = 0
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8", errors="ignore").strip()
                if not line.startswith("data: "):
                    continue
                payload_text = line[len("data: ") :]
                if payload_text == "[DONE]":
                    break
                event = json.loads(payload_text)
                delta = event["choices"][0].get("delta", {})
                text = delta.get("content") or ""
                if text and first_token_at is None:
                    first_token_at = time.perf_counter()
                output_chars += len(text)
        elapsed = time.perf_counter() - start
        ttft = None if first_token_at is None else first_token_at - start
        return RequestMetric(True, elapsed, ttft, output_chars)
    except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
        return RequestMetric(False, time.perf_counter() - start, first_token_at, output_chars, str(exc))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8000/v1")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--requests", type=int, default=16)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--timeout-s", type=int, default=120)
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    url = args.base_url.rstrip("/") + "/chat/completions"
    worker = run_streaming if args.stream else run_non_streaming

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures = [
            pool.submit(worker, url, args.model, args.prompt, args.max_tokens, args.timeout_s)
            for _ in range(args.requests)
        ]
        metrics = [future.result() for future in concurrent.futures.as_completed(futures)]
    wall = time.perf_counter() - start

    ok = [m for m in metrics if m.ok]
    failed = [m for m in metrics if not m.ok]
    latencies = [m.latency_s for m in ok]
    ttfts = [m.ttft_s for m in ok if m.ttft_s is not None]
    total_chars = sum(m.output_chars for m in ok)

    result = {
        "requests": args.requests,
        "concurrency": args.concurrency,
        "ok": len(ok),
        "failed": len(failed),
        "wall_time_s": round(wall, 4),
        "latency_p50_s": round(percentile(latencies, 0.50), 4),
        "latency_p90_s": round(percentile(latencies, 0.90), 4),
        "latency_mean_s": round(statistics.mean(latencies), 4) if latencies else None,
        "ttft_p50_s": round(percentile(ttfts, 0.50), 4) if ttfts else None,
        "ttft_p90_s": round(percentile(ttfts, 0.90), 4) if ttfts else None,
        "output_chars_per_s": round(total_chars / wall, 2) if wall > 0 else None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if failed:
        print("\nFirst errors:")
        for item in failed[:3]:
            print(f"- {item.error}")


if __name__ == "__main__":
    main()

