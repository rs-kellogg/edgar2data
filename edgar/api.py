"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import tempfile
from pathlib import Path
from typing import Dict
from fastapi import FastAPI
from edgar.utils import create_doc


app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "edgar2data service"}


@app.post("/form")
async def process_form(filename: str, text: str) -> Dict[str, str]:
    """
    Accepts a filename and the text contents of a file, and returns a dicitonary with all
    information extracted. The filename is required in order to trace the contents back to
    source. However, the function caller can supply any string here and the code will accept it.
    :param filename:
    :param text:
    :return:
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        file = Path(tmp_dir) / filename
        file.write_text(text)
        doc = create_doc(file)
        return_dict = {**doc.doc_info, **{"report_owners": doc.report_owners}}
        return_dict = {**return_dict, **{"signatures": doc.signatures}}
        return_dict = {**return_dict, **{"derivatives": doc.derivatives}}
        return_dict = {**return_dict, **{"nonderivatives": doc.nonderivatives}}
        return_dict = {**return_dict, **{"footnotes": doc.footnotes}}
        # a cleaner way to do this for python version >= 3.9:
        # return_dict = (
        #     doc.doc_info
        #     | {"report_owners": doc.report_owners}
        #     | {"signatures": doc.signatures}
        #     | {"derivatives": doc.derivatives}
        #     | {"nonderivatives": doc.nonderivatives}
        #     | {"footnotes": doc.footnotes}
        # )
        return return_dict
