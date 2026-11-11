from pathlib import Path


DIR_SQL = Path(__file__).parent.absolute() / 'sql'
"""Base directory holding SQL templates."""

ENV_VAR = 'PG_ANALYSE_DSN'
"""Name of environment variable to search PostgreSQL DSN in."""
