import os
import tempfile
import main

def test_stats_file_output():
    with tempfile.TemporaryDirectory() as tmpdir:
        input_pdf = "data/ufo-sightings.pdf"
        output_dir = os.path.join(tmpdir, "out")
        stats_file = os.path.join(tmpdir, "stats.txt")

        os.makedirs(output_dir, exist_ok=True)

        with open(stats_file, "w", encoding="utf-8") as stats_handle:
            main.redact_pdf(
                input_pdf,
                output_dir,
                names=["Bonilla"],
                redact_all=False,
                stats_file_handle=stats_handle,
                coref=False,
            )

        with open(stats_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) > 0
            assert lines[0].count("\t") == 4  # tab-separated
