import argparse

def extract_pdf_text():
    print("Hello")


if __name__ == "__main__":
    print("Hello World!")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs="+", help="input files globs")
    parser.add_argument("--output", help="output directory for pdf files")
    parser.add_argument("--names", nargs="+", help="Takes one or more case sensitive tokens as input")
    parser.add_argument("--entities", help="Get all entities")
    parser.add_argument("--coref", help="Redact all coreferences")
    parser.add_argument("--stats", help="Specify the location of the stats file")

    args = parser.parse_args()
    print("Arguments: ", args)

    extract_pdf_text(args.input)
    