# Kids Assistant — A Hands-On AI Agent Learning Project

A personal assistant for my 4th-grade son (middle school exam prep), built as a **learning project** to understand how AI agents work from the ground up.

The goal is to be able to look at a product requirement and judge *whether it needs an agent at all* — and if so, how much to delegate to it. Getting there means building the whole stack by hand first: agent loop, tool execution, guardrails, evaluation, observability. I intentionally avoid agent frameworks (LangChain, Claude Agent SDK, etc.) until late in the project, at which point I rebuild the same system with one and compare what it abstracts away.

I use Claude Code as a teacher and code reviewer, not as a code writer. The `docs/learnings/` directory contains my Q&A notes from each milestone, written in my own words.

---

## Tech Stack

- Python
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages) + Tool Use (L1 — raw API, no frameworks)
- `python-dotenv` for API key management
- FastAPI + plain HTML/JS (planned for M4)

---

## Milestones

| # | Milestone | Focus | Status |
|---|-----------|-------|--------|
| M0 | Raw API call, no tools | LLM fundamentals | ✅ |
| M1 | Conversation history | Statelessness, context | ✅ |
| M2 | Tool Use & agent loop | Agent fundamentals | ✅ |
| M3 | Guardrails (input/output) | Safety & control | ✅ |
| M4 | Application boundary (Web UI) | Separation of concerns | 🔜 |
| M5 | Multiple tools | Tool engineering | |
| M6 | Tool execution gate | Permissions, human-in-the-loop | |
| M7 | Context engineering & memory | Context management | |
| M8 | Agent evaluation | Trajectory eval, datasets | |
| M9 | Observability | Tracing, cost, latency | |
| M10 | Production failure modes | Resilience | |
| M11 | Framework comparison | What frameworks abstract away | |
| M12 | Workflow vs Agent | Architecture judgment | |

The later milestones are the point. Tool calling is where most agent tutorials stop — evaluation, observability, and failure handling are where the actual engineering lives.

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
