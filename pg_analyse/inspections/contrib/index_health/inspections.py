from pathlib import Path
from typing import Dict

from ...base import ContribInspection


class _IndexHealthInspection(ContribInspection):
    """Base check for Index Health contrib.

    https://github.com/mfvanek/pg-index-health-sql

    """
    sql_dir: Path = ContribInspection.sql_dir / 'index_health' / 'sql'


class SeqOverflow(_IndexHealthInspection):
    """Reveals sequences exhaustion."""

    title: str = 'Sequences exhaustion'
    alias: str = 'seq_exh'
    sql_name: str = 'sequence_overflow'

    params: dict = {
        'schema': 'public',
        'left_min': 20,
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
        'left_min': 'remaining_percentage_threshold',
    }


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


class IndexesMissingForFk(_IndexHealthInspection):
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


class IndexesBtreeArray(_IndexHealthInspection):
    """Reveal B-Tree indexes on array columns."""

    title: str = 'B-Tree indexes on array columns'
    alias: str = 'idx_btree_arr'
    sql_name: str = 'btree_indexes_on_array_columns'

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


class IndexesBoolean(_IndexHealthInspection):
    """Reveals indexes on boolean."""

    title: str = 'Indexes on Boolean'
    alias: str = 'idx_bool'
    sql_name: str = 'indexes_with_boolean'

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


class ConstraintsInvalid(_IndexHealthInspection):
    """Reveal not valid constraints."""

    title: str = 'Not valid constraints'
    alias: str = 'constr_invalid'
    sql_name: str = 'not_valid_constraints'

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


class ColumnsJson(_IndexHealthInspection):
    """Reveals columns using JSON type (jsonb advised)."""

    title: str = 'Columns using JSON type'
    alias: str = 'col_json'
    sql_name: str = 'columns_with_json_type'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class ColumnsSerialPrimary(_IndexHealthInspection):
    """Reveals columns using serial types but non-primary or primary+foreign."""

    title: str = 'Serial types in relation to primary key'
    alias: str = 'col_serial'
    sql_name: str = 'columns_with_serial_types'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class ColumnsUnconventionalNames(_IndexHealthInspection):
    """Reveals columns that have to be enclosed in double-quotes due
    to not following naming conventions."""

    title: str = 'Columns with unconventional names'
    alias: str = 'col_unconv'
    sql_name: str = 'columns_not_following_naming_convention'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class FkDuplicated(_IndexHealthInspection):
    """Reveals duplicated foreign keys."""

    title: str = 'FK duplicated'
    alias: str = 'fk_dub'
    sql_name: str = 'duplicated_foreign_keys'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class FkUnmatchedType(_IndexHealthInspection):
    """Reveals foreign keys with the constrained column type not matching
    the type in the referenced table."""

    title: str = 'FK unmatched types'
    alias: str = 'fk_typematch'
    sql_name: str = 'foreign_keys_with_unmatched_column_type'

    params: dict = {
        'schema': 'public',
    }

    params_aliases: Dict[str, str] = {
        'schema': 'schema_name_param',
    }


class FkIntersecting(_IndexHealthInspection):
    """Reveals foreign keys with overlapping sets of columns."""

    title: str = 'FK intersected'
    alias: str = 'fk_isect'
    sql_name: str = 'intersected_foreign_keys'

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
