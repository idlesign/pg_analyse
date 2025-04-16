#! /bin/sh
# Updates already initialized contrib Git submodules
git submodule update --remote --merge
git add pg_analyse/sql/contrib/index_health/
