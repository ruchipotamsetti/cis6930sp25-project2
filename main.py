import argparse
import glob
import spacy
import fitz
import os

def extract_pdf_text(file_path):

    doc = fitz.open(file_path)
    text_by_page = [page.get_text() for page in doc]
    return doc, text_by_page

def get_named_entities(text, names, redact_all):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = []
    if redact_all:
        entities = [
            (ent.text, ent.start_char, ent.end_char, ent.label_)
            for ent in doc.ents if ent.label_ == "PERSON"
        ]
    else:
        for ent in doc.ents:
            # print(ent.text)
            if ent.text in names:
                entities.append((ent.text, ent.start_char, ent.end_char, ent.label_))

    return entities

def redact_entities_in_pdf(doc, entities_by_page):
    for page_num, page in enumerate(doc):
        for ent_text, start, end, label in entities_by_page[page_num]:
            text_instances = page.search_for(ent_text)
            for inst in text_instances:
                page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()

def redact_pdf(pdf_path, output_path, names, redact_all):
    doc, pages_text = extract_pdf_text(pdf_path)
    
    entities_by_page = []
    for text in pages_text:
        ents = get_named_entities(text, names, redact_all)
        entities_by_page.append(ents)
    
    redact_entities_in_pdf(doc, entities_by_page)
    input_filename = os.path.basename(pdf_path)
    output_file_path = os.path.join(output_path, input_filename)
    doc.save(output_file_path)
    doc.close()


if __name__ == "__main__":
    print("Hello World!")

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", help="input files globs", required=True)
    parser.add_argument("--output", help="output directory for pdf files", required=True)
    parser.add_argument("--names", action="append", help="Takes one or more case sensitive tokens as input", type=str)
    parser.add_argument("--entities", action="store_true", help="Get all entities")
    parser.add_argument("--coref", action="store_true", help="Redact all coreferences")
    parser.add_argument("--stats", help="Specify the location of the stats file")

    args = parser.parse_args()
    print("Arguments: ", args)

    input_files = []
    for pattern in args.input:
        matched_files = glob.glob(pattern)
        print("matched_files: ",matched_files)
        input_files.extend(matched_files)

    if not input_files:
        print("No files matched the given --input patterns.")
        exit(1)

    os.makedirs(args.output, exist_ok=True)
    

    for file_path in input_files:
        try:
            redact_pdf(file_path, args.output, args.names, args.entities)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
