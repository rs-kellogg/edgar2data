"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict


class Form13:
    """
    Represents a generic SEC document
    """

    xml_pat = re.compile(r"<XML>(.+?)</XML>", flags=re.DOTALL)

    # document level info outside of XML section
    # key -> document field name
    # value -> regualar expression used to extract key value from document
    header_fields: Dict[str, re.Pattern] = {
        "accession_num": re.compile(r"ACCESSION NUMBER:\s*([\d-]+)"),
        "sec_accept_datetime": re.compile(r"<ACCEPTANCE-DATETIME>(\d{14})"),
        "sec_file_num": re.compile(r"SEC FILE NUMBER:\s*([\d-]+)"),
        "doc_count": re.compile(r"PUBLIC DOCUMENT COUNT:\s*(\d+)"),
        "filed_date": re.compile(r"FILED AS OF DATE:\s*(\d{8})"),
        "conformed_period_of_report": re.compile(
            r"CONFORMED PERIOD OF REPORT:\s*(\d{8})"
        ),
        "change_date": re.compile(r"DATE AS OF CHANGE:\s*(\d{8})"),
        "filer_cik": re.compile(
            r"FILER:.+COMPANY\s+DATA:.+CENTRAL\s+INDEX\s+KEY:\s*(\d+)", re.DOTALL
        ),
    }

    def __init__(self, file: Path, replace: Dict[str, str] = {}):
        """
        Initialize the Document object from the contents of the file parameter.
        :param file: File source of the document
        :param replace: A dictionary that can be used to replace and normalize extracted values, e.g. "true" => "1"
        """
        assert file.exists() and file.is_file()
        self.path = file
        doc_text = file.read_text()
        match = Form13.xml_pat.findall(doc_text)
        assert match is not None and len(match) == 2
        self.xml_root1 = ET.fromstring(match[0].strip())
        self.xml_root2 = ET.fromstring(match[1].strip())
        self.replace = replace

        self._doc_field_dict = {"filename": self.path.name}
        for field, pat in Form13.header_fields.items():
            match = pat.findall(doc_text)
            self._doc_field_dict[field] = match[0].strip() if match else None

    @property
    def accession_num(self) -> str:
        """
        Return the accession number of the document
        :return: str
        """
        return self._doc_field_dict["accession_num"]

    @property
    def filename(self) -> str:
        """
        Return the filename of the source file for the document
        :return: str
        """
        return self._doc_field_dict["filename"]

    @property
    def doc_info(self) -> Dict[str, str]:
        """
        Return the document level information for the document
        :return: Dict[str, str]
        """
        return self._doc_field_dict
