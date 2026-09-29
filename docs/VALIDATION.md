# Delivery validation

Checked on 29 September 2026 with Python 3.12.

- `python -m pytest -q`: 12 passed; one upstream TestClient/httpx deprecation warning.
- `node --check static/app.js`: passed syntax validation.
- `python scripts/create_sample.py`: generated the two-page fictional PDF successfully.
- TestClient verified that the homepage and health endpoint respond.

Tests include invalid/corrupt PDFs, empty text, consent, byte/page/text limits,
missing API key, oversized questions, final-page coverage, matched/unmatched clause
quotes, and mixed scanned/text-page warnings. Gemini calls are mocked in integration tests.

Not verified: live Gemini responses (no user API key supplied), legal accuracy,
browser visual/interaction behavior, Docker image build or public deployment.
No GitHub remote repository was created as part of the downloadable package.
Dependency files use bounded ranges, not an exact transitive lockfile.
