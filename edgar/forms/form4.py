"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

from typing import List, Dict
from pathlib import Path
from edgar.forms.secdoc import Document


class Form4(Document):
    """
    Represents SEC document Form 4
    """

    # Non-derivatives transactions and holdings info in XML section
    # key -> document field name
    # value -> XML path used to extract key value from document
    xml_nonderivative_fields: Dict[str, str] = {
        "security_title": "securityTitle",
        "transaction_date": "transactionDate",
        "deemed_execution_date": "deemedExecutionDate",
        "transaction_acquired_disposed_code": "transactionAmounts/transactionAcquiredDisposedCode",
        "transaction_timeliness": "transactionTimeliness",
        "transaction_price_per_share": "transactionAmounts/transactionPricePerShare",
        "transaction_shares": "transactionAmounts/transactionShares",
        "direct_or_indirect_ownership": "ownershipNature/directOrIndirectOwnership",
        "nature_of_ownership": "ownershipNature/natureOfOwnership",
        "transaction_form_type": "transactionCoding/transactionFormType",
        "equity_swap_involved": "transactionCoding/equitySwapInvolved",
        "shares_owned_following_transaction": "postTransactionAmounts/sharesOwnedFollowingTransaction",
        "value_owned_following_transaction": "postTransactionAmounts/valueOwnedFollowingTransaction",
        "transaction_code": "transactionCoding/transactionCode",
    }

    # Derivatives transactions and holdings info in XML section
    # key -> document field name
    # value -> XML path used to extract key value from document
    xml_derivative_fields: Dict[str, str] = {
        "security_title": "securityTitle",
        "conversion_or_exercise_price": "conversionOrExercisePrice",
        "transaction_date": "transactionDate",
        "deemed_execution_date": "deemedExecutionDate",
        "transaction_form_type": "transactionCoding/transactionFormType",
        "transaction_code": "transactionCoding/transactionCode",
        "equity_swap_involved": "transactionCoding/equitySwapInvolved",
        "transaction_acquired_disposed_code": "transactionAmounts/transactionAcquiredDisposedCode",
        "transaction_price_per_share": "transactionAmounts/transactionPricePerShare",
        "transaction_shares": "transactionAmounts/transactionShares",
        "transaction_total_value": "transactionAmounts/transactionTotalValue",
        "transaction_timeliness": "transactionTimeliness",
        "exercise_date": "exerciseDate",
        "expiration_date": "expirationDate",
        "underlying_security_title": "underlyingSecurity/underlyingSecurityTitle",
        "underlying_security_shares": "underlyingSecurity/underlyingSecurityShares",
        "underlying_security_value": "underlyingSecurity/underlyingSecurityValue",
        "value_owned_following_transaction": "postTransactionAmounts/valueOwnedFollowingTransaction",
        "shares_owned_following_transaction": "postTransactionAmounts/sharesOwnedFollowingTransaction",
        "direct_or_indirect_ownership": "ownershipNature/directOrIndirectOwnership",
        "nature_of_ownership": "ownershipNature/natureOfOwnership",
    }

    def __init__(
        self, file: Path, replace: Dict[str, str] = {"true": "1", "false": "0"}
    ):
        """
        Initialize the Form4 object from the contents of the file parameter.
        :param file: File source of the document
        :param replace: A dictionary that can be used to replace and normalize extracted values, e.g. "true" => "1"
        """
        Document.__init__(self, file, replace)

        self._footnotes = []
        self._nonderivatives_dict_list = []
        self._derivatives_dict_list = []

        dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form4.xml_nonderivative_fields,
            xml_path="nonDerivativeTable/nonDerivativeTransaction",
            row_type="nonDerivTrans",
        )
        self._nonderivatives_dict_list.extend(dict_list)
        self._footnotes.extend(footnotes)

        dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form4.xml_nonderivative_fields,
            xml_path="nonDerivativeTable/nonDerivativeHolding",
            row_type="nonDerivHolding",
        )
        self._nonderivatives_dict_list.extend(dict_list)
        self._footnotes.extend(footnotes)

        dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form4.xml_derivative_fields,
            xml_path="derivativeTable/derivativeTransaction",
            row_type="derivTrans",
        )
        self._derivatives_dict_list.extend(dict_list)
        self._footnotes.extend(footnotes)

        dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form4.xml_derivative_fields,
            xml_path="derivativeTable/derivativeHolding",
            row_type="derivHolding",
        )
        self._derivatives_dict_list.extend(dict_list)
        self._footnotes.extend(footnotes)

    @property
    def nonderivatives(self) -> List[Dict[str, str]]:
        """
        The non-derivative transactions and holdings info. Maybe be zero or more in a document.
        :return: List[Dict[str, str]]
        """
        return self._nonderivatives_dict_list

    @property
    def derivatives(self) -> List[Dict[str, str]]:
        """
        The derivative transactions and holdings info. Maybe be zero or more in a document.
        :return: List[Dict[str, str]]
        """
        return self._derivatives_dict_list

    @property
    def footnotes(self) -> List[Dict[str, str]]:
        """
        The footnotes info. Maybe be zero or more in a document.
        :return: List[Dict[str, str]]
        """
        return self._footnotes
