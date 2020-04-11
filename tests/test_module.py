import json
from os import environ

from pg_analyse.settings import ENV_VAR
from pg_analyse.toolbox import analyse_and_format, parse_args_string


def test_parse_args():

    assert parse_args_string('idx_bloat :schema=my, bloat_min=20 ; idx_unused:schema =my') == {
        'idx_bloat': {
            'schema': 'my',
            'bloat_min': '20',
        },
        'idx_unused': {
            'schema': 'my',
        },
    }

    assert parse_args_string('xxxx:') == {}


def test_analyse_and_format(mock_pg):

    mock_pg(
        ['some_size', 'size'], [
            [123456789, 0],
        ])

    environ[ENV_VAR] = 'host=localhost user=postgres password=postgres'

    out = analyse_and_format()
    assert '123456789' in out

    out = analyse_and_format(
        fmt='json',
        human=True,
        only=['idx_unused', 'idx_bloat'],
        arguments={'idx_bloat': {'bloat_min': '70'}}
    )
    out = json.loads(out)

    assert out == [
        {'title': 'Bloating indexes', 'alias': 'idx_bloat',
         'arguments': {'schema': 'public', 'bloat_min': '70'}, 'errors': [],
         'result': {'rows': [['117.74 MB', '0 B']], 'columns': ['some_size', 'size']}
         },
        {'title': 'Unused indexes', 'alias': 'idx_unused',
         'arguments': {'schema': 'public'}, 'errors': [],
         'result': {'rows': [['117.74 MB', '0 B']], 'columns': ['some_size', 'size']}}]


def test_exceptions(mock_pg):

    mock_pg([], [], exception='bang!')

    environ[ENV_VAR] = 'host=localhost user=postgres password=postgres'

    out = analyse_and_format()
    assert 'bang!' in out

    out = analyse_and_format(fmt='json', only=['idx_unused'],)
    out = json.loads(out)
    assert out == [{
        'title': 'Unused indexes', 'alias': 'idx_unused',
        'arguments': {'schema': 'public'},
        'errors': ['bang!'], 'result': {'rows': [], 'columns': []}}]

