import os
import fitz
import pytest
from main import extract_pdf_text, get_named_entities, redact_pdf 

@pytest.fixture
def sample_pdf(tmp_path):
    pdf_path = tmp_path / "test.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((100, 100), "John Doe met Alice in Paris. He gave her the documents.")
    doc.save(pdf_path)
    doc.close()
    return pdf_path

def test_text_extraction(sample_pdf):
    doc, pages_text = extract_pdf_text(sample_pdf)
    assert len(pages_text) == 1
    assert "John Doe" in pages_text[0]
    assert "Alice" in pages_text[0]

def test_entity_recognition():
    text = "John Doe works at Google in New York."
    entities = get_named_entities(text, ["John Doe"], False, False)
    assert any(ent[0] == "John Doe" for ent in entities)
    
    entities_all = get_named_entities(text, [], True, False)
    assert len(entities_all) == 1  
