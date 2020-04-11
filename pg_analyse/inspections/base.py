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

    def __init__(self, *, args: Dict[str, str] = None):

        self.title = self.title or self.alias

        self.sql_name = self.sql_name or self.alias

        self.arguments = {**self.params, **(args or {})}
        """User supplied arguments to replace defaults."""

        self.errors: List[str] = []
        """Inspection errors description."""

        self.result: Optional[InspectionResult] = None
        """Inspection run result. Populated runtime."""

    def _get_sql_dir(self) -> Path:
        """Returns SQL directory."""
        return self.sql_dir

    def get_sql_path(self) -> str:
        """Returns executed SQL path."""
        return str(self._get_sql_dir() / f'{self.sql_name}.sql')

    def _tpl_read(self) -> str:
        """Reads from filesystem SQL template and returns it."""
        with open(self.get_sql_path()) as f:
            return f.read()

    def get_sql(self) -> str:
        """Returns SQL ready to be executed."""

        # Here we replace ":var"-like param placeholders
        # with "%(var)s"-like acceptable for psycopg2,
        # escaping % with %%.

        out = self._tpl_read().replace('%', '%%')
        aliases = self.params_aliases

        for name, value in self.arguments.items():
            name_sql = aliases.get(name, name)
            out = out.replace(f':{name_sql}', f'%({name})s')

        return out


class ContribInspection(Inspection):
    """Base class for contributed inspections."""

    sql_dir: Path = DIR_SQL / 'contrib'
