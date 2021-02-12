"""
Copyright (c) 2021 Northwestern University. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""

import yaml
import pytest
import os
import re

from pathlib import Path

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))


def validate(
    file: Path,
    value: str,
    pattern: str,
    whole_string: bool = True,
    none_allowed: bool = False,
) -> bool:
    """
    Validate a string value using a regular expression constraint.
    :param file: source of the test value
    :param value: value to be tested
    :param pattern: regex pattern that will match the value
    :param whole_string: governs whether the match has to be the whole string, or just a prefix
    :param none_allowed: is None allowed as a value
    :return: whether or not the regex matches the value
    """
    if value is None and none_allowed:
        return True
    if whole_string:
        pattern = f"{pattern}$"
    if re.compile(pattern).match(value):
        return True
    print(f"Validate error in file {file}: '{value}' does not match {pattern}")
    return False


@pytest.fixture
def config():
    with open(Path(f"{dir_path}/config.yaml")) as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        return conf


@pytest.fixture
def test_form3_collection(config) -> Path:
    path = Path(dir_path) / "data/form-3/sample/2020"
    return path


@pytest.fixture
def test_form4_collection(config) -> Path:
    path = Path(dir_path) / "data/form-4/sample/2020"
    return path


@pytest.fixture
def test_form5_collection(config) -> Path:
    path = Path(dir_path) / "data/form-5/sample/2020"
    return path


@pytest.fixture
def test_form3(config) -> Path:
    file = Path(dir_path) / "data/form-3/37996_4_0001209191-20-054135.txt"
    return file


@pytest.fixture
def test_form4(config) -> Path:
    file = Path(dir_path) / "data/form-4/0001012975-17-000759.txt"
    return file


@pytest.fixture
def test_form5(config) -> Path:
    file = Path(dir_path) / "data/form-5/11544_1_0000011544-20-000013.txt"
    return file
