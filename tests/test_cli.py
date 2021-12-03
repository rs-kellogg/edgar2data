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


def test_script_on_form3_collection(test_form3_collection, tmpdir):
    """
    Test script on a random sample of Form 3 documents
    :param test_form3_collection:
    :return:
    """
    assert tmpdir.exists()
    result = runner.invoke(
        app,
        [str(test_form3_collection), "--out_dir", str(tmpdir)],
    )
    assert result.exit_code == 0
    assert "processing files in dir" in result.stdout
    assert "generating output in dir" in result.stdout
    assert result.stdout.count("processing file:") == 100

    assert (Path(tmpdir) / "document_info.csv").exists()
    assert count_lines((Path(tmpdir) / "document_info.csv").read_text()) == 100
    assert (Path(tmpdir) / "footnotes.csv").exists()
    assert count_lines((Path(tmpdir) / "footnotes.csv").read_text()) == 500
    assert (Path(tmpdir) / "derivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "derivatives.csv").read_text()) == 128
    assert (Path(tmpdir) / "nonderivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "nonderivatives.csv").read_text()) == 54
    assert (Path(tmpdir) / "report_owners.csv").exists()
    assert count_lines((Path(tmpdir) / "report_owners.csv").read_text()) == 178
    assert (Path(tmpdir) / "signatures.csv").exists()
    assert count_lines((Path(tmpdir) / "signatures.csv").read_text()) == 168


def test_script_on_form4_collection(test_form4_collection, tmpdir):
    """
    Test script on a random sample of Form 4 documents
    :param test_form4_collection:
    :return:
    """
    result = runner.invoke(
        app,
        [str(test_form4_collection), "--out_dir", str(tmpdir)],
    )
    assert result.exit_code == 0
    assert "processing files in dir" in result.stdout
    assert "generating output in dir" in result.stdout
    assert result.stdout.count("processing file:") == 100

    assert (Path(tmpdir) / "document_info.csv").exists()
    assert count_lines((Path(tmpdir) / "document_info.csv").read_text()) == 100
    assert (Path(tmpdir) / "footnotes.csv").exists()
    assert count_lines((Path(tmpdir) / "footnotes.csv").read_text()) == 417
    assert (Path(tmpdir) / "derivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "derivatives.csv").read_text()) == 81
    assert (Path(tmpdir) / "nonderivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "nonderivatives.csv").read_text()) == 182
    assert (Path(tmpdir) / "report_owners.csv").exists()
    assert count_lines((Path(tmpdir) / "report_owners.csv").read_text()) == 129
    assert (Path(tmpdir) / "signatures.csv").exists()
    assert count_lines((Path(tmpdir) / "signatures.csv").read_text()) == 123


def test_script_on_form5_collection(test_form5_collection, tmpdir):
    """
    Test script on a random sample of Form 5 documents
    :param test_form5_collection:
    :return:
    """
    result = runner.invoke(
        app,
        [str(test_form5_collection), "--out_dir", str(tmpdir)],
    )
    assert result.exit_code == 0
    assert "processing files in dir" in result.stdout
    assert "generating output in dir" in result.stdout
    assert result.stdout.count("processing file:") == 100

    assert (Path(tmpdir) / "document_info.csv").exists()
    assert count_lines((Path(tmpdir) / "document_info.csv").read_text()) == 100
    assert (Path(tmpdir) / "footnotes.csv").exists()
    assert count_lines((Path(tmpdir) / "footnotes.csv").read_text()) == 546
    assert (Path(tmpdir) / "derivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "derivatives.csv").read_text()) == 138
    assert (Path(tmpdir) / "nonderivatives.csv").exists()
    assert count_lines((Path(tmpdir) / "nonderivatives.csv").read_text()) == 286
    assert (Path(tmpdir) / "report_owners.csv").exists()
    assert count_lines((Path(tmpdir) / "report_owners.csv").read_text()) == 102
    assert (Path(tmpdir) / "signatures.csv").exists()
    assert count_lines((Path(tmpdir) / "signatures.csv").read_text()) == 102
