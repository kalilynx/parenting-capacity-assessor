"""Configuration loader. Reads from .env, exposes typed constants."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", str(BASE_DIR / "data")))
KNOWLEDGE_DIR = Path(os.getenv("KNOWLEDGE_DIR", str(DATA_DIR / "knowledge")))
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", str(DATA_DIR / "reports")))
SKILL_DOC_DIR = Path(os.getenv("SKILL_DOC_DIR", str(DATA_DIR / "skill_doc")))
UPLOADS_DIR = Path(os.getenv("UPLOADS_DIR", str(BASE_DIR / "uploads")))

for _d in (DATA_DIR, KNOWLEDGE_DIR, REPORTS_DIR, SKILL_DOC_DIR, UPLOADS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

HF_HOME = Path(os.getenv("HF_HOME", str(BASE_DIR / ".hf_cache")))
HF_HOME.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(HF_HOME))

# ── LLM ──────────────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai" if os.getenv("OPENAI_API_KEY") else "ollama").lower()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
TEMP_REPORT = float(os.getenv("LLM_TEMPERATURE_REPORT", "0.25"))
TEMP_CHAT = float(os.getenv("LLM_TEMPERATURE_CHAT", "0.6"))

# ── RAG ──────────────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1200"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "4"))

# ── Report structure ─────────────────────────────────────────
REPORT_SECTIONS = [
    {
        "id": 1,
        "title": "Referral Information and Source of Referral",
        "description": (
            "Identify who requested the assessment, the legal context "
            "(PCO revocation, reunification, initial protection), the "
            "specific referral questions, and the date/scope of the assessment."
        ),
    },
    {
        "id": 2,
        "title": "Background and Historical Information",
        "description": (
            "Child protection history, prior court orders, reasons for "
            "removal, placement history, and any prior assessments."
        ),
    },
    {
        "id": 3,
        "title": "Assessment Methods and Sources Consulted",
        "description": (
            "List every method used (clinical interviews, observations, "
            "document review, collateral interviews, psychometric testing) "
            "with dates, durations, and participants."
        ),
    },
    {
        "id": 4,
        "title": "Psychosocial and Developmental History",
        "description": (
            "Parent's early life, attachment history, adverse childhood "
            "experiences, educational/vocational history, relationship "
            "patterns, and current life circumstances (housing, employment, "
            "support networks)."
        ),
    },
    {
        "id": 5,
        "title": "Mental Health and Substance Use History",
        "description": (
            "Psychiatric diagnoses, treatment history, current mental "
            "state, medication compliance, substance use pattern, periods "
            "of sobriety, and treatment engagement."
        ),
    },
    {
        "id": 6,
        "title": "Parenting Capacity Across Key Domains",
        "description": (
            "Evaluate the seven domains: (1) safety and protection from "
            "harm, (2) emotional availability and secure attachment, "
            "(3) stability and consistency, (4) insight and understanding, "
            "(5) appropriate supervision and developmental responsiveness, "
            "(6) capacity under stress, (7) engagement with services and "
            "willingness to change. Each domain should cite evidence using "
            "the evidence hierarchy."
        ),
    },
    {
        "id": 7,
        "title": "Parent-Child Interaction Observations",
        "description": (
            "Observation settings, attachment quality, emotional attunement, "
            "boundary setting, play/engagement, communication, stress "
            "management, and safety awareness."
        ),
    },
    {
        "id": 8,
        "title": "Psychometric Testing Results",
        "description": (
            "Standardised test administration, scores, interpretation, "
            "and how results inform parenting capacity. Note limitations "
            "(testing supplements, does not replace, clinical judgment)."
        ),
    },
    {
        "id": 9,
        "title": "Risk and Protective Factor Analysis",
        "description": (
            "Apply the evidence hierarchy. For each risk and protective "
            "factor, state the evidence level (Level 1 objective records "
            "to Level 5 unverified self-report) and source explicitly."
        ),
    },
    {
        "id": 10,
        "title": "Clinical Formulation and Opinions",
        "description": (
            "Integrative synthesis. Answer the referral questions directly. "
            "State opinion on current parenting capacity, change achieved, "
            "and whether reunion is in the child's best interests. "
            "Distinguish clearly between fact, inference, and opinion."
        ),
    },
    {
        "id": 11,
        "title": "Recommendations and Safeguards",
        "description": (
            "Specific, actionable recommendations regarding contact, "
            "services, monitoring, and safeguards. Include conditions "
            "under which recommendations should be reviewed."
        ),
    },
]
