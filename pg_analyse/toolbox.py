from typing import List, Union, Set, Dict

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
TypeInspectionsArgs = Dict[str, Dict[str, str]]


class Analyser:
    """Performs the analysis running known inspections."""

    def __init__(self, *, dsn: str = ''):
        """

        :param dsn: DSN to connection to PostgreSQL.

        """
        if not dsn:
            dsn = environ.get(ENV_VAR, '')

        self.dsn = dsn

    def _sql_exec(self, *, connection, sql: str, params: dict) -> InspectionResult:

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [column.name for column in cursor.description]
            rows = cursor.fetchall()

        return InspectionResult(columns, rows)

    def run(self, *, only: TypeOnly = None, arguments: TypeInspectionsArgs = None) -> List[Inspection]:
        """Run analysis.

        :param only: Names of inspections we're interested in.
            If not set all inspections are run.

        :param arguments: Arguments to pass to inspections.

            Example: {'insp_alias': {'param1': 'value', 'param2': 'value'}}

        """
        results = []
        only = set(only or [])
        arguments = arguments or {}

        with psycopg2.connect(self.dsn) as connection:

            for inspection_cls in Inspection.inspections_all:

                alias = inspection_cls.alias

                if not only or alias in only:

                    inspection = inspection_cls(args=arguments.get(alias))

                    try:

                        inspection.result = self._sql_exec(
                            connection=connection,
                            sql=inspection.get_sql(),
                            params=inspection.arguments,
                        )

                    except Exception as e:
                        inspection.errors.append(f'{e}')

                    results.append(inspection)

        return results


def analyse_and_format(
        *,
        dsn: str = '',
        fmt: str = '',
        only: TypeOnly = None,
        human: bool = False,
        arguments: TypeInspectionsArgs = None
) -> str:
    """Performs the analysis and returns results as a string.

    :param dsn: DSN to connection to PostgreSQL.

    :param fmt: Formatter alias to be used to format analysis results.

    :param only: Names of inspections we're interested in.
        If not set all inspections are run.

    :param human: Use human friendly values formatting (e.g. sizes).

    :param arguments: Arguments to pass to inspections.

        Example: {'insp_alias': {'param1': 'value', 'param2': 'value'}}

    """
    analyser = Analyser(dsn=dsn)
    inspections = analyser.run(only=only, arguments=arguments)

    fmt = fmt or TableFormatter.alias
    formatter_cls = Formatter.formatters_all[fmt]

    out = []

    for inspection in inspections:
        out.append(formatter_cls(inspection, human=human).run())

    return formatter_cls.wrap(out)


def parse_args_string(val: str) -> TypeInspectionsArgs:
    """Parses inspections args string into a dict.

    :param val: E.g.: idx_bloat:schema=my,bloat_min=20;idx_unused:schema=my

    """
    out = {}

    for chunk in val.split(';'):
        args = {}

        alias, _, argstr = chunk.strip().partition(':')
        argstr = argstr.strip()

        for arg in argstr.split(','):
            name, _, val = arg.partition('=')
            val = val.strip()

            if val:
                args[name.strip()] = val

        if args:
            out[alias.strip()] = args

    return out
