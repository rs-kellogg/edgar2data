"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict


class Document:
    """
    Represents a generic SEC document
    """

    xml_pat = re.compile(r"<XML>(.+)</XML>", flags=re.DOTALL)

    header_fields: Dict[str, re.Pattern] = {
        "accession_num": re.compile(r"ACCESSION NUMBER:(.+?)$", flags=re.MULTILINE),
        "sec_accept_datetime": re.compile(
            r"<ACCEPTANCE-DATETIME>(.+?)$", flags=re.MULTILINE
        ),
        "sec_file_num": re.compile(r"SEC FILE NUMBER:(.+?)$", flags=re.MULTILINE),
        "doc_count": re.compile(r"PUBLIC DOCUMENT COUNT:(.+?)$", flags=re.MULTILINE),
        "filed_date": re.compile(r"FILED AS OF DATE:(.+?)$", flags=re.MULTILINE),
        "conformed_period_of_report": re.compile(
            r"CONFORMED PERIOD OF REPORT:(.+?)$", flags=re.MULTILINE
        ),
        "change_date": re.compile(r"DATE AS OF CHANGE:(.+?)$", flags=re.MULTILINE),
        "regcik": re.compile(
            r"^ISSUER.+COMPANY\s+DATA.+CENTRAL\s+INDEX\s+KEY:(.+?)$",
            re.MULTILINE | re.DOTALL,
        ),
        "regsic": re.compile(
            r"^ISSUER.+COMPANY\s+DATA.+STANDARD INDUSTRIAL CLASSIFICATION:.+?\[(.+?)\]$",
            re.MULTILINE | re.DOTALL,
        ),
    }

    xml_document_fields: Dict[str, str] = {
        "schema_version": "schemaVersion",
        "document_type": "documentType",
        "period_of_report": "periodOfReport",
        "not_subject_to_section_16": "notSubjectToSection16",
        "issuer_cik": "issuer/issuerCik",
        "issuer_name": "issuer/issuerName",
        "issuer_trading_symbol": "issuer/issuerTradingSymbol",
        "remarks": "remarks",
    }

    xml_report_owner_fields: Dict[str, str] = {
        "rpt_owner_cik": "reportingOwnerId/rptOwnerCik",
        "rpt_owner_name": "reportingOwnerId/rptOwnerName",
        "rpt_owner_street1": "reportingOwnerAddress/rptOwnerStreet1",
        "rpt_owner_street2": "reportingOwnerAddress/rptOwnerStreet2",
        "rpt_owner_city": "reportingOwnerAddress/rptOwnerCity",
        "rpt_owner_state": "reportingOwnerAddress/rptOwnerState",
        "rpt_owner_zip_code": "reportingOwnerAddress/rptOwnerZipCode",
        "rpt_owner_state_descr": "reportingOwnerAddress/rptOwnerStateDescription",
        "is_director": "reportingOwnerRelationship/isDirector",
        "is_officer": "reportingOwnerRelationship/isOfficer",
        "is_ten_percent_owner": "reportingOwnerRelationship/isTenPercentOwner",
        "is_other": "reportingOwnerRelationship/isOther",
        "officer_title": "reportingOwnerRelationship/officerTitle",
        "other_text": "reportingOwnerRelationship/otherText",
    }

    xml_signature_fields: Dict[str, str] = {
        "signature_name": "signatureName",
        "signature_date": "signatureDate",
    }

    @property
    def accession_num(self) -> str:
        """
        :return: str
        """
        return self._doc_field_dict["accession_num"]

    @property
    def filename(self) -> str:
        """
        :return: str
        """
        return self._doc_field_dict["filename"]

    @property
    def doc_info(self) -> Dict[str, str]:
        """
        :return: Dict[str, str]
        """
        return self._doc_field_dict

    @property
    def report_owners(self) -> List[Dict[str, str]]:
        """
        :return: List[Dict[str, str]]
        """
        return self._report_owner_dict_list

    @property
    def signatures(self) -> List[Dict[str, str]]:
        """
        :return: List[Dict[str, str]]
        """
        return self._signature_dict_list

    def __init__(self, file: Path, replace: Dict[str, str] = {}):
        """

        :param file:
        :param replace:
        """
        assert file.exists() and file.is_file()
        self.path = file
        doc_text = file.read_text()
        match = Document.xml_pat.findall(doc_text)
        assert match is not None and len(match) == 1
        self.xml_root = ET.fromstring(match[0].strip())
        self.replace = replace

        self._doc_field_dict = {"filename": self.path.name}
        for field, pat in Document.header_fields.items():
            match = pat.findall(doc_text)
            self._doc_field_dict[field] = match[0].strip() if match else None
        for field, path in Document.xml_document_fields.items():
            child = self.xml_root.find(path)
            text = child.text if child is not None else None
            if text is not None and text.lower() in self.replace:
                text = self.replace[text.lower()]
            self._doc_field_dict[field] = text
        self._report_owner_dict_list, _ = self._extract_xml_fields(
            field_dict=Document.xml_report_owner_fields,
            xml_path="reportingOwner",
            row_type="reportingOwner",
        )
        self._signature_dict_list, _ = self._extract_xml_fields(
            field_dict=Document.xml_signature_fields,
            xml_path="ownerSignature",
            row_type="signature",
        )

    def _extract_xml_fields(
        self,
        field_dict: Dict[str, str],
        xml_path: str,
        row_type: str = None,
    ) -> (List[Dict[str, str]], List[Dict[str, str]]):

        row_dicts: List[Dict] = []
        footnotes: List[Dict] = []

        children = self.xml_root.findall(xml_path)
        for idx, child in enumerate(children):
            row_dict = {
                "filename": self.filename,
                "accession_num": self.accession_num,
                "order": str(idx + 1),
            }
            if row_type is not None:
                row_dict["type"] = row_type
                row_dict["index"] = row_type + str(idx + 1)
                footnotes.extend(
                    self._extract_footnotes(
                        child,
                        row_dict["index"],
                    )
                )

            for field, xml_path in field_dict.items():
                target = child.find(xml_path)
                if target is None:
                    text = None
                else:
                    value = target.find("value")
                    if value is not None:
                        text = value.text if value.text is not None else ""
                    else:
                        text = target.text
                    if text:
                        text = text.strip()
                if text is not None and text.lower() in self.replace:
                    text = self.replace[text.lower()]
                row_dict[field] = text
            row_dicts.append(row_dict)
        return row_dicts, footnotes

    def _extract_footnotes(self, parent: ET, index) -> List[Dict[str, str]]:
        row_dicts: List[Dict] = []
        parent_map = {c: p for p in parent.iter() for c in p if c.tag == "footnoteId"}
        for fnote, parent in parent_map.items():
            fnote_text = self.xml_root.find(
                f"footnotes/footnote/[@id = '{fnote.attrib['id']}']"
            ).text
            row_dict = {
                "filename": self.filename,
                "accession_num": self.accession_num,
                "footnote": fnote.attrib["id"],
                "index": index,
                "field": parent.tag,
                "text": fnote_text,
            }
            row_dicts.append(row_dict)
        return row_dicts
