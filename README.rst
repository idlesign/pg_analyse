pg_analyse
==========
https://github.com/idlesign/pg_analyse

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/pg_analyse.svg
    :target: https://pypi.python.org/pypi/pg_analyse

.. |lic| image:: https://img.shields.io/pypi/l/pg_analyse.svg
    :target: https://pypi.python.org/pypi/pg_analyse

.. |ci| image:: https://img.shields.io/travis/idlesign/pg_analyse/master.svg
    :target: https://travis-ci.org/idlesign/pg_analyse

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/pg_analyse/master.svg
    :target: https://coveralls.io/r/idlesign/pg_analyse


.. image:: https://github.com/idlesign/pg_analyse/blob/master/pg_analyse_cli.gif


Description
-----------

*Tools to gather useful information from PostgreSQL*

This package can function both as Python module and as a command line utility.
Command line interface can show gathered information in the form of tables or ``JSON``.

Use it to gather information manually or in Continuous Integration.

Can give you some information on:

* Index health (bloat, duplicates, unused, etc.);
* Tables missing PKs and indexes;
* Slowest queries.


.. note:: SQLs used for inspections are available in https://github.com/mfvanek/pg-index-health-sql


Requirements
------------

* Python 3.6+
* psycopg 2


Installation
------------

.. code-block:: bash

    ; If you do not have psycopg2 yet, install it as `psycopg2` or `psycopg2-binary`. 
    ; You may also want to install `envbox` to get PG connection settings from .env files.
    ; Your distribution may require issuing `pip3` command instead of plain `pip`.
    $ pip install psycopg2-binary envbox

    ; If you want to use it just as Python module:
    $ pip install pg_analyse

    ; If you want to use it from command line:
    $ pip install pg_analyse[cli]


Usage
-----

Hint
~~~~

One can set ``PG_ANALYSE_DSN`` environment variable instead of explicitly passing DSN
to connect to PostgreSQL. If `envbox <https://pypi.org/project/envbox/>`_ is installed this
variable can be defined in ``.env`` file .

Python module
~~~~~~~~~~~~~


.. code-block:: python

    from pg_analyse.toolbox import Analyser, analyse_and_format

    analyser = Analyser(dsn='user=test')

    inspections = analyser.run()
    inspection = inspections[0]

    print(inspection.alias)
    print(inspection.result)

    # Shortcut function is available:
    out = analyse_and_format()


CLI
~~~

.. code-block:: bash

    ; Show known inspections and descriptions:
    $ pg_analyse inspections

    ; Use DSN from the environment variable (see hint above),
    ; print out complex values (e.g. sizes) in human-friendly way:
    $ pg_analyse run --human

    ; Run certain inspections, override default params
    $ pg_analyse run --one idx_unused --one idx_bloat --args "idx_bloat:schema=my,bloat_min=20;idx_unused:schema=my"

    ; Use explicitly passed DSN:
    $ pg_analyse run --dsn "host=myhost.net port=6432 user=test password=xxx sslmode=verify-full sslrootcert=/home/my.pem"
    ; Local connection as `postgres` user with password:
    $ pg_analyse run --dsn "host=127.0.0.1 user=postgres password=yourpass"

    ; Output analysis result as json (instead of tables):
    $ pg_analyse run --fmt json


Adding Inspections
------------------

To add a new inspection to ``pg_analyse``:

1. Compose SQL for inspection and put it into a file under ``sql/`` directory.
2. Add a subclass of ``Inspection`` into ``inspections/bundled.py``. Fill in ``alias``, ``sql_name`` attributes (see docstrings in ``Inspection``).
