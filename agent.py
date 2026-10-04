"""Core agent — chat intake + report generation."""
from __future__ import annotations

from typing import List, Dict, Optional

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import config
from prompts import (
    PERSONA_PROMPT,
    INTAKE_PROMPT,
    section_prompt,
    QUALITY_CHECK_PROMPT,
    FOLLOWUP_PROMPT,
)
from knowledge_base import KnowledgeBase


class Agent:
    """Parenting Capacity Assessor agent."""

    def __init__(self, kb: Optional[KnowledgeBase] = None):
        self.kb = kb or KnowledgeBase()
        self.llm_report = ChatOllama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMP_REPORT,
        )
        self.llm_chat = ChatOllama(
            base_url=config.OLLAMA_BASE_URL,
            model=config.OLLAMA_MODEL,
            temperature=config.TEMP_CHAT,
        )

    def check_connection(self) -> Dict[str, object]:
        try:
            resp = self.llm_report.invoke([HumanMessage(content="Reply with the single word OK.")])
            return {"ok": True, "model": config.OLLAMA_MODEL, "sample": resp.content.strip()[:40]}
        except Exception as e:
            return {"ok": False, "error": str(e)[:300]}

    def chat(self, history: List[Dict[str, str]], user_message: str) -> str:
        messages = [SystemMessage(content=INTAKE_PROMPT)]
        for h in history:
            if h["role"] == "user":
                messages.append(HumanMessage(content=h["content"]))
            else:
                messages.append(AIMessage(content=h["content"]))
        messages.append(HumanMessage(content=user_message))
        resp = self.llm_chat.invoke(messages)
        return resp.content

    def draft_section(self, section: dict, case_notes: str) -> str:
        prompt_template = section_prompt(section)
        retrieved = self.kb.retrieve(
            query=section["title"] + " " + section["description"],
            k=config.RETRIEVAL_TOP_K,
        )
        final_prompt = prompt_template.format(
            case_notes=case_notes or "(no case notes yet)",
            retrieved_knowledge=retrieved,
        )
        resp = self.llm_report.invoke([HumanMessage(content=final_prompt)])
        return resp.content.strip()

    def quality_check(self, full_report: str) -> str:
        prompt = QUALITY_CHECK_PROMPT.format(report=full_report)
        resp = self.llm_report.invoke([HumanMessage(content=prompt)])
        return resp.content.strip()

    def suggest_followups(self, case_notes: str) -> str:
        prompt = FOLLOWUP_PROMPT.format(case_notes=case_notes)
        resp = self.llm_chat.invoke([HumanMessage(content=prompt)])
        return resp.content.strip()

    def add_file(self, path) -> int:
        return self.kb.add_file(path)

    def list_sources(self) -> List[str]:
        return self.kb.list_sources()

    def clear_knowledge(self) -> None:
        self.kb.clear()
