# Discovery Studies Validation Scripts

This folder contains validation tools for the discovery studies translation files.

## validate_translations.py

Comprehensive **two-phase validation script** that ensures quality and consistency across all translation files.

### Two-Phase Validation Approach

**PHASE A: Index Validation**
- Validates index.json format, structure, and data integrity
- Checks for missing translations and marks them as PENDING
- If Phase A fails, validation stops and errors are reported
- index.json becomes the single source of truth for Phase B

**PHASE B: Translation Files Validation** 
- Only runs if Phase A passes
- Uses index.json as the authoritative source of studies
- Validates all translation files referenced in index.json
- Verifies file existence, structure, and content quality

### Features

1. **Index.json Validation (Phase A)**
   - Validates JSON format and syntax
   - Checks required fields: id, version, emoji, files, titles, subtitles, estimated_reading_minutes
   - Verifies data structure integrity
   - Detects studies with incomplete translations
   - Reports PENDING translations by language

2. **JSON Format Validation (Phase B)**
   - Validates that all files are proper JSON
   - Checks for syntax errors

3. **Language Consistency**
   - Verifies correct language codes (en, es, pt, fr, ja, zh)
   - Ensures proper Bible version for each language
   - Detects mixed languages in content

4. **Structural Validation**
   - Confirms all required fields are present
   - Validates array structures (cards, tags, themes)
   - Checks metadata completeness

5. **Translation Accuracy**
   - Compares card counts across translations
   - Verifies tag counts match
   - Ensures theme counts are consistent
   - Validates that non-English files don't contain English content

6. **File Reference Validation**
   - Verifies all files listed in index.json actually exist
   - Checks filename format consistency
   - Ensures language directory structure is correct

### Usage

```bash
# From the discovery folder
python3 scripts/validate_translations.py

# Make it executable (optional)
chmod +x scripts/validate_translations.py
./scripts/validate_translations.py
```

### Expected Output

The script will display:
- **Phase A Report**: Index validation results
- **Phase B Report**: Translation files validation (only if Phase A passes)
- Statistics (total files, languages, studies, pending translations)
- Information messages
- Warnings (non-critical issues)
- Errors (must be fixed)

Exit code:
- `0` = All validations passed
- `1` = Errors found (stops at first phase with errors)

### Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

### Validation Rules

**Expected Languages:**
- English (en) - KJV, NIV
- Spanish (es) - RVR1960, NVI
- Portuguese (pt) - ARC, NVI
- French (fr) - LSG1910, TOB
- Japanese (ja) - 新改訳2003, リビングバイブル
- Chinese (zh) - 和合本1919, 新译本

**Studies:** Defined in index.json (single source of truth)

**File Naming Convention:**
- Format: `{study_name}_{language}_001.json`
- Example: `born_again_en_001.json`

### Automated Checks

**Phase A (Index):**
- ✅ index.json exists and is valid JSON
- ✅ Required fields present in each study entry
- ✅ No duplicate study IDs
- ✅ Files object has valid language codes
- ✅ Titles and subtitles match file languages
- ✅ Detection of incomplete translations (PENDING status)

**Phase B (Translation Files):**
- ✅ Valid JSON syntax in all files
- ✅ Correct language codes
- ✅ Correct Bible versions
- ✅ Matching structure across translations
- ✅ No English content in non-English files (for ja/zh)
- ✅ All files referenced in index.json exist

### Adding New Translations

When adding a new study or language:
1. Update index.json with the new study entry
2. Ensure all required fields are present
3. Add translation files to appropriate language folders
4. Run validation - it will automatically use index.json as source of truth
5. Fix any PENDING translations as needed

### Understanding PENDING Status

Studies with incomplete translations are reported as PENDING in Phase A:
- Shows which languages are missing for each study
- Helps track translation progress
- Does not cause validation failure (only a warning)
