#!/usr/bin/env python3
"""
Master validator: simply calls both macro validators for the entire database.
1. Runs validate_translations.py (global translation/JSON/structure validation)
2. Runs validate_structure_bulk.py for each English base file (study-level structure validation)
No additional logic or per-file handling.
"""


import subprocess
import sys
import os
import glob

print("==============================")
print("GLOBAL TRANSLATION/JSON VALIDATION")
print("==============================")

# Run the global translation/JSON validator
result = subprocess.run([
    sys.executable, "validate_translations.py"
], cwd="./discovery/bible_studies_scripts", capture_output=True, text=True)
print(result.stdout)
if result.returncode != 0:
    print("\n❌ Errors found in translation/JSON validation.")
    sys.exit(result.returncode)

print("==============================")
print("BULK STRUCTURE VALIDATION FOR ALL STUDIES")
print("==============================")

# Find all English base files for studies
en_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../en'))
base_files = glob.glob(os.path.join(en_dir, '*_en_*.json'))

for base_file in base_files:
    print(f"\n--- Structure validation for study: {os.path.basename(base_file)} ---")
    result2 = subprocess.run([
        sys.executable, "validate_structure_bulk.py", base_file
    ], cwd="./discovery/bible_studies_scripts", capture_output=True, text=True)
    print(result2.stdout)
    if result2.returncode != 0:
        print(f"\n❌ Structure errors found for {os.path.basename(base_file)}.")
        sys.exit(result2.returncode)

print("\n✅ All studies passed bulk structure validation.\n")
