"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
import re
import tempfile
import pytest
from pathlib import Path
from typer.testing import CliRunner
from edgar.cli import *

runner = CliRunner()

dir_path = os.path.dirname(os.path.realpath(__file__))


def count_lines(text):
    matches = re.compile(r"^\".+?\.txt\"", re.MULTILINE).findall(text)
    return len(matches)


def test_script_on_form4():
    assert app is not None
    in_dir = Path(dir_path) / "data/form-4/sample/2020"
    assert in_dir.exists()
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_dir = Path(tmp_dir)
        assert out_dir.exists()
        result = runner.invoke(
            app,
            ["form4", str(in_dir), "--out_dir", str(tmp_dir)],
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
