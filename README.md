 # Two Provider Cost Tracker

A Python CLI script built with `uv` that sends the same prompt to **Google Gemini** and **Groq**, displays each reply alongside token counts, response latency, and estimated USD cost, and saves the structured output to `results.json`.

## Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) package manager
- Free API keys for [Google AI Studio (Gemini)](https://aistudio.google.com/) and [Groq Console](https://console.groq.com/)

## Setup & Installation

1. Clone the repository and enter the project folder:
   ```bash
   git clone [https://github.com/Ahsan2026/cost-tracker.git](https://github.com/Ahsan2026/cost-tracker.git)
   cd cost-tracker
   ```

2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

3. Create a `.env` file in the root directory (copy from `.env.example`) and configure the required environment variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_MODEL=gemini-3.5-flash-lite
   GROQ_MODEL=openai/gpt-oss-20b
   ```

## How to Run

Pass your prompt as a command-line argument to `tracker.py`:

```bash
uv run tracker.py "Explain tokens in one sentence."
```

## Sample Output

```text
=== gemini (gemini-3.5-flash-lite) ===
Tokens are chunks of text—ranging from characters to words—that AI models use to process and understand language.

=== groq (openai/gpt-oss-20b) ===
Tokens are the smallest discrete units of text—usually subword segments, words, or punctuation marks—that a language model encodes, processes, and predicts to understand and generate language.

provider | input_tokens | output_tokens | seconds | cost_usd
gemini | 7 | 22 | 7.165 | $0.00001425 (free tier est.)
groq | 77 | 105 | 0.570 | $0.00012838 (free tier est.)
```

Each run also writes the provider metadata, token counts, pricing, and calculated cost to `results.json`.

 