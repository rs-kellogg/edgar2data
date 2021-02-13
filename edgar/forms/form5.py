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

    def __init__(self, file: Path, replace: Dict[str, str] = {}):
        Form4.__init__(self, file, replace)
