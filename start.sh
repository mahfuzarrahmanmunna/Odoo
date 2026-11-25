#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

exec ./venv/bin/python ./odoo/odoo-bin \
    -c ./config/odoo.conf \
    "$@"
