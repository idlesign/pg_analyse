import json
from os import environ

from pg_analyse.settings import ENV_VAR
from pg_analyse.toolbox import analyse_and_format


def test_analyse_and_format(mock_pg):

    mock_pg(
        ['some_size', 'size'], [
            [123456789, 0],
        ])

    environ[ENV_VAR] = 'host=localhost user=postgres password=postgres'

    out = analyse_and_format()
    assert '123456789' in out

    out = analyse_and_format(fmt='json', human=True, only=['idx_unused', 'idx_bloat'])
    out = json.loads(out)

    assert out == [
        {'title': 'Bloating indexes', 'alias': 'idx_bloat',
         'arguments': {'schema_name_param': 'public', 'bloat_percentage_threshold': 50},
         'result': {'rows': [['117.74 MB', '0 B']], 'columns': ['some_size', 'size']}
         },
        {'title': 'Unused indexes', 'alias': 'idx_unused',
         'arguments': {'schema_name_param': 'public'},
         'result': {'rows': [['117.74 MB', '0 B']], 'columns': ['some_size', 'size']}}]
