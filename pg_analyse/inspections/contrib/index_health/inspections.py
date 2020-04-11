from pathlib import Path
from typing import Dict

from ...base import ContribInspection


class _IndexHealthInspection(ContribInspection):
    """Base check for Index Health contrib.

    https://github.com/mfvanek/pg-index-health-sql

    """
    sql_dir: Path = ContribInspection.sql_dir / 'index_health' / 'sql'


class IndexesBloated(_IndexHealthInspection):
    """Reveals bloated indexes."""

    title: str = 'Bloating indexes'
    alias: str = 'idx_bloat'
    sql_name: str = 'bloated_indexes'

    params: dict = {
        'schema': 'public',
        'bloat_min': 50,
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
        'bloat_min': 'bloat_percentage_threshold',
    }


class IndexesDuplicated(_IndexHealthInspection):
    """Reveals duplicated/identical indexes."""

    title: str = 'Duplicated indexes'
    alias: str = 'idx_dub'
    sql_name: str = 'duplicated_indexes'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class IndexesMissingForPk(_IndexHealthInspection):
    """Reveals foreign keys without indexes."""

    title: str = 'Foreign keys without indexes'
    alias: str = 'idx_fk'
    sql_name: str = 'foreign_keys_without_index'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class IndexesWithNulls(_IndexHealthInspection):
    """Reveals indexes with NULL values."""

    title: str = 'Indexes with NULLs'
    alias: str = 'idx_nulls'
    sql_name: str = 'indexes_with_null_values'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class IndexesWithIntersections(_IndexHealthInspection):
    """Reveals partially identical (intersected) indexes."""

    title: str = 'Intersecting indexes'
    alias: str = 'idx_intersect'
    sql_name: str = 'intersected_indexes'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class IndexesInvalid(_IndexHealthInspection):
    """Reveals invalid/broken indexes."""

    title: str = 'Invalid indexes'
    alias: str = 'idx_invalid'
    sql_name: str = 'invalid_indexes'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class IndexesUnused(_IndexHealthInspection):
    """Reveals unused indexes."""

    title: str = 'Unused indexes'
    alias: str = 'idx_unused'
    sql_name: str = 'unused_indexes'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class TablesBloated(_IndexHealthInspection):
    """Reveals bloated tables."""

    title: str = 'Bloating tables'
    alias: str = 'tbl_bloat'
    sql_name: str = 'bloated_tables'

    params: dict = {
        'schema': 'public',
        'bloat_min': 50,
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
        'bloat_min': 'bloat_percentage_threshold',
    }


class TablesMissingIndexes(_IndexHealthInspection):
    """Reveals tables with missing indexes."""

    title: str = 'Tables lacking indexes'
    alias: str = 'tbl_noindex'
    sql_name: str = 'tables_with_missing_indexes'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class TablesMissingPk(_IndexHealthInspection):
    """Reveals tables missing primary keys."""

    title: str = 'Tables without Primary Key'
    alias: str = 'tbl_nopk'
    sql_name: str = 'tables_without_primary_key'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class QueriesSlowest(_IndexHealthInspection):
    """Reveals slowest queries. Requires the pg_stat_statement extension"""

    title: str = 'Slowest queries'
    alias: str = 'q_slowest'

    sql_dir: Path = _IndexHealthInspection.sql_dir / 'ext'
    sql_name: str = 'slowest_queries_by_total_execution_time'

    params: dict = {
        'count': 10,
    }

    params_aliases: Dict[str, str] = {
        'count': 'limit_count',
    }
