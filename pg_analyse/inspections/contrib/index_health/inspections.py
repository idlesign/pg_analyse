from pathlib import Path

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
        'schema_name_param': 'public',
        'bloat_percentage_threshold': 50,
    }


class IndexesDuplicated(_IndexHealthInspection):
    """Reveals duplicated/identical indexes."""

    title: str = 'Duplicated indexes'
    alias: str = 'idx_dub'
    sql_name: str = 'duplicated_indexes'

    params: dict = {
        'schema_name_param': 'public',
    }


class IndexesMissingForPk(_IndexHealthInspection):
    """Reveals foreign keys without indexes."""

    title: str = 'Foreign keys without indexes'
    alias: str = 'idx_fk'
    sql_name: str = 'foreign_keys_without_index'

    params: dict = {
        'schema_name_param': 'public',
    }


class IndexesWithNulls(_IndexHealthInspection):
    """Reveals indexes with NULL values."""

    title: str = 'Indexes with NULLs'
    alias: str = 'idx_nulls'
    sql_name: str = 'indexes_with_null_values'

    params: dict = {
        'schema_name_param': 'public',
    }


class IndexesWithIntersections(_IndexHealthInspection):
    """Reveals partially identical (intersected) indexes."""

    title: str = 'Intersecting indexes'
    alias: str = 'idx_intersect'
    sql_name: str = 'intersected_indexes'

    params: dict = {
        'schema_name_param': 'public',
    }


class IndexesInvalid(_IndexHealthInspection):
    """Reveals invalid/broken indexes."""

    title: str = 'Invalid indexes'
    alias: str = 'idx_invalid'
    sql_name: str = 'invalid_indexes'

    params: dict = {
        'schema_name_param': 'public',
    }


class IndexesUnused(_IndexHealthInspection):
    """Reveals unused indexes."""

    title: str = 'Unused indexes'
    alias: str = 'idx_unused'
    sql_name: str = 'unused_indexes'

    params: dict = {
        'schema_name_param': 'public',
    }


class TablesBloated(_IndexHealthInspection):
    """Reveals bloated tables."""

    title: str = 'Bloating tables'
    alias: str = 'tbl_bloat'
    sql_name: str = 'bloated_tables'

    params: dict = {
        'schema_name_param': 'public',
        'bloat_percentage_threshold': 50,
    }


class TablesMissingIndexes(_IndexHealthInspection):
    """Reveals tables with missing indexes."""

    title: str = 'Tables lacking indexes'
    alias: str = 'tbl_noindex'
    sql_name: str = 'tables_with_missing_indexes'

    params: dict = {
        'schema_name_param': 'public',
    }


class TablesMissingPk(_IndexHealthInspection):
    """Reveals tables missing primary keys."""

    title: str = 'Tables without Primary Key'
    alias: str = 'tbl_nopk'
    sql_name: str = 'tables_without_primary_key'

    params: dict = {
        'schema_name_param': 'public',
    }
