# WELDING_CHUNK_VALIDATION_RULES.md

Version: v0.2  
Scope: RAG technical chunks for spot welding and dynamic resistance (RD)  
Status: official base rules before PDF extraction

---

## 1. Purpose

This document defines the validation contract for technical chunks used by the OpenClaw RAG Welding System.

The goal is to prevent generic, unsafe or overconfident answers when interpreting spot welding data, especially dynamic resistance (RD).

No PDF extraction should start before these rules are respected.

---

## 2. Base chunk schema

Every technical chunk must keep this base schema:

```json
{
  "chunk_id": "",
  "topic": "",
  "subtopic": "",
  "title": "",
  "content": "",
  "keywords": [],
  "query_patterns": [],
  "source": "",
  "page": null,
  "layer": "",
  "validation": "A | B | C | D",
  "status": "",
  "applicability": "",
  "risk_note": ""
}
