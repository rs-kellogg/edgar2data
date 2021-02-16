"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
from conftest import validate
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5

dir_path = os.path.dirname(os.path.realpath(__file__))


def test_extract_doclevel_form3_collection(test_form3_collection):
    """
    Validate Form3 extraction code against a random sample of documents
    :param test_form3_collection:
    :return:
    """
    for file in test_form3_collection.glob("*.txt"):
        doc = Form3(file)
        assert doc.filename == file.name
        fields = doc.doc_info
        assert len(fields) == 19
        assert fields["filename"] == file.name
        assert fields["schema_version"] == "X0206"
        assert fields["document_type"] == "3"

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["sec_accept_datetime"], r"\d{14,14}")
        assert validate(file, fields["sec_file_num"], r"[\d-]+")
        assert validate(file, fields["doc_count"], r"\d+")
        assert validate(file, fields["filed_date"], r"\d{8,8}")
        assert validate(file, fields["conformed_period_of_report"], r"\d{8,8}")
        assert validate(file, fields["change_date"], r"\d{8,8}")
        assert validate(file, fields["period_of_report"], r"\d\d\d\d-\d\d-\d\d")
        assert validate(
            file, fields["not_subject_to_section_16"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["issuer_cik"], r"\d+")
        assert validate(file, fields["issuer_name"], r".+")
        assert validate(file, fields["issuer_trading_symbol"], r"[A-Z\.]+")
        assert validate(file, fields["regcik"], r"\d+")
        assert validate(file, fields["regsic"], r"\d\d\d\d", none_allowed=True)
        assert validate(file, fields["no_securities_owned"], r"[01]")


def test_extract_doclevel_form3(test_form3):
    """
    Validate Form3 extraction code against a single detailed example
    :param test_form3:
    :return:
    """
    doc = Form3(test_form3)
    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name
    fields = doc.doc_info
    assert len(fields) == 19
    assert fields["filename"] == test_form3.name
    assert fields["accession_num"] == doc.accession_num
    assert fields["sec_accept_datetime"] == "20201007163300"
    assert fields["sec_file_num"] == "001-03950"
    assert fields["doc_count"] == "2"
    assert fields["filed_date"] == "20201007"
    assert fields["conformed_period_of_report"] == "20201001"
    assert fields["change_date"] == "20201007"
    assert fields["schema_version"] == "X0206"
    assert fields["document_type"] == "3"
    assert fields["period_of_report"] == "2020-10-01"
    assert fields["not_subject_to_section_16"] is None
    assert fields["issuer_cik"] == "0000037996"
    assert fields["issuer_name"] == "FORD MOTOR CO"
    assert fields["issuer_trading_symbol"] == "F"
    assert fields["remarks"] is None
    assert fields["regcik"] == "0000037996"
    assert fields["regsic"] == "3711"
    assert fields["no_securities_owned"] == "0"


def test_extract_doclevel_form4_collection(test_form4_collection):
    """
    Validate Form4 extraction code against a random sample of documents
    :param test_form4_collection:
    :return:
    """
    for file in test_form4_collection.glob("*.txt"):
        doc = Form4(file)
        assert doc.filename == file.name
        fields = doc.doc_info
        assert len(fields) == 18
        assert fields["filename"] == file.name
        assert fields["accession_num"] is not None
        assert fields["schema_version"] == "X0306"
        assert fields["document_type"] == "4"

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["sec_accept_datetime"], r"\d{14,14}")
        assert validate(file, fields["sec_file_num"], r"[\d-]+")
        assert validate(file, fields["doc_count"], r"\d+")
        assert validate(file, fields["filed_date"], r"\d{8,8}")
        assert validate(file, fields["conformed_period_of_report"], r"\d{8,8}")
        assert validate(file, fields["change_date"], r"\d{8,8}")
        assert validate(file, fields["period_of_report"], r"\d\d\d\d-\d\d-\d\d")
        assert validate(
            file, fields["not_subject_to_section_16"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["issuer_cik"], r"\d+")
        assert validate(file, fields["issuer_name"], r".+")
        assert validate(file, fields["issuer_trading_symbol"], r"[A-Z\.]+")
        assert validate(file, fields["regcik"], r"\d+")
        assert validate(file, fields["regsic"], r"\d\d\d\d", none_allowed=True)


def test_extract_doclevel_form4(test_form4):
    """
    Validate Form4 extraction code against a single detailed example
    :param test_form4:
    :return:
    """
    doc = Form4(test_form4)
    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name
    fields = doc.doc_info
    assert len(fields) == 18
    assert fields["filename"] == test_form4.name
    assert fields["accession_num"] == doc.accession_num
    assert fields["sec_accept_datetime"] == "20171017200436"
    assert fields["sec_file_num"] == "001-32587"
    assert fields["doc_count"] == "1"
    assert fields["filed_date"] == "20171017"
    assert fields["conformed_period_of_report"] == "20171013"
    assert fields["change_date"] == "20171017"
    assert fields["schema_version"] == "X0306"
    assert fields["document_type"] == "4"
    assert fields["period_of_report"] == "2017-10-13"
    assert fields["not_subject_to_section_16"] is None
    assert fields["issuer_cik"] == "0001326190"
    assert fields["issuer_name"] == "Altimmune, Inc."
    assert fields["issuer_trading_symbol"] == "ALT"
    assert fields["remarks"] is None
    assert fields["regcik"] == "0001326190"
    assert fields["regsic"] == "2834"


def test_extract_doclevel_form5_collection(test_form5_collection):
    """
    Validate Form5 extraction code against a random sample of documents
    :param test_form5_collection:
    :return:
    """
    for file in test_form5_collection.glob("*.txt"):
        doc = Form5(file)
        assert doc.filename == file.name
        fields = doc.doc_info
        assert len(fields) == 18
        assert fields["filename"] == file.name
        assert fields["accession_num"] is not None
        assert fields["schema_version"] == "X0306"
        assert fields["document_type"] == "5"

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["sec_accept_datetime"], r"\d{14,14}")
        assert validate(file, fields["sec_file_num"], r"[\d-]+")
        assert validate(file, fields["doc_count"], r"\d+")
        assert validate(file, fields["filed_date"], r"\d{8}")
        assert validate(file, fields["conformed_period_of_report"], r"\d{8}")
        assert validate(file, fields["change_date"], r"\d{8}")
        assert validate(file, fields["period_of_report"], r"\d\d\d\d-\d\d-\d\d")
        assert validate(
            file, fields["not_subject_to_section_16"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["issuer_cik"], r"\d+")
        assert validate(file, fields["issuer_name"], r".+")
        assert validate(file, fields["issuer_trading_symbol"], r"[A-Z\.;\s\.,]+")
        assert validate(file, fields["regcik"], r"\d+")
        assert validate(file, fields["regsic"], r"\d\d\d\d", none_allowed=True)


def test_extract_doclevel_form5(test_form5):
    """
    Validate Form5 extraction code against a single detailed example
    :param test_form5:
    :return:
    """
    doc = Form5(test_form5)
    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name
    fields = doc.doc_info
    assert len(fields) == 18
    assert fields["filename"] == test_form5.name
    assert fields["accession_num"] == doc.accession_num
    assert fields["sec_accept_datetime"] == "20200213162819"
    assert fields["sec_file_num"] == "001-15202"
    assert fields["doc_count"] == "1"
    assert fields["filed_date"] == "20200213"
    assert fields["conformed_period_of_report"] == "20191231"
    assert fields["change_date"] == "20200213"
    assert fields["schema_version"] == "X0306"
    assert fields["document_type"] == "5"
    assert fields["period_of_report"] == "2019-12-31"
    assert fields["not_subject_to_section_16"] is None
    assert fields["issuer_cik"] == "0000011544"
    assert fields["issuer_name"] == "BERKLEY W R CORP"
    assert fields["issuer_trading_symbol"] == "WRB"
    assert fields["remarks"] is None
    assert fields["regcik"] == "0000011544"
    assert fields["regsic"] == "6331"
