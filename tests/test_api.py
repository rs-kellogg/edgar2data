"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from edgar.api import app


client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "edgar2data service"}


def test_process_form3(test_form3):
    response = client.post(
        "/form",
        params={"filename": test_form3.name, "text": test_form3.read_text()},
    )
    assert response.status_code == 200
    json_resp = response.json()
    assert len(json_resp) == 24


def test_process_form4(test_form4):
    response = client.post(
        "/form",
        params={"filename": test_form4.name, "text": test_form4.read_text()},
    )
    assert response.status_code == 200
    json_resp = response.json()
    assert len(json_resp) == 23


def test_process_form5(test_form5):
    response = client.post(
        "/form",
        params={"filename": test_form5.name, "text": test_form5.read_text()},
    )
    assert response.status_code == 200
    json_resp = response.json()
    assert len(json_resp) == 23
