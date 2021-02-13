"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
import tempfile
import pytest
from pathlib import Path
from typer.testing import CliRunner
from edgar.cli import *

runner = CliRunner()

dir_path = os.path.dirname(os.path.realpath(__file__))


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
        assert sum(1 for line in open((Path(tmp_dir) / "document_info.csv"))) == 101
        assert (Path(tmp_dir) / "footnotes.csv").exists()
        assert sum(1 for line in open((Path(tmp_dir) / "footnotes.csv"))) == 417
        assert (Path(tmp_dir) / "report_owners.csv").exists()
        assert sum(1 for line in open((Path(tmp_dir) / "report_owners.csv"))) == 130
        assert (Path(tmp_dir) / "signatures.csv").exists()
        assert sum(1 for line in open((Path(tmp_dir) / "signatures.csv"))) == 140
        assert (Path(tmp_dir) / "derivatives.csv").exists()
        assert sum(1 for line in open((Path(tmp_dir) / "derivatives.csv"))) == 53
        assert (Path(tmp_dir) / "nonderivatives.csv").exists()
        assert sum(1 for line in open((Path(tmp_dir) / "nonderivatives.csv"))) == 150
