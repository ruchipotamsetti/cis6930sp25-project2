import argparse
import glob
import spacy
import fitz
import os
import sys
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)


def extract_pdf_text(file_path):
    doc = fitz.open(file_path)
    text_by_page = [page.get_text() for page in doc]
    return doc, text_by_page

def get_named_entities(text, names, redact_all, coref):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []

    if redact_all:
        entities += [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents if ent.label_ == "PERSON"]
    
    else:
        for ent in doc.ents:
            if ent.text in names:
                entities.append((ent.text, ent.start_char, ent.end_char, ent.label_))

    if coref:
        pronouns = {"he", "she", "him", "her", "his", "hers", "they", "them", "their", "theirs"}
        for sent in doc.sents:
            if any(ent.label_ == "PERSON" for ent in sent.ents):
                for token in sent:
                    if token.text.lower() in pronouns:
                        entities.append((token.text, token.idx, token.idx + len(token.text), "COREF"))

    return entities

def redact_entities_in_pdf(doc, entities_by_page, pdf_filename, stats_file_handle):
    stats_entries = []

    for page_num, page in enumerate(doc):
        already_redacted = set()

        for ent_text, start, end, label in entities_by_page[page_num]:
            if label == "COREF":
                matches = []
                for w in page.get_text("words"):
                    x0, y0, x1, y1, word, *_ = w
                    if word == ent_text:
                        matches.append(fitz.Rect(x0, y0, x1, y1))
            else:
                matches = page.search_for(ent_text)

            for inst in matches:
                loc_key = (int(inst.x0), int(inst.y0))
                if loc_key not in already_redacted:
                    already_redacted.add(loc_key)
                    page.add_redact_annot(inst, fill=(0, 0, 0))
                    location = f"{int(inst.x0)}x{int(inst.y0)}"
                    stats_entries.append(f"{pdf_filename}\t{location}\t{ent_text}\t{len(ent_text)}\t{label}")

        page.apply_redactions()

    if stats_file_handle and stats_entries:
        stats_file_handle.write("\n".join(stats_entries) + "\n")
        stats_file_handle.flush()

def redact_pdf(pdf_path, output_path, names, redact_all, stats_file_handle=None, coref=False):
    doc, pages_text = extract_pdf_text(pdf_path)

    entities_by_page = []
    for text in pages_text:
        ents = get_named_entities(text, names, redact_all, coref)
        entities_by_page.append(ents)

    redact_entities_in_pdf(doc, entities_by_page, os.path.basename(pdf_path), stats_file_handle)

    input_filename = os.path.basename(pdf_path)
    output_file_path = os.path.join(output_path, input_filename)
    doc.save(output_file_path)
    doc.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", help="input files globs", required=True)
    parser.add_argument("--output", help="output directory for pdf files", required=True)
    parser.add_argument("--names", action="append", help="Takes one or more case sensitive tokens as input", type=str)
    parser.add_argument("--entities", action="store_true", help="Get all entities")
    parser.add_argument("--coref", action="store_true", help="Redact all coreferences")
    parser.add_argument("--stats", help="Specify the location of the stats file. Defaults to stderr if not provided.")

    args = parser.parse_args()

    input_files = []
    for pattern in args.input:
        matched_files = glob.glob(pattern)
        input_files.extend(matched_files)

    if not input_files:
        print("No files matched the given --input patterns.")
        exit(1)

    os.makedirs(args.output, exist_ok=True)

    stats_file_handle = None
    if args.stats:
        os.makedirs(os.path.dirname(args.stats), exist_ok=True)
        stats_file_handle = open(args.stats, "a", encoding="utf-8")
    else:
        stats_file_handle = sys.stderr

    try:
        for file_path in input_files:
            redact_pdf(file_path, args.output, args.names or [], args.entities, stats_file_handle, args.coref)
    finally:
        if args.stats and stats_file_handle:
            stats_file_handle.close()
