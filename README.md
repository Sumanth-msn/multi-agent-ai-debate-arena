# ⚔️ Multi-Agent AI Debate Arena

Two AI agents argue opposite sides of any topic. A third judge AI scores both and declares a winner — all powered by a LangGraph pipeline with real-time web search.

🔗 **[Live Demo](https://sumanth-multi-agent-ai-debate-arena-3.streamlit.app)**

---

## How it works

```
User enters topic
       ↓
  [Search Agent]  ← fetches real web facts via DuckDuckGo
       ↓
  [FOR Agent]     ← argues in favor using search context
       ↓
  [AGAINST Agent] ← argues against using search context
       ↓
  [Judge Agent]   ← scores both sides and declares winner
       ↓
  Result shown in Streamlit UI
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| LangGraph | Agent orchestration & graph state management |
| Groq + Llama 3.3 70B | LLM inference (free tier) |
| LangChain | Agent & tool abstractions |
| DuckDuckGo Search | Free real-time web search |
| Streamlit | Frontend UI |

---

## Project Structure

```
├── app.py              # Streamlit UI
├── src/
│   ├── agents.py       # FOR / AGAINST / Judge agent logic
│   ├── graph.py        # LangGraph pipeline
│   ├── prompts.py      # System prompts for each agent
│   └── tools.py        # DuckDuckGo search tool
└── requirements.txt
```

---

## Run locally

```bash
git clone https://github.com/sumanth-msn/multi-agent-ai-debate-arena.git
cd multi-agent-ai-debate-arena

uv venv --python 3.12
source .venv/bin/activate

uv pip install -r requirements.txt
```

Add your Groq API key (free at [console.groq.com](https://console.groq.com)):
```bash
echo "GROQ_API_KEY=your_key_here" > .env
```

Run:
```bash
streamlit run app.py
```

---

## What I learned building this

- How to structure a multi-node agentic pipeline using LangGraph's `StateGraph`
- The **agent-as-evaluator** pattern (Judge agent scoring other agents)
- Why grounding LLM responses with real search results reduces hallucination
- Managing shared state across independent agent nodes

---

*Built by Sumanth · [GitHub](https://github.com/sumanth-msn)*

## How it works

                        ┌─────────────────────┐
                        │   User enters topic  │
                        └────────┬────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │      Search Node        │
                    │  DuckDuckGo web search  │
                    │  → stores in state      │
                    └────────────┬───────────┘
                                 │ search_results
                    ┌────────────▼───────────┐
                    │       FOR Agent         │
                    │  "Argue IN FAVOR of     │
                    │   the topic"            │
                    │  uses search_results    │
                    └────────────┬───────────┘
                                 │ for_argument
                    ┌────────────▼───────────┐
                    │     AGAINST Agent       │
                    │  "Argue AGAINST         │
                    │   the topic"            │
                    │  uses search_results    │
                    └────────────┬───────────┘
                                 │ against_argument
                    ┌────────────▼───────────┐
                    │      Judge Agent        │
                    │  reads both arguments   │
                    │  scores each out of 10  │
                    │  declares a winner      │
                    └────────────┬───────────┘
                                 │ verdict
                    ┌────────────▼───────────┐
                    │     Streamlit UI        │
                    │  displays full debate   │
                    │  + judge's verdict      │
                    └────────────────────────┘

  All agents share a single DebateState (TypedDict)
  orchestrated by LangGraph's StateGraph