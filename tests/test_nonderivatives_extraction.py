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
def test_extract_nonderivatives_form3_collection(test_form3_collection, doc_num: int):
    """
    Validate Form3 extraction code against a random sample of documents
    :param test_form3_collection:
    :return:
    """
    file = list(test_form3_collection.glob('*.txt'))[doc_num]
    doc = Form3(file)
    assert doc.filename == file.name
    fields_list = doc.nonderivatives
    assert len(fields_list) >= 0
    for idx, fields in enumerate(fields_list):
        assert (len(fields)) == 8
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "nonDerivHolding"
        assert fields["index"] == f"nonDerivHolding{idx+1}"

        assert validate(file, fields["security_title"], r".+")
        assert validate(
            file, fields["shares_owned_following_transaction"], r"[\d\.]+"
        )
        assert validate(file, fields["direct_or_indirect_ownership"], r"[DI]")


def test_extract_signature_form3(test_form3):
    """
    Validate Form3 extraction code against a single detailed example
    :param test_form3:
    :return:
    """
    doc = Form3(test_form3)

    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name

    fields_list = doc.nonderivatives
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 8
    assert fields_list[0]["filename"] == test_form3.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "nonDerivHolding"
    assert fields_list[0]["index"] == "nonDerivHolding1"
    assert fields_list[0]["security_title"] == "Common Stock, $0.01 par value"
    assert fields_list[0]["shares_owned_following_transaction"] == "157800"
    assert fields_list[0]["direct_or_indirect_ownership"] == "D"


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_nonderivative_trans_form4_collection(test_form4_collection, doc_num: int):
    """
    Validate Form4 extraction code against a random sample of documents
    :param test_form4_collection:
    :return:
    """
    file = list(test_form4_collection.glob('*.txt'))[doc_num]
    doc = Form4(file)
    assert doc.filename == file.name
    fields_list = doc.nonderivatives
    assert len(fields_list) >= 0

    trans_fields_list = [f for f in fields_list if f["type"] == "nonDerivTrans"]
    for idx, fields in enumerate(trans_fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "nonDerivTrans"
        assert fields["index"] == f"nonDerivTrans{idx+1}"

        assert validate(file, fields["security_title"], r".+")
        assert validate(file, fields["transaction_date"], r"\d\d\d\d-\d\d-\d\d")
        assert validate(file, fields["transaction_acquired_disposed_code"], r"[AD]")
        assert validate(file, fields["transaction_price_per_share"], r"[\d\.]*")
        assert validate(file, fields["transaction_shares"], r"[\d\.]*")
        assert validate(file, fields["direct_or_indirect_ownership"], r"[DI]")
        assert validate(file, fields["equity_swap_involved"], r"[10]")
        assert validate(file, fields["transaction_form_type"], r"[45]")
        assert validate(
            file, fields["shares_owned_following_transaction"], r"[\d\.]*"
        )
        assert validate(file, fields["transaction_code"], r"[A-Z]")

    holdings_fields_list = [
        f for f in fields_list if f["type"] == "nonDerivHolding"
    ]
    for idx, fields in enumerate(holdings_fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "nonDerivHolding"
        assert fields["index"] == f"nonDerivHolding{idx+1}"

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["security_title"], r".+")
        assert validate(file, fields["direct_or_indirect_ownership"], r"[DI]")


def test_extract_nonderivative_trans_form4(test_form4):
    """
    Validate Form4 extraction code against a single detailed example
    :param test_form4:
    :return:
    """
    doc = Form4(test_form4)

    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name

    fields_list = doc.nonderivatives
    assert len(fields_list) == 1
    assert fields_list[0]["filename"] == test_form4.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "nonDerivTrans"
    assert fields_list[0]["index"] == "nonDerivTrans1"
    assert fields_list[0]["security_title"] == "Common Stock, par value $0.0001"
    assert fields_list[0]["transaction_date"] == "2017-10-17"
    assert fields_list[0]["deemed_execution_date"] is None
    assert fields_list[0]["transaction_acquired_disposed_code"] == "D"
    assert fields_list[0]["transaction_timeliness"] is None
    assert fields_list[0]["transaction_price_per_share"] == "0"
    assert fields_list[0]["transaction_shares"] == "1278471"
    assert fields_list[0]["direct_or_indirect_ownership"] == "I"
    assert fields_list[0]["equity_swap_involved"] == "0"
    assert fields_list[0]["nature_of_ownership"] == "See Footnote"
    assert fields_list[0]["transaction_form_type"] == "4"
    assert fields_list[0]["shares_owned_following_transaction"] == "0"
    assert fields_list[0]["value_owned_following_transaction"] is None
    assert fields_list[0]["transaction_code"] == "J"


@pytest.mark.parametrize("doc_num", range(100))
def test_extract_nonderivative_trans_form5_collection(test_form5_collection, doc_num: int):
    """
    Validate Form5 extraction code against a random sample of documents
    :param test_form5_collection:
    :return:
    """
    file = list(test_form5_collection.glob('*.txt'))[doc_num]
    doc = Form5(file)
    assert doc.filename == file.name
    fields_list = doc.nonderivatives

    trans_fields_list = [f for f in fields_list if f["type"] == "nonDerivTrans"]
    for idx, fields in enumerate(trans_fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "nonDerivTrans"
        assert fields["index"] == f"nonDerivTrans{idx+1}"

        assert validate(file, fields["security_title"], r".+")
        assert validate(file, fields["transaction_date"], r"\d\d\d\d-\d\d-\d\d")
        assert validate(file, fields["transaction_acquired_disposed_code"], r"[AD]")
        assert validate(file, fields["transaction_price_per_share"], r"[\d\.]*")
        assert validate(file, fields["transaction_shares"], r"[\d\.]*")
        assert validate(file, fields["direct_or_indirect_ownership"], r"[DI]")
        assert validate(file, fields["equity_swap_involved"], r"[10]")
        assert validate(file, fields["transaction_form_type"], r"[45]")
        assert validate(
            file, fields["shares_owned_following_transaction"], r"[\d\.]*"
        )
        assert validate(file, fields["transaction_code"], r"[A-Z]")

    holdings_fields_list = [
        f for f in fields_list if f["type"] == "nonDerivHolding"
    ]
    for idx, fields in enumerate(holdings_fields_list):
        assert (len(fields)) == 19
        assert fields["filename"] == file.name
        assert fields["accession_num"] == doc.accession_num
        assert fields["order"] == f"{idx+1}"
        assert fields["type"] == "nonDerivHolding"
        assert fields["index"] == f"nonDerivHolding{idx+1}"

        assert validate(file, fields["accession_num"], r"[\d-]+")
        assert validate(file, fields["security_title"], r".+")
        assert validate(file, fields["direct_or_indirect_ownership"], r"[DI]")


def test_extract_nonderivative_trans_form5(test_form5):
    """
    Validate Form5 extraction code against a single detailed example
    :param test_form5:
    :return:
    """
    doc = Form5(test_form5)

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.nonderivatives
    assert len(fields_list) == 1
    assert fields_list[0]["filename"] == test_form5.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "nonDerivTrans"
    assert fields_list[0]["index"] == "nonDerivTrans1"
    assert fields_list[0]["security_title"] == "Common Stock"
    assert fields_list[0]["transaction_date"] == "2019-12-11"
    assert fields_list[0]["deemed_execution_date"] is None
    assert fields_list[0]["transaction_acquired_disposed_code"] == "A"
    assert fields_list[0]["transaction_timeliness"] is None
    assert fields_list[0]["transaction_price_per_share"] == "70.27"
    assert fields_list[0]["transaction_shares"] == "3"
    assert fields_list[0]["direct_or_indirect_ownership"] == "D"
    assert fields_list[0]["equity_swap_involved"] == "0"
    assert fields_list[0]["nature_of_ownership"] is None
    assert fields_list[0]["transaction_form_type"] == "5"
    assert fields_list[0]["shares_owned_following_transaction"] == "359"
    assert fields_list[0]["value_owned_following_transaction"] is None
    assert fields_list[0]["transaction_code"] == "P"
