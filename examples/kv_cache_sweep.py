"""Sweep KV cache memory estimates and write a CSV table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from estimate_kv_cache import estimate_kv_cache_bytes


def parse_ints(raw: str) -> list[int]:
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", type=int, required=True)
    parser.add_argument("--heads", type=int, required=True)
    parser.add_argument("--kv-heads", type=int, required=True)
    parser.add_argument("--head-dim", type=int, required=True)
    parser.add_argument("--seq-lens", default="1024,2048,4096,8192,16384")
    parser.add_argument("--batch-sizes", default="1,2,4,8,16")
    parser.add_argument("--dtype-bytes", type=int, default=2)
    parser.add_argument("--output", default="benchmarks/kv-cache-sweep.csv")
    args = parser.parse_args()

    seq_lens = parse_ints(args.seq_lens)
    batch_sizes = parse_ints(args.batch_sizes)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "layers",
                "heads",
                "kv_heads",
                "head_dim",
                "seq_len",
                "batch_size",
                "dtype_bytes",
                "kv_cache_gib",
            ],
        )
        writer.writeheader()
        for seq_len in seq_lens:
            for batch_size in batch_sizes:
                total = estimate_kv_cache_bytes(
                    layers=args.layers,
                    kv_heads=args.kv_heads,
                    head_dim=args.head_dim,
                    seq_len=seq_len,
                    batch_size=batch_size,
                    dtype_bytes=args.dtype_bytes,
                )
                writer.writerow(
                    {
                        "layers": args.layers,
                        "heads": args.heads,
                        "kv_heads": args.kv_heads,
                        "head_dim": args.head_dim,
                        "seq_len": seq_len,
                        "batch_size": batch_size,
                        "dtype_bytes": args.dtype_bytes,
                        "kv_cache_gib": round(total / (1024**3), 3),
                    }
                )

    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()

