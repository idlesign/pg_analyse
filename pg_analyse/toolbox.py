from typing import List, Union, Set

import psycopg2

from .formatters import Formatter, TableFormatter
from .inspections import Inspection, InspectionResult
from .settings import ENV_VAR

try:  # pragma: nocover
    from envbox import get_environment
    environ = get_environment()

except ImportError:
    from os import environ


TypeOnly = Union[List[str], Set[str]]


class Analyser:
    """Performs the analysis running known inspections."""

    def __init__(self, *, dsn: str = ''):
        """

        :param dsn: DSN to connection to PostgreSQL.

        """
        if not dsn:
            dsn = environ.get(ENV_VAR, '')

        self.dsn = dsn

    def _sql_exec(self, *, connection, sql: str) -> InspectionResult:

        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [column.name for column in cursor.description]
            rows = cursor.fetchall()

        return InspectionResult(columns, rows)

    def run(self, *, only: TypeOnly = None) -> List[Inspection]:
        """Run analysis.

        :param only: Names of inspections we're interested in.
            If not set all inspections are run.

        """
        results = []
        only = set(only or [])

        with psycopg2.connect(self.dsn) as connection:

            for inspection_cls in Inspection.inspections_all:

                if not only or inspection_cls.alias in only:

                    inspection = inspection_cls()

                    inspection.result = self._sql_exec(
                        connection=connection,
                        sql=inspection.get_sql()
                    )

                    results.append(inspection)

        return results


def analyse_and_format(*, dsn: str = '', fmt: str = '', only: TypeOnly = None, human: bool = False) -> str:
    """Performs the analysis and returns results as a string.

    :param dsn: DSN to connection to PostgreSQL.

    :param fmt: Formatter alias to be used to format analysis results.

    :param only: Names of inspections we're interested in.
        If not set all inspections are run.

    :param human: Use human friendly values formatting (e.g. sizes).

    """
    analyser = Analyser(dsn=dsn)
    inspections = analyser.run(only=only)

    fmt = fmt or TableFormatter.alias
    formatter_cls = Formatter.formatters_all[fmt]

    out = []

    for inspection in inspections:
        out.append(formatter_cls(inspection, human=human).run())

    return formatter_cls.wrap(out)
