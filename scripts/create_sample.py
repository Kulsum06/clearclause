"""Generate a fictional, selectable-text PDF for the local demo."""
from pathlib import Path
import fitz

root = Path(__file__).resolve().parents[1]
text = (root / 'examples' / 'sample-agreement.txt').read_text()
with fitz.open() as doc:
    for section in text.split('\n---PAGE---\n'):
        page = doc.new_page()
        remaining = page.insert_textbox(fitz.Rect(50, 50, 545, 790), section, fontsize=12)
        if remaining < 0:
            raise RuntimeError('Sample text does not fit on the page.')
    target = root / 'examples' / 'sample-agreement.pdf'
    doc.save(target)
    print(target)
