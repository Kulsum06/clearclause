const $ = (id) => document.getElementById(id);
let latest = null;
const add = (parent, tag, text) => {
  const node = document.createElement(tag);
  node.textContent = text;
  parent.appendChild(node);
  return node;
};
$('form').addEventListener('submit', async (event) => {
  event.preventDefault();
  latest = null;
  $('results').hidden = true;
  $('download').hidden = true;
  $('empty').hidden = false;
  $('status').className = '';
  const file = $('file').files[0];
  if (!file || file.size > 10 * 1024 * 1024) {
    $('status').textContent = 'Choose a PDF no larger than 10 MB.';
    $('status').className = 'error';
    return;
  }
  const body = new FormData();
  body.append('file', file);
  body.append('question', $('question').value.trim());
  body.append('consent', String($('consent').checked));
  $('submit').disabled = true;
  $('status').textContent = 'Reading and analyzing your document. This may take a minute…';
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 120000);
  try {
    const response = await fetch('/process', {method: 'POST', body, signal: controller.signal});
    const data = await response.json();
    if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check your upload and try again.');
    latest = data;
    $('empty').hidden = true;
    $('results').hidden = false;
    $('download').hidden = false;
    $('coverage').textContent = `${data.pages_with_text}/${data.pages_total} pages contain extracted text · ${data.characters_processed.toLocaleString()} characters sent`;
    $('summary').textContent = data.summary;
    $('clauses').replaceChildren();
    if (!data.risky_clauses.length) add($('clauses'), 'p', 'No clauses were flagged by the AI. This does not establish that the document is safe.');
    data.risky_clauses.forEach((clause) => {
      const card = add($('clauses'), 'article', '');
      card.className = 'clause';
      add(card, 'h4', clause.title);
      add(card, 'small', `Page ${clause.page} · ${clause.quote_verified ? 'Quote matched to extracted text' : 'Quote needs manual verification'}`);
      add(card, 'blockquote', clause.quote);
      add(card, 'p', clause.explanation);
      add(card, 'p', `Ask: ${clause.question_to_ask}`);
    });
    $('answer-section').hidden = !data.question_answer;
    $('answer').textContent = data.question_answer || '';
    $('warnings').replaceChildren();
    data.warnings.forEach((message) => add($('warnings'), 'p', message));
    $('status').textContent = 'Analysis ready. Review the source document alongside these explanations.';
  } catch (error) {
    $('status').textContent = error.name === 'AbortError' ? 'The request timed out. Try again with a smaller document.' : error.message;
    $('status').className = 'error';
  } finally {
    clearTimeout(timer);
    $('submit').disabled = false;
  }
});
$('download').addEventListener('click', () => {
  if (!latest) return;
  const lines = ['CLEARCLAUSE — DOCUMENT REVIEW', 'Educational assistance, not legal advice.', '', latest.summary, '', 'CLAUSES TO REVIEW'];
  latest.risky_clauses.forEach(c => lines.push('', `${c.title} (page ${c.page})`, `Quote matched: ${c.quote_verified}`, c.quote, c.explanation, `Ask: ${c.question_to_ask}`));
  if (latest.question_answer) lines.push('', 'ANSWER', latest.question_answer);
  lines.push('', 'COVERAGE', `${latest.pages_with_text}/${latest.pages_total} pages contain extracted text.`, '', 'NOTES', ...latest.warnings);
  const url = URL.createObjectURL(new Blob([lines.join('\n')], {type: 'text/plain;charset=utf-8'}));
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = 'clearclause-report.txt';
  anchor.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
