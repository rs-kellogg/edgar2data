"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5


dir_path = os.path.dirname(os.path.realpath(__file__))


def test_extract_derivative_trans_form3_collection(test_form3_collection):
    for file in test_form3_collection.glob("*.txt"):
        doc = Form3(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.derivatives
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 12
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["order"] == f"{idx+1}"
            assert fields["type"] == "derivHolding"
            assert fields["index"] == f"derivHolding{idx+1}"
            assert fields["security_title"] is not None
            assert fields["conversion_or_exercise_price"] is not None
            assert fields["exercise_date"] is not None
            assert fields["expiration_date"] is not None
            assert fields["underlying_security_title"] is not None
            assert fields["underlying_security_shares"] is not None
            assert fields["direct_or_indirect_ownership"] is not None


def test_extract_derivative_trans_form3(test_form3):
    doc = Form3(test_form3, replace={"true": "1", "false": "0"})

    assert doc.accession_num == "0001209191-20-054135"
    assert doc.filename == test_form3.name

    fields_list = doc.derivatives
    assert len(fields_list) == 9

    assert len(fields_list[0]) == 12
    assert fields_list[0]["filename"] == test_form3.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "derivHolding"
    assert fields_list[0]["index"] == "derivHolding1"
    assert fields_list[0]["security_title"] == "BEP Ford Stock Fund Units"
    assert fields_list[0]["conversion_or_exercise_price"] == ""
    assert fields_list[0]["exercise_date"] == ""
    assert fields_list[0]["expiration_date"] == ""
    assert (
        fields_list[0]["underlying_security_title"] == "Common Stock, $0.01 par value"
    )
    assert fields_list[0]["underlying_security_shares"] == "65"
    assert fields_list[0]["direct_or_indirect_ownership"] == "D"

    assert len(fields_list[8]) == 12
    assert fields_list[8]["filename"] == test_form3.name
    assert fields_list[8]["accession_num"] == doc.accession_num
    assert fields_list[8]["order"] == "9"
    assert fields_list[8]["type"] == "derivHolding"
    assert fields_list[8]["index"] == "derivHolding9"
    assert fields_list[8]["security_title"] == "Ford Stock Units"
    assert fields_list[8]["conversion_or_exercise_price"] == ""
    assert fields_list[8]["exercise_date"] == ""
    assert fields_list[8]["expiration_date"] == ""
    assert (
        fields_list[8]["underlying_security_title"] == "Common Stock, $0.01 par value"
    )
    assert fields_list[8]["underlying_security_shares"] == "247533"
    assert fields_list[8]["direct_or_indirect_ownership"] == "D"


def test_extract_derivative_trans_form4_collection(test_form4_collection):
    for file in test_form4_collection.glob("*.txt"):
        doc = Form4(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.derivatives
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 26
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["order"] == f"{idx+1}"
            assert fields["type"] == "derivTrans"
            assert fields["index"] == f"derivTrans{idx+1}"
            assert fields["security_title"] is not None
            assert fields["transaction_date"] is not None
            assert fields["transaction_acquired_disposed_code"] is not None
            assert fields["transaction_price_per_share"] is not None
            assert fields["transaction_shares"] is not None
            assert fields["direct_or_indirect_ownership"] is not None
            assert fields["equity_swap_involved"] is not None
            assert fields["transaction_form_type"] is not None
            assert fields["shares_owned_following_transaction"] is not None
            assert fields["transaction_code"] is not None


def test_extract_derivative_trans_form4(test_form4):

    print(test_form4)
    doc = Form4(test_form4, replace={"true": "1", "false": "0"})

    assert doc.accession_num == "0001012975-17-000759"
    assert doc.filename == test_form4.name

    fields_list = doc.derivatives
    assert len(fields_list) == 1
    assert len(fields_list[0]) == 26
    assert fields_list[0]["filename"] == test_form4.name
    assert fields_list[0]["accession_num"] == doc.accession_num
    assert fields_list[0]["order"] == "1"
    assert fields_list[0]["type"] == "derivTrans"
    assert fields_list[0]["index"] == "derivTrans1"
    assert fields_list[0]["security_title"] == "Stock Options (option to buy)"
    assert fields_list[0]["transaction_date"] == "2017-10-13"
    assert fields_list[0]["deemed_execution_date"] is None
    assert fields_list[0]["transaction_acquired_disposed_code"] == "A"
    assert fields_list[0]["transaction_timeliness"] is None
    assert fields_list[0]["transaction_price_per_share"] == "0"
    assert fields_list[0]["transaction_shares"] == "20000"
    assert fields_list[0]["direct_or_indirect_ownership"] == "D"
    assert fields_list[0]["equity_swap_involved"] == "0"
    assert fields_list[0]["nature_of_ownership"] == ""
    assert fields_list[0]["transaction_form_type"] == "4"
    assert fields_list[0]["shares_owned_following_transaction"] == "20000"
    assert fields_list[0]["value_owned_following_transaction"] is None
    assert fields_list[0]["transaction_code"] == "A"
    assert fields_list[0]["conversion_or_exercise_price"] == "2.50"
    assert fields_list[0]["transaction_total_value"] is None
    assert fields_list[0]["exercise_date"] == "2018-04-30"
    assert fields_list[0]["expiration_date"] == "2027-10-13"
    assert (
        fields_list[0]["underlying_security_title"] == "Common Stock, par value $0.0001"
    )
    assert fields_list[0]["underlying_security_shares"] == "20000"
    assert fields_list[0]["underlying_security_value"] is None


def test_extract_derivative_trans_form5_collection(test_form5_collection):
    for file in test_form5_collection.glob("*.txt"):
        doc = Form5(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.derivatives
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 26
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["order"] == f"{idx + 1}"
            assert fields["type"] == "derivTrans"
            assert fields["index"] == f"derivTrans{idx + 1}"
            assert fields["security_title"] is not None
            assert fields["transaction_date"] is not None
            assert fields["transaction_acquired_disposed_code"] is not None
            assert fields["transaction_price_per_share"] is not None
            assert fields["transaction_shares"] is not None
            assert fields["direct_or_indirect_ownership"] is not None
            assert fields["equity_swap_involved"] is not None
            assert fields["transaction_form_type"] is not None
            assert fields["shares_owned_following_transaction"] is not None
            assert fields["transaction_code"] is not None


def test_extract_derivative_trans_form5(test_form5):
    doc = Form5(test_form5, replace={"true": "1", "false": "0"})

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.derivatives
    assert len(fields_list) == 0
