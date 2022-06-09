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
def test_extract_report_owner_form3_collection(test_form3_collection, doc_num: int):
    """
    Validate Form3 extraction code against a random sample of documents
    :param test_form3_collection:
    :return:
    """
    file = list(test_form3_collection.glob('*.txt'))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.report_owners
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "reportingOwner"
        assert fields["index"] == f"reportingOwner{idx+1}"

        assert validate(file, fields["rpt_owner_cik"], r"\d{10}")
        assert validate(file, fields["rpt_owner_name"], r".+")
        assert validate(file, fields["rpt_owner_city"], r".+")
        assert validate(file, fields["is_director"], r"[10]", none_allowed=True)
        assert validate(file, fields["is_officer"], r"[10]", none_allowed=True)
        assert validate(
            file, fields["is_ten_percent_owner"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["is_other"], r"[10]", none_allowed=True)


def test_extract_report_owner_form3(test_form3):
    """
    Validate Form3 extraction code against a single detailed example
    :param test_form3:
    :return:
    """
    doc = Form3(test_form3)

    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name

    fields_list = doc.report_owners
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 19

    assert fields_list[0]["filename"] == test_form3.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "reportingOwner"
    assert fields_list[0]["index"] == "reportingOwner1"
    assert fields_list[0]["rpt_owner_cik"] == "0001676526"
    assert fields_list[0]["rpt_owner_name"] == "Lawler John T."
    assert fields_list[0]["rpt_owner_street1"] == "ONE AMERICAN ROAD"
    assert fields_list[0]["rpt_owner_street2"] is None
    assert fields_list[0]["rpt_owner_city"] == "DEARBORN"
    assert fields_list[0]["rpt_owner_state"] == "MI"
    assert fields_list[0]["rpt_owner_zip_code"] == "48126"
    assert fields_list[0]["rpt_owner_state_descr"] is None
    assert fields_list[0]["is_director"] == "0"
    assert fields_list[0]["is_officer"] == "1"
    assert fields_list[0]["is_ten_percent_owner"] == "0"
    assert fields_list[0]["is_other"] == "0"
    assert fields_list[0]["officer_title"] == "Vice President, CFO"
    assert fields_list[0]["other_text"] is None


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_report_owner_form4_collection(test_form4_collection, doc_num: int):
    """
    Validate Form4 extraction code against a random sample of documents
    :param test_form4_collection:
    :return:
    """
    file = list(test_form4_collection.glob('*.txt'))[doc_num]
    doc = Form4(file)
    assert doc.filename == file.name
    fields_list = doc.report_owners
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "reportingOwner"
        assert fields["index"] == f"reportingOwner{idx+1}"

        assert validate(file, fields["rpt_owner_cik"], r"\d{10}")
        assert validate(file, fields["rpt_owner_name"], r".+")
        assert validate(file, fields["rpt_owner_city"], r".+")
        assert validate(file, fields["is_director"], r"[10]", none_allowed=True)
        assert validate(file, fields["is_officer"], r"[10]", none_allowed=True)
        assert validate(
            file, fields["is_ten_percent_owner"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["is_other"], r"[10]", none_allowed=True)


def test_extract_report_owner_form4(test_form4):
    """
    Validate Form4 extraction code against a single detailed example
    :param test_form4:
    :return:
    """
    doc = Form4(test_form4)

    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name

    fields_list = doc.report_owners
    assert len(fields_list) == 2
    assert len(fields_list[0]) == 19

    assert fields_list[0]["filename"] == test_form4.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "reportingOwner"
    assert fields_list[0]["index"] == "reportingOwner1"
    assert fields_list[0]["rpt_owner_cik"] == "0001705562"
    assert fields_list[0]["rpt_owner_name"] == "Hodges Philip"
    assert fields_list[0]["rpt_owner_street1"] == "C/O ALTIMMUNE, INC."
    assert fields_list[0]["rpt_owner_street2"] == "19 FIRSTFIELD ROAD, SUITE 200"
    assert fields_list[0]["rpt_owner_city"] == "GAITHERSBURG"
    assert fields_list[0]["rpt_owner_state"] == "MD"
    assert fields_list[0]["rpt_owner_zip_code"] == "20878"
    assert fields_list[0]["rpt_owner_state_descr"] is None
    assert fields_list[0]["is_director"] == "1"
    assert fields_list[0]["is_officer"] == "0"
    assert fields_list[0]["is_ten_percent_owner"] == "0"
    assert fields_list[0]["is_other"] == "0"
    assert fields_list[0]["officer_title"] is None
    assert fields_list[0]["other_text"] is None

    assert len(fields_list[1]) == 19
    assert fields_list[1]["filename"] == test_form4.name
    assert fields_list[1]["accession_num"] == doc.accession_num
    assert fields_list[1]["order"] == "2"
    assert fields_list[1]["type"] == "reportingOwner"
    assert fields_list[1]["index"] == "reportingOwner2"
    assert fields_list[1]["rpt_owner_cik"] == "0001705638"
    assert fields_list[1]["rpt_owner_name"] == "Redmont VAXN Capital Holdings, LLC"
    assert fields_list[1]["rpt_owner_street1"] == "C/O ALTIMMUNE, INC."
    assert fields_list[1]["rpt_owner_street2"] == "19 FIRSTFIELD ROAD, SUITE 200"
    assert fields_list[1]["rpt_owner_city"] == "GAITHERSBURG"
    assert fields_list[1]["rpt_owner_state"] == "MD"
    assert fields_list[1]["rpt_owner_zip_code"] == "20878"
    assert fields_list[1]["rpt_owner_state_descr"] is None
    assert fields_list[1]["is_director"] == "1"
    assert fields_list[1]["is_officer"] == "0"
    assert fields_list[1]["is_ten_percent_owner"] == "0"
    assert fields_list[1]["is_other"] == "0"
    assert fields_list[1]["officer_title"] is None
    assert fields_list[1]["other_text"] is None


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_report_owner_form5_collection(test_form5_collection, doc_num: int):
    """
    Validate Form5 extraction code against a random sample of documents
    :param test_form5_collection:
    :return:
    """
    file = list(test_form5_collection.glob('*.txt'))[doc_num]
    doc = Form5(file)
    assert doc.filename == file.name
    fields_list = doc.report_owners
    assert len(fields_list) > 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "reportingOwner"
        assert fields["index"] == f"reportingOwner{idx+1}"

        assert validate(file, fields["rpt_owner_cik"], r"\d{10}")
        assert validate(file, fields["rpt_owner_name"], r".+")
        assert validate(file, fields["rpt_owner_city"], r".+")
        assert validate(file, fields["is_director"], r"[10]", none_allowed=True)
        assert validate(file, fields["is_officer"], r"[10]", none_allowed=True)
        assert validate(
            file, fields["is_ten_percent_owner"], r"[10]", none_allowed=True
        )
        assert validate(file, fields["is_other"], r"[10]", none_allowed=True)


def test_extract_report_owner_form5(test_form5):
    """
    Validate Form5 extraction code against a single detailed example
    :param test_form5:
    :return:
    """
    doc = Form5(test_form5)

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.report_owners
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 19

    assert fields_list[0]["filename"] == test_form5.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "reportingOwner"
    assert fields_list[0]["index"] == "reportingOwner1"
    assert fields_list[0]["rpt_owner_cik"] == "0001794251"
    assert fields_list[0]["rpt_owner_name"] == "Talisman Jonathan"
    assert fields_list[0]["rpt_owner_street1"] == "W. R. BERKLEY CORPORATION"
    assert fields_list[0]["rpt_owner_street2"] == "475 STEAMBOAT ROAD"
    assert fields_list[0]["rpt_owner_city"] == "GREENWICH"
    assert fields_list[0]["rpt_owner_state"] == "CT"
    assert fields_list[0]["rpt_owner_zip_code"] == "06830"
    assert fields_list[0]["rpt_owner_state_descr"] is None
    assert fields_list[0]["is_director"] == "1"
    assert fields_list[0]["is_officer"] == "0"
    assert fields_list[0]["is_ten_percent_owner"] == "0"
    assert fields_list[0]["is_other"] == "0"
    assert fields_list[0]["officer_title"] is None
    assert fields_list[0]["other_text"] is None
