import pytest

from os import environ

from pg_analyse.toolbox import analyse_and_format
from pg_analyse.settings import ENV_VAR


@pytest.mark.skip
def test_analyse_and_format():
    environ[ENV_VAR] = 'dummy'
    out = analyse_and_format()
