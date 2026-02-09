#!/usr/bin/env python3
"""
Master validator for phased validation of discovery study files.

PHASE 1: Validate the base file using the single-file validator (validate_translations.py).
- If errors are found, report and exit.
- If successful, proceed to phase 2.

PHASE 2: Run the bulk structure validator (validate_structure_bulk.py) for all related files.
"""

import sys
import subprocess
import os

if len(sys.argv) < 2:
    print("Usage: python master_validator.py <base_file.json>")
    sys.exit(1)

# Get absolute path to base file
base_file = os.path.abspath(sys.argv[1])

print("==============================")
print("PHASE 1: Single File Validation")
print("==============================")

# Run the single-file validator (validate_translations.py)
result = subprocess.run([
    sys.executable, "validate_translations.py", base_file
], cwd="./discovery/bible_studies_scripts", capture_output=True, text=True)

print(result.stdout)
if result.returncode != 0:
    print("\n❌ Errors found in base file. Fix these before continuing.")
    sys.exit(result.returncode)
else:
    print("\n✅ Base file passed single-file validation. Proceeding to bulk structure validation.\n")

print("==============================")
print("PHASE 2: Bulk Structure Validation")
print("==============================")

# Run the bulk structure validator (validate_structure_bulk.py)
result2 = subprocess.run([
    sys.executable, "validate_structure_bulk.py", base_file
], cwd="./discovery/bible_studies_scripts", capture_output=True, text=True)

print(result2.stdout)
if result2.returncode != 0:
    print("\n❌ Errors found in bulk structure validation.")
    sys.exit(result2.returncode)
else:
    print("\n✅ All files passed bulk structure validation.\n")
