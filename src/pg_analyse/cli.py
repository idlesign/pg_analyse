#!/usr/bin/env python
from functools import partial
from textwrap import wrap, indent

import click

from pg_analyse import VERSION_STR
from pg_analyse.formatters import Formatter
from pg_analyse.inspections.base import Inspection
from pg_analyse.toolbox import analyse_and_format, parse_args_string


@click.group()
@click.version_option(version=VERSION_STR)
def entry_point():
    """pg_analyse allows you to run various ."""


@entry_point.command()
@click.option('--dsn', help='DSN to connect to PG', default='')
@click.option(
    '--fmt',
    help='Format used for output',
    type=click.Choice(Formatter.formatters_all.keys()),
)
@click.option(
    '--one',
    help='Inspection name to limit runs',
    multiple=True
)
@click.option(
    '--human',
    help='Use human friendly values formatting (e.g. sizes)',
    is_flag=True
)
@click.option(
    '--args',
    help='Arguments to pass to inspections. E.g.: "idx_bloat:schema=my,bloat_min=20;idx_unused:schema=my"',
    default=''
)
def run(dsn, fmt, one, human, args):
    """Run analysis."""

    click.secho(analyse_and_format(
        dsn=dsn,
        fmt=fmt or '',
        only=one,
        human=human,
        arguments=parse_args_string(args)
    ))


@entry_point.command()
def inspections():
    """List known inspections."""

    for inspection in Inspection.inspections_all:
        click.secho(f'* {inspection.title} [{inspection.alias}]', fg='blue')

        shift = partial(indent, prefix='  ')

        click.secho(shift('\n'.join(wrap(f'{inspection.__doc__}'))))
        click.secho()

        click.secho(shift('Parameters:'))

        shift = partial(indent, prefix='    ')
        for key, val in inspection.params.items():
            click.secho(shift(f'{key}: {val}'))

        click.secho()


def main():
    entry_point(obj={})


if __name__ == '__main__':
    main()
