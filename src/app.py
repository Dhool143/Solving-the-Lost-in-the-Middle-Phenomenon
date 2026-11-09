
import streamlit as st

from src.rewriter import rewrite_query
from src.retriever import DocumentRetriever
from src.reranker import DocumentReranker
from src.web_fallback import search_web
from src.generator import generate_answer


st.set_page_config(
    page_title="Production RAG Pipeline",
    page_icon="🔎",
    layout="wide",
)

st.title("Production RAG Pipeline")
st.write("Two-Stage Retrieval with Adaptive Web Fallback")


@st.cache_resource
def load_models():
    retriever = DocumentRetriever()
    reranker = DocumentReranker()
    retriever.index_documents()
    return retriever, reranker


retriever, reranker = load_models()

st.sidebar.header("Pipeline Settings")
threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.55,
    step=0.01,
)

reranker.threshold = threshold

query = st.text_input(
    "Ask a technical question:",
    placeholder="What should I do if deployment fails?",
)

history = st.text_area(
    "Previous conversation (optional)",
    placeholder="We were discussing Kubernetes Worker Nodes.",
)

if st.button("Search", type="primary"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running RAG pipeline..."):
            transformed_query = rewrite_query(query, history)

            candidates = retriever.retrieve(
                transformed_query, k=20
            )

            ranked, confidence, status = reranker.rerank(
                transformed_query, candidates, top_k=5
            )

            if status == "HIGH_CONFIDENCE":
                route = "INTERNAL_RAG"
                selected_chunks = ranked
            else:
                route = "WEB_FALLBACK"
                selected_chunks = search_web(
                    transformed_query, max_results=3
                )

            response = generate_answer(
                query=query,
                chunks=selected_chunks,
                route_taken=route,
                confidence_score=confidence,
                transformed_query=transformed_query,
            )

        st.subheader("Pipeline Results")

        st.write("**Original Question:**", query)
        st.write("**Transformed Query:**", transformed_query)

        if route == "INTERNAL_RAG":
            st.success("INTERNAL_RAG — High Confidence")
        else:
            st.warning("WEB_FALLBACK — Low Confidence")

        st.metric(
            "Confidence Score",
            f"{confidence:.3f}",
        )

        st.progress(min(max(confidence, 0.0), 1.0))
        st.caption(f"Confidence threshold: {threshold:.2f}")

        st.subheader("Stage 1 — Bi-Encoder Retrieval")

        with st.expander("View Retrieved Candidates"):
            st.dataframe([
                {
                    "Rank": i + 1,
                    "Document": c.get("filename", ""),
                    "Distance": c.get("distance", 0),
                    "Chunk ID": c["chunk_id"],
                }
                for i, c in enumerate(candidates)
            ])

        st.subheader("Stage 2 — Cross-Encoder Re-Ranking")

        with st.expander("View Re-Ranked Candidates"):
            st.dataframe([
                {
                    "Rank": i + 1,
                    "Document": c.get("filename", ""),
                    "Score": c["confidence"],
                    "Chunk ID": c["chunk_id"],
                }
                for i, c in enumerate(ranked)
            ])

        st.subheader("AI-Generated Answer")
        st.markdown(response.answer)

        st.subheader("Citations")
        for i, citation in enumerate(response.citations, start=1):
            if citation.startswith(("https://", "http://")):
                st.markdown(f"[{i}] [Source]({citation})")
            else:
                st.write(f"[{i}] {citation}")
