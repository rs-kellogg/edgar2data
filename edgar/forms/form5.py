"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

from typing import List, Dict
from pathlib import Path
from edgar.forms.form4 import Form4


class Form5(Form4):
    """
    Represents SEC document Form 5
    """

    def __init__(
        self, file: Path, replace: Dict[str, str] = {"true": "1", "false": "0"}
    ):
        """
        Initialize the Document object from the contents of the file parameter.
        Note: Form % shares the same underlying schema as Form 4, so this class is not technically required,
        but is supplied for convenience, and in case Form 5 specific info needs to be added in the future.
        :param file: File source of the document
        :param replace: A dictionary that can be used to replace and normalize extracted values, e.g. "true" => "1"
        """
        Form4.__init__(self, file, replace)
