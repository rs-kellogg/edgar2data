"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
import pytest
from conftest import validate
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_signature_form3_collection(test_form3_collection, doc_num: int):
    """
    Validate Form3 extraction code against a random sample of documents
    :param test_form3_collection:
    :return:
    """
    file = list(test_form3_collection.glob('*.txt'))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.signatures
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 7
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "signature"
        assert fields["index"] == f"signature{idx+1}"

        assert validate(file, fields["signature_name"], r".+")
        assert validate(file, fields["signature_date"], r"\d\d\d\d-\d\d-\d\d")


def test_extract_signature_form3(test_form3):
    """
    Validate Form3 extraction code against a single detailed example
    :param test_form3:
    :return:
    """
    doc = Form3(test_form3)

    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name

    fields_list = doc.signatures
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 7

    assert fields_list[0]["filename"] == test_form3.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "signature"
    assert fields_list[0]["index"] == "signature1"
    assert fields_list[0]["signature_name"] == "Jerome F. Zaremba,\nAttorney-in-Fact"
    assert fields_list[0]["signature_date"] == "2020-10-07"


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_signature_form4_collection(test_form4_collection, doc_num: int):
    """
    Validate Form4 extraction code against a random sample of documents
    :param test_form4_collection:
    :return:
    """
    file = list(test_form4_collection.glob('*.txt'))[doc_num]
    doc = Form4(file)
    assert doc.filename == file.name
    fields_list = doc.signatures
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 7
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "signature"
        assert fields["index"] == f"signature{idx+1}"

        assert validate(file, fields["signature_name"], r".+")
        assert validate(file, fields["signature_date"], r"\d\d\d\d-\d\d-\d\d")


def test_extract_signature_form4(test_form4):
    """
    Validate Form4 extraction code against a single detailed example
    :param test_form4:
    :return:
    """
    doc = Form4(test_form4)

    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name

    fields_list = doc.signatures

    assert len(fields_list) == 2
    assert len(fields_list[0]) == 7

    assert fields_list[0]["filename"] == test_form4.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "signature"
    assert fields_list[0]["index"] == "signature1"
    assert (
        fields_list[0]["signature_name"]
        == "/s/ Ori Solomon, Attorney in fact for Philip Hodges"
    )
    assert fields_list[0]["signature_date"] == "2017-10-17"

    assert fields_list[1]["filename"] == test_form4.name
    assert fields_list[1]["accession_num"] == doc.accession_num
    assert fields_list[1]["order"] == "2"
    assert fields_list[1]["type"] == "signature"
    assert fields_list[1]["index"] == "signature2"
    assert (
        fields_list[1]["signature_name"]
        == "/s/ Ori Solomon, Attorney in fact for Redmont VAXN Capital Holdings, LLC"
    )
    assert fields_list[1]["signature_date"] == "2017-10-17"


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_signature_form5_collection(test_form5_collection, doc_num: int):
    """
    Validate Form5 extraction code against a random sample of documents
    :param test_form5_collection:
    :return:
    """
    file = list(test_form5_collection.glob('*.txt'))[doc_num]
    doc = Form5(file)
    assert doc.filename == file.name
    fields_list = doc.signatures
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 7
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "signature"
        assert fields["index"] == f"signature{idx+1}"

        assert validate(file, fields["signature_name"], r".+")
        assert validate(file, fields["signature_date"], r"\d\d\d\d-\d\d-\d\d")


def test_extract_signature_form5(test_form5):
    """
    Validate Form5 extraction code against a single detailed example
    :param test_form5:
    :return:
    """
    doc = Form5(test_form5)

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.signatures
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 7

    assert fields_list[0]["filename"] == test_form5.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "signature"
    assert fields_list[0]["index"] == "signature1"
    assert fields_list[0]["signature_name"] == "Jonathan Talisman"
    assert fields_list[0]["signature_date"] == "2020-02-13"
