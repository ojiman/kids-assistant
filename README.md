# Kids Assistant — A Hands-On AI Agent Learning Project

A personal assistant for my 4th-grade son (middle school exam prep), built as a **learning project** to deeply understand how AI agents work from the ground up.

The primary goal is **understanding**, not shipping. I intentionally avoid agent frameworks (LangChain, Claude Agent SDK, etc.) and build everything by hand — agent loop, tool execution, guardrails — using the raw Anthropic Messages API.

I use Claude Code as a teacher and code reviewer, not as a code writer. The `docs/learnings/` directory contains my Q&A notes from each milestone, written in my own words.

---

## Tech Stack

- Python
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) + Tool Use (L1 — raw API, no frameworks)
- `python-dotenv` for API key management
- FastAPI + plain HTML/JS (planned for M4)

---

## Milestones

| # | Milestone | Status |
|---|-----------|--------|
| M0 | Raw API call, no tools | ✅ Done |
| M1 | Conversation history | ✅ Done |
| M2 | Tool Use & agent loop | ✅ Done |
| M3 | Guardrails (input/output) | ✅ Done |
| M4 | Local Web UI (FastAPI) | 🔜 Next |

---

## Setup

```bash
# Install dependencies
pip install anthropic python-dotenv

# Set your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run
python main.py
```

---

## Project Structure

```
.
├── main.py               # Agent harness (agent loop, tools, guardrails)
├── docs/
│   └── learnings/
│       ├── m0.md         # Raw API call — learnings
│       ├── m1.md         # Conversation history — learnings
│       ├── m2.md         # Tool Use & agent loop — learnings
│       └── m3.md         # Guardrails — learnings
└── logs/                 # Conversation logs (gitignored)
```

---

## Safety

- API key stored in `.env`, never hardcoded
- Conversation logs stored in `logs/` (gitignored, never committed)
- No file system or shell execution tools
- Multi-layer guardrails: system prompt → LLM input review → LLM output review
