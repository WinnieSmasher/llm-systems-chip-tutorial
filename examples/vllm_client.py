"""Minimal client for a local vLLM OpenAI-compatible server.

Start a server first:

    vllm serve Qwen/Qwen2.5-0.5B-Instruct
"""

from __future__ import annotations

import time

from openai import OpenAI


MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"


def main() -> None:
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

    start = time.perf_counter()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": "用四句话解释 KV Cache 为什么影响 LLM 推理显存。",
            }
        ],
        temperature=0,
        max_tokens=256,
    )
    elapsed = time.perf_counter() - start

    print(response.choices[0].message.content)
    print(f"\nlatency_seconds={elapsed:.3f}")
    if response.usage:
        print(response.usage)


if __name__ == "__main__":
    main()

