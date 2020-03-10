pg_analyse
==========
https://github.com/idlesign/pg_analyse

|release| |lic|

.. |release| image:: https://img.shields.io/pypi/v/pg_analyse.svg
    :target: https://pypi.python.org/pypi/pg_analyse

.. |lic| image:: https://img.shields.io/pypi/l/pg_analyse.svg
    :target: https://pypi.python.org/pypi/pg_analyse


Description
-----------

*Tools to gather useful information from PostgreSQL*

This package can function both as Python module and as a command line utility.
Command line interface can show gathered information in the form of tables or ``JSON``.

Use it to gather information manually or in Continuous Integration.

Can give you some information on:

* Index health (bloat, duplicates, unused, etc.);
* Tables missing PKs and indexes.


Requirements
------------

* Python 3.6+


Installation
------------

.. code-block:: bash

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

    from pg_analyse.toolbox import Analyser

    analyser = Analyser(dsn='user=test')

    inspections = analyser.run()
    inspection = inspections[0]

    print(inspection.alias)
    print(inspection.result)


CLI
~~~

.. code-block:: bash

    ; Show known inspections and descriptions:
    $ pg_analyse inspections

    ; Use DSN from the environment variable (see hint above),
    ; print out human values (e.g. sizes) in human-friendly way:
    $ pg_analyse run --human

    ; Run certain inspections:
    $ pg_analyse run --one idx_unused --one idx_nulls

    ; Use explicitly passed DSN:
    $ pg_analyse run --dsn "host=myhost.net port=6432 user=test password=xxx sslmode=verify-full sslrootcert=/home/my.pem"

    ; Output analysis result as json (instead of tables):
    $ pg_analyse run --fmt json


Adding Inspection
-----------------

To add a new inspection to ``pg_analyse``:

1. Compose SQL for inspection and put it into a file under ``sql/`` directory.
2. Add a subclass of ``Inspection`` into ``inspections/bundled.py``.
  Fill in ``alias``, ``sql_name`` attributes (see docstrings in ``Inspection``).