from collections import namedtuple

import pytest


class PgMock:

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    @property
    def description(self):
        column_descr = namedtuple('column_descr', ['name'])
        return [column_descr(column) for column in self.columns]

    def fetchall(self):
        return self.rows

    def connect(self, *arg, **kwargs):
        return self

    def cursor(self):
        return self

    def execute(self, *args, **kwargs):
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_pg(monkeypatch):

    def mock_pg_(columns, rows):
        mock_ = PgMock(columns, rows)
        monkeypatch.setattr('pg_analyse.toolbox.psycopg2', mock_)
        return mock_

    return mock_pg_
