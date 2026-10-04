"""Streamlit UI — main entry point."""
from __future__ import annotations

import time

import streamlit as st

import config
from agent import Agent
from knowledge_base import KnowledgeBase
from report import build_markdown, export_docx


st.set_page_config(
    page_title="Parenting Capacity Assessor",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 1.5rem; }
        .stAlert { border-left: 3px solid #4a6fa5; }
        section[data-testid="stSidebar"] { background: #f7f8fa; }
        h1 { color: #1a2b4a; }
        .report-section { background: #fafbfc; padding: 1rem; border-radius: 6px;
                          border-left: 3px solid #4a6fa5; margin: 0.5rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "agent" not in st.session_state:
    st.session_state.agent = Agent(KnowledgeBase())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "case_notes" not in st.session_state:
    st.session_state.case_notes = ""
if "report_sections" not in st.session_state:
    st.session_state.report_sections = []
if "case_title" not in st.session_state:
    st.session_state.case_title = ""

with st.sidebar:
    st.header("⚖️ Parenting Capacity Assessor")
    st.caption("Dr. Elena Vasquez — Forensic Psychologist Agent")

    st.markdown("---")
    st.subheader("LLM Backend")
    status = st.session_state.agent.check_connection()
    if status["ok"]:
        st.success(f"✓ Connected — {config.OLLAMA_MODEL}")
    else:
        st.error("✗ Not connected")
        st.caption(f"{status.get('error', '')[:200]}")
        st.info(
            "Start Ollama locally:\n\n"
            "```\n"
            "ollama serve\n"
            "ollama pull llama3.1:8b\n"
            "```"
        )

    st.markdown("---")
    st.subheader("Reference Files")
    st.caption("Upload legislation, precedents, case files, and clinical notes.")

    uploaded = st.file_uploader(
        "Upload files",
        type=["pdf", "docx", "txt", "md"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )
    if uploaded:
        for f in uploaded:
            dest = config.UPLOADS_DIR / f.name
            if not dest.exists():
                with st.spinner(f"Processing {f.name}…"):
                    dest.write_bytes(f.getvalue())
                    chunks = st.session_state.agent.add_file(dest)
                st.success(f"✓ {f.name} — {chunks} chunks indexed")

    sources = st.session_state.agent.list_sources()
    if sources:
        st.markdown(f"**Indexed:** {len(sources)} file(s)")
        for s in sources:
            st.text(f"  • {s}")
        if st.button("Clear knowledge base", type="secondary"):
            st.session_state.agent.clear_knowledge()
            st.rerun()
    else:
        st.caption("No files indexed yet.")

    st.markdown("---")
    st.subheader("Settings")
    st.caption(f"Model: `{config.OLLAMA_MODEL}`")
    st.caption(f"Embedding: `{config.EMBEDDING_MODEL}`")
    st.caption(f"Chunks: {config.CHUNK_SIZE} chars / {config.CHUNK_OVERLAP} overlap")


tab_intake, tab_report, tab_preview = st.tabs([
    "1 · Case Intake",
    "2 · Generate Report",
    "3 · Report Preview & Export",
])

with tab_intake:
    st.markdown("### Case intake interview")
    st.caption("Chat with Dr. Vasquez to gather case information.")

    st.session_state.case_title = st.text_input(
        "Case identifier (optional)",
        value=st.session_state.case_title,
        placeholder="e.g., Re: Harper children — PCO revocation application",
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Describe the case, or answer Dr. Vasquez's questions…"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Dr. Vasquez is thinking…"):
                reply = st.session_state.agent.chat(st.session_state.chat_history[:-1], prompt)
            st.markdown(reply)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.session_state.case_notes += f"\n\n**User:** {prompt}\n**Dr. Vasquez:** {reply}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Suggest missing information"):
            if not st.session_state.case_notes:
                st.warning("No case information gathered yet.")
            else:
                with st.spinner("Analysing gaps…"):
                    suggestions = st.session_state.agent.suggest_followups(st.session_state.case_notes)
                st.markdown("**Information still needed:**")
                st.markdown(suggestions)
    with col2:
        if st.button("🗑️ Clear intake"):
            st.session_state.chat_history = []
            st.session_state.case_notes = ""
            st.rerun()

with tab_report:
    st.markdown("### Generate the 11-section court-ready report")
    st.caption("Drafts each section sequentially using your intake notes and retrieved context.")

    if not st.session_state.case_notes:
        st.warning("⚠️ No case information gathered yet. Complete the Case Intake tab first.")
    else:
        st.info(
            f"**{len(st.session_state.chat_history) // 2} intake exchanges** recorded. "
            f"**{len(st.session_state.agent.list_sources())} reference files** indexed."
        )

        if st.button("🚀 Generate full report", type="primary", use_container_width=True):
            progress = st.progress(0)
            sections = []
            total = len(config.REPORT_SECTIONS)

            for i, section in enumerate(config.REPORT_SECTIONS):
                progress.progress(
                    (i) / total,
                    text=f"Drafting section {section['id']}: {section['title']}…",
                )
                with st.spinner(f"Section {section['id']}: {section['title']}"):
                    body = st.session_state.agent.draft_section(section, st.session_state.case_notes)
                sections.append({"title": section["title"], "body": body})
                st.markdown(f"**✓ Section {section['id']} drafted**")

            progress.progress(1.0, text="Report complete.")
            st.session_state.report_sections = sections
            st.success("✅ All 11 sections drafted. Switch to the Preview tab to review and export.")
            st.rerun()

with tab_preview:
    st.markdown("### Report preview and export")

    if not st.session_state.report_sections:
        st.info("No report generated yet. Complete intake and generate first.")
    else:
        md = build_markdown(st.session_state.report_sections, case_title=st.session_state.case_title)

        for s in st.session_state.report_sections:
            with st.expander(s["title"], expanded=False):
                st.markdown(s["body"])

        st.markdown("---")
        st.subheader("Download")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            ts = time.strftime("%Y%m%d-%H%M")
            safe_title = (st.session_state.case_title or "report").replace(" ", "_")[:40]
            md_name = f"pca_{safe_title}_{ts}.md"
            st.download_button(
                "📄 Download Markdown",
                data=md,
                file_name=md_name,
                mime="text/markdown",
            )
        with col_b:
            docx_name = f"pca_{safe_title}_{ts}.docx"
            docx_path = export_docx(
                st.session_state.report_sections,
                case_title=st.session_state.case_title,
                filename=docx_name,
            )
            with open(docx_path, "rb") as f:
                st.download_button(
                    "📋 Download .docx",
                    data=f.read(),
                    file_name=docx_name,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
        with col_c:
            if st.button("🔍 Run quality check"):
                with st.spinner("Running quality check…"):
                    qc = st.session_state.agent.quality_check(md)
                st.markdown("**Quality check results:**")
                st.markdown(qc)

        st.markdown("---")
        st.subheader("Raw markdown")
        st.code(md, language="markdown")
