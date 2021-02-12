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


def test_extract_footnotes_form3_collection(test_form3_collection):
    for file in test_form3_collection.glob("*.txt"):
        doc = Form3(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.footnotes
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 6
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["footnote"] is not None
            assert fields["index"] is not None
            assert fields["field"] is not None
            assert fields["text"] is not None


def test_extract_footnotes_form3(test_form3):
    doc = Form3(test_form3, replace={"true": "1", "false": "0"})

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


def test_extract_footnotes_form4_collection(test_form4_collection):
    for file in test_form4_collection.glob("*.txt"):
        doc = Form3(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.footnotes
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 6
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["footnote"] is not None
            assert fields["index"] is not None
            assert fields["field"] is not None
            assert fields["text"] is not None


def test_extract_footnotes_form4(test_form4):
    doc = Form4(test_form4, replace={"true": "1", "false": "0"})

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


def test_extract_footnotes_form5_collection(test_form5_collection):
    for file in test_form5_collection.glob("*.txt"):
        doc = Form3(file, replace={"true": "1", "false": "0"})
        assert doc.filename == file.name
        fields_list = doc.footnotes
        assert len(fields_list) >= 0
        for idx, fields in enumerate(fields_list):
            assert (len(fields)) == 6
            assert fields["filename"] == file.name
            assert fields["accession_num"] == doc.accession_num
            assert fields["footnote"] is not None
            assert fields["index"] is not None
            assert fields["field"] is not None
            assert fields["text"] is not None


def test_extract_footnotes_form5(test_form5):
    doc = Form5(test_form5, replace={"true": "1", "false": "0"})

    assert doc.accession_num == "0000011544-20-000013"
    assert doc.filename == test_form5.name

    fields_list = doc.footnotes
    assert len(fields_list) == 0
