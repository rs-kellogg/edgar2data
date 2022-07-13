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
def test_extract_footnotes_form3_collection(test_form3_collection, doc_num: int):
    """
    Validate Form3 extraction code against a random sample of documents
    :param test_form3_collection:
    :return:
    """
    file = list(test_form3_collection.glob("*.txt"))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.footnotes
    assert len(fields_list) >= 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 6
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["footnote"], r".+")
        assert validate(file, fields["index"], r"\w+\d+")
        assert validate(file, fields["field"], r"\w+")
        assert validate(file, fields["field"], r".+")


def test_extract_footnotes_form3(test_form3):
    """
    Validate Form3 extraction code against a single detailed example
    :param test_form3:
    :return:
    """
    doc = Form3(test_form3)

    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name

    fields_list = doc.footnotes
    assert len(fields_list) == 19
    assert len(fields_list[0]) == 6

    assert fields_list[0]["filename"] == test_form3.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["footnote"] == "F1"
    assert fields_list[0]["index"] == "derivHolding1"
    assert fields_list[0]["field"] == "conversionOrExercisePrice"
    assert fields_list[0]["text"][:27] == "These Ford Stock Fund Units"

    assert fields_list[18]["filename"] == test_form3.name
    assert fields_list[18]["accession_num"] == doc.accession_num
    assert fields_list[18]["footnote"] == "F9"
    assert fields_list[18]["index"] == "derivHolding9"
    assert fields_list[18]["field"] == "expirationDate"
    assert fields_list[18]["text"][:27] == "These Ford Restricted Stock"


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_footnotes_form4_collection(test_form4_collection, doc_num: int):
    """
    Validate Form4 extraction code against a random sample of documents
    :param test_form4_collection:
    :return:
    """
    file = list(test_form4_collection.glob("*.txt"))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.footnotes
    assert len(fields_list) >= 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 6
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["footnote"], r".+")
        assert validate(file, fields["index"], r"\w+\d+")
        assert validate(file, fields["field"], r"\w+")
        assert validate(file, fields["field"], r".+")


def test_extract_footnotes_form4(test_form4):
    """
    Validate Form4 extraction code against a single detailed example
    :param test_form4:
    :return:
    """
    doc = Form4(test_form4)

    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name

    fields_list = doc.footnotes
    assert len(fields_list) == 3
    assert len(fields_list[0]) == 6

    assert fields_list[0]["filename"] == test_form4.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["footnote"] == "F1"
    assert fields_list[0]["index"] == "nonDerivTrans1"
    assert fields_list[0]["field"] == "transactionCoding"
    assert fields_list[0]["text"][:26] == "Redmont VAXN Capital Holdi"

    assert fields_list[1]["filename"] == test_form4.name
    assert fields_list[1]["accession_num"] == doc.accession_num
    assert fields_list[1]["footnote"] == "F2"
    assert fields_list[1]["index"] == "nonDerivTrans1"
    assert fields_list[1]["field"] == "natureOfOwnership"
    assert fields_list[1]["text"][:26] == "Consists of shares of Comm"

    assert fields_list[2]["filename"] == test_form4.name
    assert fields_list[2]["accession_num"] == doc.accession_num
    assert fields_list[2]["footnote"] == "F3"
    assert fields_list[2]["index"] == "derivTrans1"
    assert fields_list[2]["field"] == "directOrIndirectOwnership"
    assert fields_list[2]["text"][:26] == "Held by Philip Hodges."


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_footnotes_form5_collection(test_form5_collection, doc_num: int):
    """
    Validate Form5 extraction code against a random sample of documents
    :param test_form5_collection:
    :return:
    """
    file = list(test_form5_collection.glob("*.txt"))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.footnotes
    assert len(fields_list) >= 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 6
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["footnote"], r".+")
        assert validate(file, fields["index"], r"\w+\d+")
        assert validate(file, fields["field"], r"\w+")
        assert validate(file, fields["field"], r".+")


def test_extract_footnotes_form5(test_form5):
    """
    Validate Form5 extraction code against a single detailed example
    :param test_form5:
    :return:
    """
    doc = Form5(test_form5)

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.footnotes
    assert len(fields_list) == 0


def test_extract_many_footnotes_example(test_form4_collection):
    file = test_form4_collection / "1363364_2_0001638599-20-000500.txt"
    assert file.exists()
    doc = Form4(file)
    footnotes = doc.footnotes
    assert len(footnotes) == 39
