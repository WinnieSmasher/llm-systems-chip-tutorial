"""Estimate KV cache memory for a decoder-only Transformer.

The common intuition formula is:

    2 * layers * batch * seq_len * kv_heads * head_dim * bytes

The factor 2 is for K and V. This is still an approximation: real serving
systems add allocator overhead, block padding, tensor parallel layout, and
framework-specific bookkeeping.
"""

from __future__ import annotations

import argparse


def bytes_to_gib(num_bytes: float) -> float:
    return num_bytes / (1024**3)


def estimate_kv_cache_bytes(
    layers: int,
    kv_heads: int,
    head_dim: int,
    seq_len: int,
    batch_size: int,
    dtype_bytes: int,
) -> int:
    return 2 * layers * batch_size * seq_len * kv_heads * head_dim * dtype_bytes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layers", type=int, required=True)
    parser.add_argument("--heads", type=int, required=True, help="Attention heads; used for reporting.")
    parser.add_argument("--kv-heads", type=int, required=True, help="KV heads after GQA/MQA.")
    parser.add_argument("--head-dim", type=int, required=True)
    parser.add_argument("--seq-len", type=int, required=True)
    parser.add_argument("--batch-size", type=int, required=True)
    parser.add_argument("--dtype-bytes", type=int, default=2, help="2 for fp16/bf16, 1 for int8.")
    args = parser.parse_args()

    total = estimate_kv_cache_bytes(
        layers=args.layers,
        kv_heads=args.kv_heads,
        head_dim=args.head_dim,
        seq_len=args.seq_len,
        batch_size=args.batch_size,
        dtype_bytes=args.dtype_bytes,
    )

    print("KV cache estimate")
    print(f"  layers:      {args.layers}")
    print(f"  heads:       {args.heads}")
    print(f"  kv_heads:    {args.kv_heads}")
    print(f"  head_dim:    {args.head_dim}")
    print(f"  seq_len:     {args.seq_len}")
    print(f"  batch_size:  {args.batch_size}")
    print(f"  dtype_bytes: {args.dtype_bytes}")
    print(f"  memory:      {bytes_to_gib(total):.2f} GiB")


if __name__ == "__main__":
    main()

