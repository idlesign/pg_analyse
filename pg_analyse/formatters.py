import json
import math
from typing import Type, Dict, List

if False:  # pragma: nocover
    from .toolbox import Inspection


class Formatter:
    """Base inspection result formatter."""

    alias: str = ''
    """Short distinctive name for this formatter."""

    formatters_all: Dict[str, Type['Formatter']] = {}
    """Registry of all known formatters."""

    def __init__(self, inspection: 'Inspection', *, human: bool = False):
        """

        :param inspection:
        :param human: Use human friendly values formatting (e.g. sizes).

        """
        self.inspection = inspection
        self.human = human

    def __init_subclass__(cls):
        super().__init_subclass__()

        alias = cls.alias

        if alias:
            cls.formatters_all[alias] = cls

    @staticmethod
    def humanize_size(bytes_size: int) -> str:
        """Returns human readable size.

        :param bytes_size:

        """
        if not bytes_size:
            return '0 B'

        names = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')

        name_idx = int(math.floor(math.log(bytes_size, 1024)))
        size = round(bytes_size / math.pow(1024, name_idx), 2)

        return '%s %s' % (size, names[name_idx])

    def _get_rows_processed(self):

        column_casters = []
        human = self.human

        for name in self.inspection.result.columns:
            func = lambda value: value

            if human and 'size' in name:
                func = self.humanize_size

            column_casters.append(func)

        out = []

        for row in self.inspection.result.rows:
            out.append([column_casters[idx](chunk) for idx, chunk in enumerate(row)])

        return out

    def run(self) -> str:  # pragma: nocover
        """Must format data from self.inspection into a string."""
        raise NotImplementedError

    @classmethod
    def wrap(cls, lines: List[str]) -> str:  # pragma: nocover
        """Must wrap a list into a single string.

        :param lines: Multiple results from self.run.

        """
        raise NotImplementedError


class TableFormatter(Formatter):
    """Format inspection result as table."""

    alias: str = 'table'

    def run(self) -> str:
        from tabulate import tabulate

        inspection = self.inspection

        columns = [
            column.replace('_', ' ').capitalize()
            for column in inspection.result.columns]

        line = (
            f'{inspection.title} [{inspection.alias}]\n\n'
            f'{tabulate(self._get_rows_processed(), headers=columns)}'
        )

        return line

    @classmethod
    def wrap(cls, lines: List[str]) -> str:
        return '\n\n\n'.join(lines)


class JsonFormatter(Formatter):
    """Format inspection result as JSON."""

    alias: str = 'json'

    def run(self) -> str:
        inspection = self.inspection

        line = {
            'title': inspection.title,
            'alias': inspection.alias,
            'arguments': inspection.arguments,
            'result': {
                'rows': self._get_rows_processed(),
                'columns': inspection.result.columns,
            },
        }

        return json.dumps(line)

    @classmethod
    def wrap(cls, lines: List[str]) -> str:
        return f"[{','.join(lines)}]"
