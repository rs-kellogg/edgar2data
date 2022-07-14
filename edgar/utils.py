"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import typer
import re
import csv
from typing import List, Dict, Union
from pathlib import Path
from edgar.forms.secdoc import Document
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5


def create_doc(file: Path) -> Union[None, Document]:
    """
    A factory function returns a Document object with the right subtype.
    :param file: The file object that is the source of the Document
    :return: A Document object
    """
    xmlpath = Document.xml_document_fields["document_type"]
    regex = re.compile(f"<{xmlpath}>(.+)</{xmlpath}>")
    form_type = regex.findall(file.read_text())[0]
    if form_type == "3":
        return Form3(file)
    elif form_type == "4":
        return Form4(file)
    elif form_type == "5":
        return Form5(file)
    else:
        typer.secho(
            f"WARNING: {form_type} not a supported form type", fg=typer.colors.RED
        )
        return None


def write_records(row_dicts: List[Dict[str, str]], out_file: Path) -> None:
    """
    Accept input data in the form of a list of dicts, and append them to the output file.
    If the output file doesn't exist, it will be created and the keys of the first dict
    will be used to generate a header.
    :param row_dicts: List of dictionaries, each of which contains a row's worth of data
    :param out_file: The output file to be created or appended
    :return: None
    """
    if len(row_dicts) == 0:
        return
    if not out_file.exists():
        csv_writer = csv.writer(open(out_file, "a+", newline=""))
        csv_writer.writerow(row_dicts[0].keys())
    with open(out_file, "a+", newline="") as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        for row_dict in row_dicts:
            csv_writer.writerow(row_dict.values())
