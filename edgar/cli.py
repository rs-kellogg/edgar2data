"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
import typer
from rich.console import Console
from typing import Optional
from edgar.utils import *
from edgar.forms.form13 import Form13


app = typer.Typer()
console = Console()


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
) -> int:
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


@app.command()
def process_form_13(
    in_dir: Path = typer.Argument(
        ..., help="The directory containing the input form files"
    ),
    out_dir: Optional[Path] = typer.Option(
        None,
        "--out_dir",
        help="The directory where the output flat files will be created. Defaults to the current working directory",
    ),
) -> int:
    """
    This function expects to be given a directory containing SEC Form 13 files
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
            doc = Form13(file)
            write_records([doc.doc_info], out_file=out_dir / "document_info.csv")
            write_records(doc.info_tables, out_file=out_dir / "info_tables.csv")
        except Exception as e:
            typer.secho(f"ERROR: {file.name}: {str(e)}", fg=typer.colors.RED)

    return 0
