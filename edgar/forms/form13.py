"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import re
from lxml import etree as ET
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
        # "filer_name": re.compile(
        #     r"FILER:.+COMPANY\s+DATA:.+COMPANY\s+CONFORMED\s+NAME:\s*(.+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_cik": re.compile(
        #     r"FILER:.+COMPANY\s+DATA:.+CENTRAL\s+INDEX\s+KEY:\s*(\d+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_irs_number": re.compile(
        #     r"FILER:.+COMPANY\s+DATA:.+IRS\s+NUMBER:\s*(\d+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_state_of_incorporation": re.compile(
        #     r"FILER:.+COMPANY\s+DATA:.+STATE\s+OF\s+INCORPORATION:\s*(.+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_fiscal_year_end": re.compile(
        #     r"FILER:.+COMPANY\s+DATA:.+FISCAL\s+YEAR\s+END:\s*(\d+)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_city": re.compile(
        #     r"FILER:.+BUSINESS\s+ADDRESS:.+CITY:\s*(.+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_state": re.compile(
        #     r"FILER:.+BUSINESS\s+ADDRESS:.+STATE:\s*(.+?)$", re.DOTALL | re.MULTILINE
        # ),
        # "filer_zip": re.compile(
        #     r"FILER:.+BUSINESS\s+ADDRESS:.+ZIP:\s*(\d+?)$", re.DOTALL | re.MULTILINE
        # ),
    }

    # document level info in XML section 1
    # key -> document field name
    # value -> XML path used to extract key value from document
    edgar_submission_fields: Dict[str, str] = {
        "submission_type": "headerData/submissionType",
        "report_period": "headerData/filerInfo/periodOfReport",
        "cik": "headerData/filerInfo/filer/credentials/cik",
        "report_quarter": "formData/coverPage/reportCalendarOrQuarter",
        "name": "formData/coverPage/filingManager/name",
        "city": "formData/coverPage/filingManager/address/com:city",
        "state_or_country": "formData/coverPage/filingManager/address/com:stateOrCountry",
        "zip_code": "formData/coverPage/filingManager/address/com:zipCode",
        "table_entry_total": "formData/summaryPage/tableEntryTotal",
        "table_value_total": "formData/summaryPage/tableValueTotal",
    }

    # info table info in XML section 2
    # key -> document field name
    # value -> XML path used to extract key value from document
    info_table_fields: Dict[str, str] = {
        "issuer_name": "nameOfIssuer",
        "title_class": "titleOfClass",
        "cusip": "cusip",
        "value": "value",
        "ssh_prnamt": "shrsOrPrnAmt/sshPrnamt",
        "ssh_prnamt_type": "shrsOrPrnAmt/sshPrnamtType",
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
        self.xml_edgar_submission = ET.fromstring(match[0].strip().encode("utf-8"))
        self.xml_info_tables = ET.fromstring(match[1].strip().encode("utf-8"))
        self.replace = replace

        self._doc_field_dict: Dict[str, str] = {"filename": self.path.name}
        self._info_tables: List[Dict[str, str]] = []

        for field, pat in Form13.header_fields.items():
            match = pat.findall(doc_text)
            self._doc_field_dict[field] = match[0].strip() if match else None

        for field, path in Form13.edgar_submission_fields.items():
            child = self.xml_edgar_submission.find(
                path, self.xml_edgar_submission.nsmap
            )
            text = child.text if child is not None else None
            if text is not None and text.lower() in self.replace:
                text = self.replace[text.lower()]
            self._doc_field_dict[field] = text

        for xml_info_table in self.xml_info_tables.findall(
            "infoTable", self.xml_info_tables.nsmap
        ):
            info_dict = {}
            for field, path in Form13.info_table_fields.items():
                child = xml_info_table.find(path, self.xml_info_tables.nsmap)
                text = child.text if child is not None else None
                if text is not None and text.lower() in self.replace:
                    text = self.replace[text.lower()]
                info_dict[field] = text
            self._info_tables.append(info_dict)

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

    @property
    def info_tables(self) -> List[Dict[str, str]]:
        """
        Return the info tables for the document
        :return: List[Dict[str, str]]
        """
        return self._info_tables
