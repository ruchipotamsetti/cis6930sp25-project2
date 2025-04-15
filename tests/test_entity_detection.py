import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main

def test_named_entity_detection():
    text = "Alice and Bob are attending the conference in Paris."
    names = ["Alice"]
    entities = main.get_named_entities(text, names, redact_all=False, coref=False)
    assert any(ent[0] == "Alice" and ent[3] == "PERSON" for ent in entities)
    assert all(ent[0] != "Bob" for ent in entities)
