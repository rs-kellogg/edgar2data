"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import os
from conftest import validate
from edgar.utils import extract_named_entities
from edgar.forms.form3 import Form3
from edgar.forms.form4 import Form4
from edgar.forms.form5 import Form5


def test_smoke():
    text = """
    Redmont VAXN Capital Holdings, LLC, a Delaware limited liability company (&quot;Redmont VAXN&quot;) 
    distributed to its members, pro rata and without consideration, 1,278,471 shares of the Issuer's common stock.
    """
    extract_named_entities(text)
