
# AI Prompt Log — Week 6 Production RAG Pipeline

## 1. AI Assistance

I used ChatGPT to help build my Production RAG Pipeline
using Python, ChromaDB, Sentence Transformers, OpenAI,
Tavily, and Streamlit.

My goal was to create a two-stage retrieval system that
searches internal documents, reranks the results, and
uses web search when internal confidence is low.

## 2. Initial AI Request

I asked ChatGPT to help me build the Week 6 assignment
step by step, explain the code, and create the required
RAG pipeline components.

The AI helped generate the Python files for query
rewriting, document retrieval, reranking, web fallback,
answer generation, and the Streamlit interface.

## 3. Issue 1 — Streamlit Import Error

Problem:

The initial command failed with:

ModuleNotFoundError: No module named 'src'

Original command:

uv run streamlit run src/app.py

Correction:

uv run python -m streamlit run src/app.py

Result:

The application opened successfully in my browser.

## 4. Issue 2 — Confidence Score Calibration

The AI-generated reranker uses sigmoid normalization
to transform raw cross-encoder scores into values
between 0 and 1.

The initial threshold was set to 0.55.

A normalized score does not automatically represent
the probability that an answer is correct.

Status:

I verified that internal deployment questions received
high scores and an unrelated SpaceX question triggered
web fallback.

Further calibration across more sample questions
is still needed.

## 5. Issue 3 — Prompt Injection Risk

External web search results may contain instructions
that attempt to influence the AI's answer.

The generator was designed to separate retrieved text
using <retrieved_content> boundaries and instruct the
AI not to follow commands found in source material.

Status:

I created an initial test using a simulated malicious
web snippet. However, the test uses a mocked AI response,
so it does not prove that a real model resists injection.

Additional security testing is needed.

## 6. Testing Results

I ran the automated test suite using:

uv run python -m pytest -v

Results:

8 tests passed.

I also tested the Streamlit application manually:

- Internal deployment question: INTERNAL_RAG
- Unrelated SpaceX question: WEB_FALLBACK
- Tavily successfully retrieved external search results
- OpenAI generated answers with citations

## 7. Reflection

This project helped me understand the difference between
retrieval and reranking, how confidence thresholds affect
routing, and why AI-generated code needs testing.

I learned how to troubleshoot Python import errors,
use pytest, and connect different components into
one Streamlit application.
