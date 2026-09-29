# ClearClause project details

## Abstract

ClearClause is an AI-powered prototype designed to make complex legal documents
more understandable. It extracts text from uploaded PDFs, uses Google Gemini to
produce plain-language explanations, identifies clauses that deserve closer review,
and answers questions using the document as context. Page labels and quote-matching
checks help users return to the source. It supports understanding rather than legal
judgment and requires human verification of every consequential interpretation.

## Problem and users

Students, freelancers, tenants and small business owners may struggle to understand
dense agreements. Important renewal, payment and termination conditions can be hard
to locate. The prototype brings those details into a readable review workflow.

## Objectives

1. Reduce effort required to understand document language.
2. Surface obligations and clauses for further review.
3. Answer document-specific questions without inventing missing facts.
4. Make source verification easier through page references and quotations.

## Workflow

Select PDF → confirm sharing consent → extract page text → enforce limits → ask
Gemini for structured output → validate fields and match quotes → display results
and warnings → download report or ask another question.

## What changed from the uploaded main.py

- Added a complete browser UI and setup/configuration files.
- Removed silent first-five-chunks truncation.
- Replaced repeated prompts/API calls with one structured-output request.
- Added asynchronous Gemini calls and offloaded PDF extraction from the event loop.
- Moved key checks to analysis time, so health/UI work without a key.
- Added size, page, character, consent and question checks.
- Closed PDF documents and upload handles and hid raw provider exceptions.
- Added page coverage, quote matching, tests, sample input and GitHub instructions.

## Evaluation plan — proposed, not completed

Create 20–30 fictional or permission-cleared agreements with human-annotated payment,
renewal, confidentiality and termination clauses. Ask reviewers to mark correct
summaries, omissions, unsupported claims and answerable/unanswerable questions.
Measure clause precision/recall, quotation match rate, answer faithfulness,
abstention on missing facts, latency and API cost. Include long documents with key
clauses on the last page, mixed scans, contradictory clauses and embedded instructions.
Obtain qualified review before describing output quality as legally reliable.

## Two-minute demo outline

- 0:00–0:20: Explain the problem: important terms are buried in dense documents.
- 0:20–0:40: Upload the fictional agreement and explain the sharing consent.
- 0:40–1:10: Show the summary and renewal/termination clauses, subject to actual model output.
- 1:10–1:35: Ask about early termination; compare the answer with page 2.
- 1:35–1:50: Ask about governing law and show the expected not-specified response.
- 1:50–2:00: Download the report and explain that human verification remains essential.

## Portfolio wording

Built ClearClause, a legal document understanding prototype using FastAPI, PyMuPDF
and Google Gemini, with PDF summaries, clause review, document-grounded Q&A and
source-quote matching.

Do not add an event name, placement or measured accuracy until independently confirmed.
