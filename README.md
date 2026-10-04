# Parenting Capacity Assessor Agent

A local, privacy-first AI agent for generating court-ready parenting capacity assessment reports for child protection proceedings.

## Features

- Local intake chat with a forensic psychologist persona
- RAG-backed knowledge base from uploaded PDFs, DOCX, TXT, and MD files
- Eleven-section parenting capacity report drafting workflow
- Markdown and DOCX export
- Quality check and follow-up gap analysis
- Runs fully on local hardware with Ollama

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Make sure Ollama is running:

```bash
ollama serve
ollama pull llama3.1:8b
```

## Project structure

- `app.py` — Streamlit user interface
- `agent.py` — LLM orchestration and report generation
- `knowledge_base.py` — local vector-search knowledge base
- `report.py` — Markdown and DOCX generation
- `config.py` — app configuration and report section definitions
- `prompts.py` — interview and drafting prompts
- `data/` — generated reports and local vector data

## Notes

This project is intended for local, privacy-sensitive use. It does not send case material to external APIs when configured with Ollama.
