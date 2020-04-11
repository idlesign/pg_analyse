from collections import namedtuple

import pytest


class PgMock:

    def __init__(self, columns, rows, *, exception=None):
        self.columns = columns
        self.rows = rows
        self.exception = exception

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
        exception = self.exception
        if exception:
            raise ValueError(exception)
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_pg(monkeypatch):

    def mock_pg_(columns, rows, *, exception=None):
        mock_ = PgMock(columns, rows, exception=exception)
        monkeypatch.setattr('pg_analyse.toolbox.psycopg2', mock_)
        return mock_

    return mock_pg_
