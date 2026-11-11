# pg_analyse

<https://github.com/idlesign/pg_analyse>

*Tools to gather useful information from PostgreSQL*

This package can function both as Python module and as a command line utility.
Command line interface can show gathered information in the form of tables or `JSON`.

Can give you some information on:

* Index health (bloat, duplicates, unused, etc.);
* Tables missing PKs and indexes;
* Slowest queries.

## Requirements

1. Python 3.10+
2. psycopg 3

## Install

```shell
$ python -m pip install pg_analyse
```

See [Usage](010_usage.md) for the details.
