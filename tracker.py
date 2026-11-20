import json
import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

prices = {
    "gemini": {"input": 0.15, "output": 0.60},
    "groq": {"input": 0.59, "output": 0.79},
}


def cost(tokens: int, price_per_million: float) -> float:
    return tokens * price_per_million / 1_000_000


def call_gemini(prompt: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in .env")

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    client = genai.Client(api_key=api_key)

    start = time.perf_counter()
    resp = client.models.generate_content(model=model, contents=prompt)
    elapsed = time.perf_counter() - start

    in_tokens = resp.usage_metadata.prompt_token_count or 0
    out_tokens = resp.usage_metadata.candidates_token_count or 0
    total_cost = cost(in_tokens, prices["gemini"]["input"]) + cost(out_tokens, prices["gemini"]["output"])

    return {
        "provider": "gemini",
        "model": model,
        "reply": resp.text or "",
        "input_tokens": in_tokens,
        "output_tokens": out_tokens,
        "input_price_per_m": prices["gemini"]["input"],
        "output_price_per_m": prices["gemini"]["output"],
        "cost_usd": total_cost,
        "seconds": round(elapsed, 3),
    }


def call_groq(prompt: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env")

    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    client = Groq(api_key=api_key)

    start = time.perf_counter()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.perf_counter() - start

    in_tokens = resp.usage.prompt_tokens or 0
    out_tokens = resp.usage.completion_tokens or 0
    total_cost = cost(in_tokens, prices["groq"]["input"]) + cost(out_tokens, prices["groq"]["output"])

    return {
        "provider": "groq",
        "model": model,
        "reply": resp.choices[0].message.content or "",
        "input_tokens": in_tokens,
        "output_tokens": out_tokens,
        "input_price_per_m": prices["groq"]["input"],
        "output_price_per_m": prices["groq"]["output"],
        "cost_usd": total_cost,
        "seconds": round(elapsed, 3),
    }


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: uv run tracker.py "your prompt"')
        sys.exit(1)

    prompt = sys.argv[1]

    try:
        gemini_data = call_gemini(prompt)
        groq_data = call_groq(prompt)
    except Exception as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    all_results = [gemini_data, groq_data]

    for item in all_results:
        print(f"\n=== {item['provider']} ({item['model']}) ===")
        print(item["reply"])

    print("\nprovider | input_tokens | output_tokens | seconds | cost_usd")
    for item in all_results:
        print(
            f"{item['provider']} | {item['input_tokens']} | {item['output_tokens']} | "
            f"{item['seconds']:.3f} | ${item['cost_usd']:.8f} (free tier est.)"
        )

    saved_results = [
        {k: v for k, v in item.items() if k != "seconds"}
        for item in all_results
    ]
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(saved_results, f, indent=2)


if __name__ == "__main__":
    main()