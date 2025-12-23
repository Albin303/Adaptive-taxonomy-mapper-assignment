# Adaptive Taxonomy Mapper – Pratilipi Assignment

Albin Biju  
December 23, 2025

Overview
This is a prototype inference engine that maps messy user tags and short story blurbs to precise fiction sub-genres. It strictly follows the three rules:
-Context Wins – blurb overrides conflicting tags
- Honesty – returns `[UNMAPPED]` if no good fit
- Hierarchy – only uses exact sub-genres from the provided taxonomy

The system correctly handles all 10 golden test cases with clear reasoning.

## Why I chose a keyword-based approach (instead of LLM)
- The taxonomy is small (only 12 sub-genres) → keyword matching is simple, fast, and 100% accurate for these cases.
- Full control: no risk of hallucinating non-existent categories.
- Completely explainable – every decision is backed by matched keywords.
- Zero cost, no API dependency, and easy to debug/maintain.
- Perfectly satisfies "Context Wins" and "Honesty" without complex prompt engineering.

For larger taxonomies (e.g., 5,000 categories) or higher ambiguity, I would switch to semantic embeddings (SentenceTransformers + FAISS) or a hybrid system with LLM only on low-confidence cases — as discussed in the design document.

## Files
- `mapper.py` – main prototype code
- `output_log.json` – results with reasoning for all 10 test cases
- `design_answers.txt` – answers to the three scaling/design questions

## How to run
```bash
python mapper.py
