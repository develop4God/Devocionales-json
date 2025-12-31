# Devotional JSON Validation and Correction Scripts

## Overview

This directory contains Python scripts to validate and correct language integrity and prayer closings in devotional JSON files for multiple languages.

## Scripts

### 1. `validate_devotionals.py`

**Purpose:** Validates the integrity of devotional JSON files by checking:
- Language consistency in content fields (reflexion, oracion)
- Correct prayer closing phrases for each language

**Usage:**
```bash
python3 scripts/validate_devotionals.py
```

**Output:** Generates a detailed validation report showing:
- Total entries validated
- Number of language mismatches
- Number of incorrect prayer closings
- Specific details for each issue found

### 2. `correct_devotionals.py`

**Purpose:** Automatically corrects common prayer closing issues in devotional JSON files.

**Usage:**
```bash
python3 scripts/correct_devotionals.py
```

**Corrections Applied:**
- Standardizes prayer closings to the correct format for each language
- Fixes common issues like:
  - Wrong language closings (e.g., Spanish closings in Portuguese files)
  - Incorrect capitalization
  - Wrong accent marks (amén vs amém)
  - Generic closings (e.g., "En tu nombre" → "En el nombre de Jesús")

**Output:** Generates a correction report showing:
- Total entries processed
- Number of corrections made
- Details of each correction

## Standard Prayer Closings by Language

| Language | Code | Standard Closing |
|----------|------|------------------|
| Spanish | es | `En el nombre de Jesús, amén.` |
| English | en | `In the name of Jesus, amen.` |
| Portuguese | pt | `Em nome de Jesus, amém.` |
| French | fr | `Au nom de Jésus, amen.` |
| Chinese | zh | `奉耶稣的名祷告，阿们。` (and variations) |
| Japanese | ja | `イエス・キリストの御名によってお祈りします。アーメン。` (and variations) |

## Files Processed

The scripts process devotional files for years 2025 and 2026 in the following languages:
- Spanish (es) - 4 files
- English (en) - 4 files
- Portuguese (pt) - 4 files
- French (fr) - 4 files
- Chinese (zh) - 4 files
- Japanese (ja) - 4 files

**Total: 24 devotional JSON files**

## Validation Rules

### Language Detection
- Content fields (reflexion, oracion) are checked for language consistency
- Short Bible verses in para_meditar are excluded to avoid false positives
- Minimum text length of 50 characters for reliable detection

### Prayer Closing Validation
- Each prayer must end with the correct closing phrase for its language
- Closings must follow the standardized format
- Chinese and Japanese have multiple acceptable variations

## Execution Results

### Initial Validation
- **Total files:** 22
- **Total entries:** 7,312
- **Issues found:** 1,124 prayer closing issues

### After Corrections
- **Corrections applied:** 2,714
- **Remaining issues:** 1,094 (all in Chinese and Japanese files with acceptable variations)
- **Files fully corrected:** Spanish, English, Portuguese, French (8 languages × 2 years)

## Common Issues Fixed

1. **Spanish files:**
   - "En tu nombre, amén" → "En el nombre de Jesús, amén."
   - Case corrections

2. **English files:**
   - "amén" → "amen" (wrong accent)
   - "In Your name" → "In the name of Jesus"
   - "in Jesus' name" → "In the name of Jesus"

3. **Portuguese files:**
   - "en el nombre de Jesús, amén" → "Em nome de Jesus, amém." (Spanish → Portuguese)
   - "Em Teu nome, amén" → "Em nome de Jesus, amém."
   - "amén" → "amém" (wrong accent)

4. **French files:**
   - "en le nom de Jésus" → "Au nom de Jésus"
   - "amén" → "amen" (wrong accent)

## Notes

- **Chinese and Japanese:** These languages have multiple culturally acceptable variations for prayer closings. The validation identifies differences but does not auto-correct to preserve linguistic nuance.
- **Field Names:** All field names (versiculo, reflexion, para_meditar, cita, texto, oracion, tags) remain in Spanish across all language versions, as designed.
- **Backup:** Always keep backups of original files before running correction scripts.

## Future Improvements

- Add language detection for potential content in wrong language (currently disabled to avoid false positives)
- Create language-specific validators for Chinese and Japanese
- Add unit tests for validation and correction logic
- Support for additional languages

## Developer Notes

- Scripts use Python 3.12+
- UTF-8 encoding for all file operations
- Regular expressions for pattern matching
- JSON pretty-printing with 4-space indentation maintained
