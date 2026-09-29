# ⚖️ ClearClause — Legal AI Assistant

**Understand legal documents in simpler language.**

ClearClause is an educational document-analysis prototype built with FastAPI,
Google Gemini and PyMuPDF. Upload a selectable-text PDF to get a plain-English
summary, potentially complex clauses to review, and answers grounded in its text.

**Focus:** Generative AI · NLP · Legal Technology  
**Author:** Kulsum Attarwala  
**Status:** Local prototype; a Gemini API key and model access are required for AI results.

## Why this project?

Dense agreements make it difficult to locate obligations, costs, renewal conditions
and termination terms. ClearClause presents these details in a readable interface
and prompts users to verify the underlying clauses with a qualified professional.
It does not replace professional legal advice or determine legal validity.

## Implemented features

- PDF upload with size, page-count and text-length limits.
- Plain-English document summaries and optional document-grounded Q&A.
- Potentially complex clauses, source quotes, page references and questions to ask.
- Exact normalized-text matching for clause quotes; unmatched quotes are flagged.
- All extracted text within supported limits is sent; later pages are not silently dropped.
- Responsive browser interface, loading/error states and downloadable text report.
- Consent before transmitting extracted text to Gemini.
- No application database or intentional upload persistence.
- FastAPI interactive documentation, automated API tests, Dockerfile and GitHub CI.

## Technology

| Layer | Technology |
| --- | --- |
| Interface | HTML, CSS, vanilla JavaScript |
| API | Python 3.11+ / FastAPI / Uvicorn |
| PDF extraction | PyMuPDF |
| AI | Google Gemini via `google-genai` |
| Output validation | Pydantic schema |
| Tests | pytest / FastAPI TestClient |

## Run locally — Windows PowerShell

Install Python 3.11 or newer. Open a terminal in this folder.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Edit `.env` and replace `your_api_key_here` with your Gemini API key from
[Google AI Studio](https://aistudio.google.com/apikey). Keep this file private.
The model is configurable; choose a text-generation model available to your account.
The example uses `gemini-2.5-flash`.

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open **http://127.0.0.1:8000**. API docs: **http://127.0.0.1:8000/docs**.
Using the virtual environment's Python directly avoids PowerShell activation-policy issues.

## Run locally — macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY.
python -m uvicorn main:app --reload
```

## Try the included example

Upload `examples/sample-agreement.pdf` and ask:

- What happens if I terminate this agreement early?
- Does this agreement renew automatically?
- What governing law is specified?

The third question deliberately tests abstention: the fictional agreement does not
specify a governing law. The sample is invented demo data, not a reusable contract.
To regenerate it, run `python scripts/create_sample.py`.

## API

`GET /health` returns server status and whether an API-key value is configured.
It does not validate the key with Google.

`POST /process` accepts multipart fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `file` | Yes | Selectable-text PDF |
| `question` | No | Question, up to 2,000 characters |
| `consent` | Yes | `true` to authorize transmission to Gemini |

```bash
curl -X POST http://127.0.0.1:8000/process \
  -F "file=@examples/sample-agreement.pdf" \
  -F "question=What are the termination terms?" \
  -F "consent=true"
```

The response contains `summary`, `risky_clauses`, `question_answer`,
`pages_total`, `pages_with_text`, `characters_processed`, and `warnings`.
Each clause includes `title`, `page`, `quote`, `explanation`, `question_to_ask`,
and `quote_verified`. Matching a quote does not verify the AI's interpretation.
The earlier prototype's string `risky_clauses` is now a structured array;
its misleading `chunks_used` counter is replaced with explicit page/text coverage.

## Architecture

The browser sends a PDF and optional question to FastAPI. PyMuPDF extracts text
with page labels. The API sends the bounded full context to Gemini once, validates
its JSON output, checks clause quotations against their cited pages, and returns
results for the browser to display. Re-running a question sends the document again;
there is no stored chat history, retrieval index or database.

## Repository contents

- `main.py`: API, extraction, prompt, Gemini integration and quote checks.
- `static/`: interface HTML, CSS and JavaScript.
- `tests/test_api.py`: validation and mocked-AI integration tests.
- `examples/`: fictional agreement as text and PDF.
- `scripts/create_sample.py`: reproducible example PDF generation.
- `docs/GITHUB_SETUP.md`: repository creation, metadata and push instructions.
- `docs/PROJECT_DETAILS.md`: problem, workflow, limitations, evaluation and demo plan.
- `.github/workflows/tests.yml`: automated tests on push / pull request.
- `.env.example`, `.gitignore`, dependency files, Dockerfile and contribution guidance.

## Tests

```bash
python -m pytest -q
```

Tests do not require an API key. They mock model output and test document validation,
full-page context, quote matching, missing-key handling and extraction warnings.
They do not measure legal accuracy or prove resistance to prompt injection.
See `docs/VALIDATION.md` for the checks performed on this delivery.

## Docker

```bash
docker build -t clearclause .
docker run --rm -p 127.0.0.1:8000:8000 --env-file .env clearclause
```

This binds the example to your local machine. GitHub stores the source;
GitHub Pages cannot run this Python backend. A public deployment needs authentication,
rate limits, HTTPS, request limits at the proxy, abuse protection and deployment review.

## Limits and data handling

- Limits: 10 MB, 80 pages, 100,000 extracted characters. Oversize inputs are rejected.
- Scanned PDFs need OCR first. Images, signatures and visual layouts are not interpreted.
- Empty-text pages are flagged; partially scanned pages may still be incomplete.
- Extracted text and the question leave the app and go to Google Gemini.
  Provider processing/retention depends on your account and current service terms.
- The framework may spool uploads to temporary disk; files are closed after reading.
  Do not describe the system as guaranteed memory-only or confidential.
- The AI can omit clauses or fabricate interpretations. Inline summary/Q&A citations
  are model-generated and are not independently validated.
- Prompt rules reduce but cannot eliminate document-based prompt injection.
- There is no OCR, multilingual guarantee, model training, vector RAG, legal database,
  production authentication, or accuracy benchmark in this release.

## Competition attribution

The exact Google event and participation year have not been confirmed for this
project. Add an event name, submission link or achievement only after checking your
registration/certificate. This repository does not claim Google affiliation,
sponsorship, selection, or an award.

## Roadmap

OCR with page-level coverage checks; retrieval for long documents; verified citation
spans for all outputs; expert-reviewed evaluation; multilingual output; document
comparison; authenticated deployment with retention controls.

## References

- [Google Gen AI Python SDK](https://github.com/googleapis/python-genai)
- [Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [FastAPI](https://fastapi.tiangolo.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)

## License

No open-source license has been selected for the project code. Choose one before
inviting reuse. Dependencies retain their own licenses; review these before distribution.
