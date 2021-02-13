"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import tempfile
from typer.testing import CliRunner
from edgar.cli import *

runner = CliRunner()

dir_path = os.path.dirname(os.path.realpath(__file__))


def count_lines(text):
    matches = re.compile(r"^\".+?\.txt\"", re.MULTILINE).findall(text)
    return len(matches)


def test_script_on_form3_collection(test_form3_collection):
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir)
        assert out_dir.exists()
        result = runner.invoke(
            app,
            [str(test_form3_collection), "--out_dir", str(tmp_dir)],
        )
        assert result.exit_code == 0
        assert "processing files in dir" in result.stdout
        assert "generating output in dir" in result.stdout
        assert result.stdout.count("processing file:") == 100

        assert (Path(tmp_dir) / "document_info.csv").exists()
        assert count_lines((Path(tmp_dir) / "document_info.csv").read_text()) == 100
        assert (Path(tmp_dir) / "footnotes.csv").exists()
        assert count_lines((Path(tmp_dir) / "footnotes.csv").read_text()) == 500
        assert (Path(tmp_dir) / "derivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "derivatives.csv").read_text()) == 128
        assert (Path(tmp_dir) / "nonderivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "nonderivatives.csv").read_text()) == 54
        assert (Path(tmp_dir) / "report_owners.csv").exists()
        assert count_lines((Path(tmp_dir) / "report_owners.csv").read_text()) == 178
        assert (Path(tmp_dir) / "signatures.csv").exists()
        assert count_lines((Path(tmp_dir) / "signatures.csv").read_text()) == 168


def test_script_on_form4_collection(test_form4_collection):
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir)
        assert out_dir.exists()
        result = runner.invoke(
            app,
            [str(test_form4_collection), "--out_dir", str(tmp_dir)],
        )
        assert result.exit_code == 0
        assert "processing files in dir" in result.stdout
        assert "generating output in dir" in result.stdout
        assert result.stdout.count("processing file:") == 100

        assert (Path(tmp_dir) / "document_info.csv").exists()
        assert count_lines((Path(tmp_dir) / "document_info.csv").read_text()) == 100
        assert (Path(tmp_dir) / "footnotes.csv").exists()
        assert count_lines((Path(tmp_dir) / "footnotes.csv").read_text()) == 417
        assert (Path(tmp_dir) / "derivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "derivatives.csv").read_text()) == 81
        assert (Path(tmp_dir) / "nonderivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "nonderivatives.csv").read_text()) == 182
        assert (Path(tmp_dir) / "report_owners.csv").exists()
        assert count_lines((Path(tmp_dir) / "report_owners.csv").read_text()) == 129
        assert (Path(tmp_dir) / "signatures.csv").exists()
        assert count_lines((Path(tmp_dir) / "signatures.csv").read_text()) == 123


def test_script_on_form5_collection(test_form5_collection):
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir)
        assert out_dir.exists()
        result = runner.invoke(
            app,
            [str(test_form5_collection), "--out_dir", str(tmp_dir)],
        )
        assert result.exit_code == 0
        assert "processing files in dir" in result.stdout
        assert "generating output in dir" in result.stdout
        assert result.stdout.count("processing file:") == 100

        assert (Path(tmp_dir) / "document_info.csv").exists()
        assert count_lines((Path(tmp_dir) / "document_info.csv").read_text()) == 100
        assert (Path(tmp_dir) / "footnotes.csv").exists()
        assert count_lines((Path(tmp_dir) / "footnotes.csv").read_text()) == 546
        assert (Path(tmp_dir) / "derivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "derivatives.csv").read_text()) == 138
        assert (Path(tmp_dir) / "nonderivatives.csv").exists()
        assert count_lines((Path(tmp_dir) / "nonderivatives.csv").read_text()) == 286
        assert (Path(tmp_dir) / "report_owners.csv").exists()
        assert count_lines((Path(tmp_dir) / "report_owners.csv").read_text()) == 102
        assert (Path(tmp_dir) / "signatures.csv").exists()
        assert count_lines((Path(tmp_dir) / "signatures.csv").read_text()) == 102
