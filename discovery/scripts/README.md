# Discovery Studies Validation Scripts

This folder contains validation tools for the discovery studies translation files.

## validate_translations.py

Comprehensive validation script that ensures quality and consistency across all translation files.

### Features

1. **JSON Format Validation**
   - Validates that all files are proper JSON
   - Checks for syntax errors

2. **Language Consistency**
   - Verifies correct language codes (en, es, pt, fr, ja, zh)
   - Ensures proper Bible version for each language
   - Detects mixed languages in content

3. **Structural Validation**
   - Confirms all required fields are present
   - Validates array structures (cards, tags, themes)
   - Checks metadata completeness

4. **Translation Accuracy**
   - Compares card counts across translations
   - Verifies tag counts match
   - Ensures theme counts are consistent
   - Validates that non-English files don't contain English content

5. **Index File Validation**
   - Checks that all studies are listed
   - Verifies all language files are referenced
   - Ensures completeness

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
- Statistics (total files, languages, studies)
- Information messages
- Warnings (non-critical issues)
- Errors (must be fixed)

Exit code:
- `0` = All validations passed
- `1` = Errors found

### Requirements

- Python 3.6 or higher
- Standard library only (no external dependencies)

### Validation Rules

**Expected Languages:**
- English (en) - KJV
- Spanish (es) - RVR1960
- Portuguese (pt) - ARC
- French (fr) - LSG1910
- Japanese (ja) - 新改訳2003
- Chinese (zh) - 和合本1919

**Expected Studies:** 7 studies total
- born_again_001
- cana_wedding_001
- lamb_of_god_001
- logos_creation_001
- morning_star_001
- natanael_fig_tree_001
- temple_cleansing_001

**File Naming Convention:**
- Format: `{study_name}_{language}_001.json`
- Example: `born_again_en_001.json`

### Automated Checks

The validator automatically checks for:
- ✅ All 42 files present (7 studies × 6 languages)
- ✅ Valid JSON syntax
- ✅ Correct language codes
- ✅ Correct Bible versions
- ✅ Matching structure across translations
- ✅ No English content in non-English files (for ja/zh)
- ✅ Index file completeness

### Adding New Translations

When adding a new language:
1. Update `EXPECTED_LANGUAGES` in the script
2. Add the Bible version mapping
3. Run validation to ensure consistency
