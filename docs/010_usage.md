# Usage

## Hint

One can set `PG_ANALYSE_DSN` environment variable instead of explicitly passing DSN
to connect to PostgreSQL. If [envbox](https://pypi.org/project/envbox/) is installed this
variable can be defined in `.env` file.

## Python module

```python
from pg_analyse.toolbox import Analyser, analyse_and_format

analyser = Analyser(dsn='user=test')

inspections = analyser.run()
inspection = inspections[0]

print(inspection.alias)
print(inspection.result)

# Shortcut function is available:
out = analyse_and_format()
```

## CLI

```shell
# Show known inspections and descriptions:
$ pg_analyse inspections

# Use DSN from the environment variable (see hint above),
# print out complex values (e.g. sizes) in human-friendly way:
$ pg_analyse run --human

# Run certain inspections, override default params.
# Use "common" keyword to pass params common for all inspections.
$ pg_analyse run --one idx_unused --one idx_bloat --args "idx_bloat:schema=my,bloat_min=20;common:schema=my"

# Use explicitly passed DSN:
$ pg_analyse run --dsn "host=myhost.net port=6432 user=test password=xxx sslmode=verify-full sslrootcert=/home/my.pem"
# Local connection as `postgres` user with password:
$ pg_analyse run --dsn "host=127.0.0.1 user=postgres password=yourpass"

# Output analysis result as json (instead of tables):
$ pg_analyse run --fmt json
```
