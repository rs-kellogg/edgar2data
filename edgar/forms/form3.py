"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

from typing import List, Dict
from pathlib import Path
from edgar.forms.secdoc import Document


class Form3(Document):
    """
    Represents SEC document Form 3
    """

    xml_document_fields_form3: Dict[str, str] = {
        "no_securities_owned": "noSecuritiesOwned"
    }

    xml_nonderivative_fields: Dict[str, str] = {
        "security_title": "securityTitle",
        "shares_owned_following_transaction": "postTransactionAmounts/sharesOwnedFollowingTransaction",
        "direct_or_indirect_ownership": "ownershipNature/directOrIndirectOwnership",
    }

    xml_derivative_fields: Dict[str, str] = {
        "security_title": "securityTitle",
        "conversion_or_exercise_price": "conversionOrExercisePrice",
        "exercise_date": "exerciseDate",
        "expiration_date": "expirationDate",
        "underlying_security_title": "underlyingSecurity/underlyingSecurityTitle",
        "underlying_security_shares": "underlyingSecurity/underlyingSecurityShares",
        "direct_or_indirect_ownership": "ownershipNature/directOrIndirectOwnership",
    }

    @property
    def nonderivatives(self) -> List[Dict[str, str]]:
        """
        :return: List[Dict[str, str]]
        """
        return self._nonderivatives_dict_list

    @property
    def derivatives(self) -> List[Dict[str, str]]:
        """
        :return: List[Dict[str, str]]
        """
        return self._derivatives_dict_list

    @property
    def footnotes(self) -> List[Dict[str, str]]:
        """
        :return: List[Dict[str, str]]
        """
        return self._footnotes

    def __init__(self, file: Path, replace: Dict[str, str] = {}):
        Document.__init__(self, file, replace)
        self._footnotes = []

        for field, path in Form3.xml_document_fields_form3.items():
            child = self.xml_root.find(path)
            text = child.text if child is not None else None
            if text is not None and text.lower() in self.replace:
                text = self.replace[text.lower()]
            self._doc_field_dict[field] = text

        self._nonderivatives_dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form3.xml_nonderivative_fields,
            xml_path="nonDerivativeTable/nonDerivativeHolding",
            row_type="nonDerivHolding",
        )
        self._footnotes.extend(footnotes)

        self._derivatives_dict_list, footnotes = self._extract_xml_fields(
            field_dict=Form3.xml_derivative_fields,
            xml_path="derivativeTable/derivativeHolding",
            row_type="derivHolding",
        )
        self._footnotes.extend(footnotes)
