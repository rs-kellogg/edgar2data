"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import typer
import os
import re
import csv
from typing import Optional, List, Dict
from pathlib import Path
from edgar.forms.secdoc import Document
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5

app = typer.Typer()


@app.command()
def process(
    in_dir: Path = typer.Argument(
        ..., help="The directory containing the input form files"
    ),
    out_dir: Optional[Path] = typer.Option(
        None,
        "--out_dir",
        help="The directory where the output flat files will be created. Defaults to the current working directory",
    ),
) -> None:
    """
    This function expects to be given a directory containing SEC files. Currently supported forms are
    insider trading filings;

    (1) form3, (2) form4, (3) form5

    The function will process each file and extract the information into a set of 6 flat csv files:
    (1) document_info.csv,
    (2) report_owners.csv,
    (3) signatures.csv,
    (4) footnotes.csv,
    (5) derivatives.csv,git
    (6) nonderivatives.csv.
    """
    assert in_dir.is_dir()
    if out_dir is not None:
        assert not out_dir.is_file()
        out_dir.mkdir(exist_ok=True)
    else:
        out_dir = Path(os.getcwd())

    typer.secho(
        f"processing files in dir: {in_dir}",
        fg=typer.colors.BLACK,
        bg=typer.colors.YELLOW,
    )
    typer.secho(
        f"generating output in dir: {out_dir}",
        fg=typer.colors.BLACK,
        bg=typer.colors.YELLOW,
    )

    for file in in_dir.glob("*.txt"):
        typer.secho(f"processing file: {file.name}", fg=typer.colors.YELLOW)
        assert file.is_file()

        try:
            doc = create_doc(file)
            write_records([doc.doc_info], out_file=out_dir / "document_info.csv")
            write_records(doc.report_owners, out_file=out_dir / "report_owners.csv")
            write_records(doc.nonderivatives, out_file=out_dir / "nonderivatives.csv")
            write_records(doc.derivatives, out_file=out_dir / "derivatives.csv")
            write_records(doc.signatures, out_file=out_dir / "signatures.csv")
            write_records(doc.footnotes, out_file=out_dir / "footnotes.csv")
        except Exception as e:
            typer.secho(f"ERROR: {file.name}: {str(e)}", fg=typer.colors.RED)
            return 1


def create_doc(file: Path) -> Document:
    xmlpath = Document.xml_document_fields["document_type"]
    regex = re.compile(f"<{xmlpath}>(.+)</{xmlpath}>")
    form_type = regex.findall(file.read_text())[0]
    if form_type == "3":
        return Form3(file, replace={"true": "1", "false": "0"})
    elif form_type == "4":
        return Form4(file, replace={"true": "1", "false": "0"})
    elif form_type == "5":
        return Form5(file, replace={"true": "1", "false": "0"})
    else:
        typer.secho(
            f"WARNING: {form_type} not a supported form type", fg=typer.colors.RED
        )
        return None


def write_records(row_dicts: List[Dict[str, str]], out_file: Path):
    if len(row_dicts) == 0:
        return
    if not out_file.exists():
        csv_writer = csv.writer(open(out_file, "a+", newline=""))
        csv_writer.writerow(row_dicts[0].keys())
    with open(out_file, "a+", newline="") as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for row_dict in row_dicts:
            csv_writer.writerow(row_dict.values())
