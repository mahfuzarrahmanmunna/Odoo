#!/usr/bin/env python3

import os
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "odoo"

sys.path.insert(0, str(SOURCE))

os.environ["PATH"] = (
    "/usr/local/bin:"
    + os.environ.get("PATH", "")
)

import odoo
import odoo.addons
import odoo.modules.module as module

assert odoo.release.version_info[0] == 17
assert Path(odoo.__file__).resolve().is_relative_to(SOURCE)

ALLOWED = [
    str(SOURCE / "odoo" / "addons"),
    str(SOURCE / "addons"),
    str(PROJECT / "custom-addons"),
    str(PROJECT / "custom-addons" / "odoomates"),
    str(PROJECT / "data" / "addons" / "17.0"),
]

ALLOWED = [p for p in ALLOWED if os.path.isdir(p)]

original_initialize = module.initialize_sys_path

def isolate_addons():
    odoo.addons.__path__ = list(ALLOWED)
    original_initialize()
    odoo.addons.__path__ = list(ALLOWED)

module.initialize_sys_path = isolate_addons
odoo.addons.__path__ = list(ALLOWED)

print("=" * 65, flush=True)
print("RETAIL PROJECTS - ISOLATED ODOO 17", flush=True)
print("Odoo Version:", odoo.release.version, flush=True)
print("Python:", sys.executable, flush=True)
print("Core:", odoo.__file__, flush=True)

for path in ALLOWED:
    print("Allowed Addons:", path, flush=True)

print("=" * 65, flush=True)

import odoo.cli
odoo.cli.main()
