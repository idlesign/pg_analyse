from collections import namedtuple
from pathlib import Path
from typing import List, Type, Optional, Dict

from ..settings import DIR_SQL

InspectionResult = namedtuple('InspectionResult', ['columns', 'rows'])


class Inspection:
    """Base class for inspections."""

    title: str = ''
    """Human-friendly inspection title."""

    alias: str = ''
    """Inspection short alias to address it easily."""

    params: dict = {}
    """Parameters accepted by this inspection."""

    params_aliases: Dict[str, str] = {}
    """Param alias mapping name->sqlname."""

    sql_name: str = ''
    """SQL template file name."""

    sql_dir: Path = DIR_SQL
    """SQL template directory."""

    inspections_all: List[Type['Inspection']] = []

    def __init_subclass__(cls):
        super().__init_subclass__()

        if cls.alias:
            cls.inspections_all.append(cls)

    def __init__(self, **kwargs):

        self.title = self.title or self.alias

        self.sql_name = self.sql_name or self.alias

        self.arguments = {**self.params, **kwargs}

        self.result: Optional[InspectionResult] = None
        """Inspection run result. Populated runtime."""

    def _get_sql_dir(self) -> Path:
        """Returns SQL directory."""
        return self.sql_dir

    def _tpl_read(self) -> str:
        """Reads from filesystem SQL template and returns it."""
        with open(str(self._get_sql_dir() / f'{self.sql_name}.sql')) as f:
            return f.read()

    def get_sql(self) -> str:
        """Returns SQL ready to be executed."""

        out = self._tpl_read()
        aliases = self.params_aliases

        for name, value in self.arguments.items():
            name_sql = aliases.get(name, name)
            out = out.replace(f':{name_sql}', f"'{value}'")

        return out


class ContribInspection(Inspection):
    """Base class for contributed inspections."""

    sql_dir: Path = DIR_SQL / 'contrib'
