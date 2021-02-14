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


@app.post("/form")
async def process_form(filename: str, text: str) -> Dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        file = Path(tmp_dir) / filename
        file.write_text(text)
        doc = create_doc(file)
        return_dict = (
            doc.doc_info
            | {"report_owners": doc.report_owners}
            | {"signatures": doc.signatures}
            | {"derivatives": doc.derivatives}
            | {"nonderivatives": doc.nonderivatives}
            | {"footnotes": doc.footnotes}
        )
        return return_dict
