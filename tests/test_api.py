import fitz
import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def pdf_bytes(pages=None):
    with fitz.open() as doc:
        for text in pages or ['Payment is due in 30 days.']:
            page = doc.new_page()
            if text:
                page.insert_text((72, 72), text)
        return doc.tobytes()


def post(data, **fields):
    return client.post('/process', files={'file': ('sample.pdf', data, 'application/pdf')}, data={'consent': 'true', **fields})


def test_health_without_key(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    assert client.get('/health').json() == {'status': 'ok', 'ai_configured': False}
    assert client.get('/').status_code == 200


def test_consent_required():
    assert post(pdf_bytes(), consent='false').status_code == 400


@pytest.mark.parametrize('data,code', [(b'not a pdf', 400), (b'%PDF-broken', 400), (pdf_bytes(['']), 422)])
def test_bad_documents(data, code):
    assert post(data).status_code == code


def test_size_limit(monkeypatch):
    monkeypatch.setattr(main, 'MAX_BYTES', 10)
    assert post(pdf_bytes()).status_code == 413


def test_page_limit(monkeypatch):
    monkeypatch.setattr(main, 'MAX_PAGES', 1)
    assert post(pdf_bytes(['First', 'Last'])).status_code == 413


def test_text_limit(monkeypatch):
    monkeypatch.setattr(main, 'MAX_CHARS', 5)
    assert post(pdf_bytes()).status_code == 413


def test_missing_key(monkeypatch):
    monkeypatch.delenv('GEMINI_API_KEY', raising=False)
    assert post(pdf_bytes()).status_code == 503


def test_entire_document_and_quotes(monkeypatch):
    async def fake(context, question):
        assert '[Page 7]' in context and 'FINAL CLAUSE' in context
        assert question == 'When is payment due?'
        return main.Analysis(summary='Payment is due in 30 days [page 1].', risky_clauses=[
            main.Clause(title='Payment', page=1, quote='Payment is due in 30 days.', explanation='Payment deadline.', question_to_ask='When does the period start?'),
            main.Clause(title='Unsupported', page=99, quote='Invented', explanation='Example', question_to_ask='Verify?'),
        ], question_answer='Within 30 days [page 1].')
    monkeypatch.setattr(main, 'generate_analysis', fake)
    response = post(pdf_bytes(['Payment is due in 30 days.'] + ['Middle'] * 5 + ['FINAL CLAUSE']), question='When is payment due?')
    assert response.status_code == 200
    data = response.json()
    assert data['pages_total'] == 7
    assert data['risky_clauses'][0]['quote_verified'] is True
    assert data['risky_clauses'][1]['quote_verified'] is False
    assert any('could not be matched' in w for w in data['warnings'])


def test_mixed_scans_warn_and_no_question(monkeypatch):
    async def fake(context, question):
        return main.Analysis(summary='Example', risky_clauses=[], question_answer='Unrequested')
    monkeypatch.setattr(main, 'generate_analysis', fake)
    data = post(pdf_bytes(['Text page', ''])).json()
    assert data['pages_with_text'] == 1
    assert data['question_answer'] is None
    assert any('pages [2]' in w for w in data['warnings'])


def test_question_limit():
    assert post(pdf_bytes(), question='x' * 2001).status_code == 400
