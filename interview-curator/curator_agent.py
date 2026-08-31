#!/usr/bin/env python3
"""
Daily System Design & AI Engineering interview reading-list curator.

Runs the agent prompt (prompt.md) against ANY supported LLM that has live web
search, and writes the resulting 10-article brief to output/<date>.md.

Pick the provider with the PROVIDER env var (or --provider):
    anthropic | openai | gemini | perplexity

Each provider needs its own API key in the environment:
    ANTHROPIC_API_KEY | OPENAI_API_KEY | GEMINI_API_KEY | PERPLEXITY_API_KEY

Optionally override the model with the MODEL env var (or --model).

The one hard requirement: the model must have live web search. A model with no
web access cannot do this job, since the whole point is fetching today's articles.
"""

import argparse
import datetime
import os
import pathlib
import sys

PROMPT_FILE = pathlib.Path(__file__).parent / "prompt.md"
OUTPUT_DIR = pathlib.Path(__file__).parent / "output"
# Used by the anthropic adapter only. Thinking is on by default on Opus 5 and
# its tokens count against this ceiling, so leave room above the brief itself
# (~3k tokens) or the report truncates mid-article.
MAX_OUTPUT_TOKENS = 16000


def load_prompt() -> str:
    return PROMPT_FILE.read_text(encoding="utf-8")


# --- Provider adapters: each takes the prompt, returns the report as text. ---
# All four use a single server-side/agentic call; the model runs its own
# search loop internally, so there's no manual tool-call handling here.

def run_anthropic(prompt: str, model: str | None) -> str:
    import anthropic
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    resp = client.beta.messages.create(
        model=model or "claude-opus-5",
        max_tokens=MAX_OUTPUT_TOKENS,
        messages=[{"role": "user", "content": prompt}],
        # The _20260209 variant adds dynamic filtering, which matters for a job
        # whose whole value is the quality of what the search turns up.
        tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 15}],
        # Safety classifiers can decline a request. "default" re-runs a declined
        # request server-side on Anthropic's recommended substitute, routed by
        # refusal category, so an unattended cron run doesn't just return empty.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if resp.stop_reason == "refusal":
        detail = getattr(resp.stop_details, "explanation", None) or "no explanation given"
        raise RuntimeError(f"Model declined the request: {detail}")
    return "".join(
        block.text for block in resp.content if getattr(block, "type", None) == "text"
    )


def run_openai(prompt: str, model: str | None) -> str:
    from openai import OpenAI
    client = OpenAI()  # reads OPENAI_API_KEY
    resp = client.responses.create(
        model=model or "gpt-4.1",  # override via MODEL for your current model
        tools=[{"type": "web_search"}],
        input=prompt,
    )
    return resp.output_text


def run_gemini(prompt: str, model: str | None) -> str:
    from google import genai
    from google.genai import types
    client = genai.Client()  # reads GEMINI_API_KEY
    resp = client.models.generate_content(
        model=model or "gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )
    return resp.text


def run_perplexity(prompt: str, model: str | None) -> str:
    # Perplexity's sonar models search the web natively; OpenAI-compatible API.
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ["PERPLEXITY_API_KEY"],
        base_url="https://api.perplexity.ai",
    )
    resp = client.chat.completions.create(
        model=model or "sonar-pro",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content


ADAPTERS = {
    "anthropic": run_anthropic,
    "openai": run_openai,
    "gemini": run_gemini,
    "perplexity": run_perplexity,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Daily interview reading-list curator")
    parser.add_argument("--provider", default=os.environ.get("PROVIDER", "anthropic"))
    parser.add_argument("--model", default=os.environ.get("MODEL"))
    args = parser.parse_args()

    provider = args.provider.lower()
    if provider not in ADAPTERS:
        sys.exit(f"Unknown provider '{provider}'. Choose from: {', '.join(ADAPTERS)}")

    prompt = load_prompt()
    print(f"Running curator: provider={provider} model={args.model or 'default'}")

    try:
        report = ADAPTERS[provider](prompt, args.model)
    except Exception as exc:  # noqa: BLE001 - surface any provider error clearly
        sys.exit(f"Agent run failed: {exc}")

    if not report or not report.strip():
        sys.exit("Agent returned an empty report.")

    today = datetime.date.today().isoformat()
    OUTPUT_DIR.mkdir(exist_ok=True)
    out_path = OUTPUT_DIR / f"{today}.md"
    header = f"# Daily Brief — {today}\n\n_Provider: {provider}_\n\n---\n\n"
    out_path.write_text(header + report, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())