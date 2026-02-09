
# 🚦 Discovery Studies Validation Workflow

## 🏁 Overview
This folder contains all scripts needed to validate the structure, translation, and consistency of the Discovery Studies JSON files across all languages and studies.

---

## 🧑‍💻 Main Scripts

- **🚀 master_validator.py**: The all-in-one orchestrator. Runs all validations for the entire codebase automatically.
- **🌐 validate_translations.py**: Global validator. Checks all translation files for JSON validity, structure, language codes, and completeness using index.json as the source of truth.
- **📊 validate_structure_bulk.py**: Per-study structure validator. Checks that all language versions of a specific study match the structure of the English base file.

---

## 🔄 Typical Validation Flows

### 1️⃣ Full Codebase Validation (Recommended)
Run this to check everything in one go:

```bash
python3 master_validator.py
```
- ✅ Runs global translation/JSON validation for all files
- ✅ Then, for every study, uses the English file as a template to check all language versions for structure
- 🛑 If any errors are found in phase 1, phase 2 will not run
- 🟢 If all pass, your codebase is fully validated!

### 2️⃣ Validate All Translations Only

```bash
python3 validate_translations.py
```
- 🌐 Checks all translation files for JSON, structure, and language issues
- Uses index.json as the source of truth

### 3️⃣ Validate Structure for a Single Study

```bash
python3 validate_structure_bulk.py discovery/en/<study_file_en>.json
```
- 📊 Checks that all language versions for the specified study match the English base file
- Example:
  ```bash
  python3 validate_structure_bulk.py discovery/en/zechariah_14_return_en_001.json
  ```

---

## 🤖 How It Works

- **master_validator.py** automatically finds all English base files in the en/ folder and runs the bulk structure validator for each, so you never have to do it manually for every study.
- If you run validate_structure_bulk.py directly, you must specify the English base file for the study you want to check.
- All scripts print clear error messages and stop on failure, so you always know what to fix.

---

## 📝 Quick Reference

- ▶️ Run `master_validator.py` for full validation (global + all studies)
- ▶️ Run `validate_translations.py` for global translation/JSON checks
- ▶️ Run `validate_structure_bulk.py` with an English file for per-study structure checks

---

## 📋 Validation Details & Rules

### 🌐 validate_translations.py — Two-Phase Validation

**PHASE A: Index Validation**
- 🗂️ Validates index.json format, structure, and data integrity
- 🕵️ Checks for missing translations and marks them as PENDING
- 🛑 If Phase A fails, validation stops and errors are reported
- 📖 index.json becomes the single source of truth for Phase B

**PHASE B: Translation Files Validation**
- ▶️ Only runs if Phase A passes
- 📚 Uses index.json as the authoritative source of studies
- 📝 Validates all translation files referenced in index.json
- 🏷️ Verifies file existence, structure, and content quality

#### Key Checks
- ✅ JSON format and syntax
- ✅ Required fields: id, version, emoji, files, titles, subtitles, estimated_reading_minutes
- ✅ Data structure integrity
- ✅ No duplicate study IDs
- ✅ Correct language codes (en, es, pt, fr, ja, zh)
- ✅ Proper Bible version for each language
- ✅ No mixed languages in content
- ✅ All required fields present in each file
- ✅ Array structures (cards, tags, themes)
- ✅ Metadata completeness
- ✅ Card, tag, and theme counts match across translations
- ✅ No English content in non-English files (for ja/zh)
- ✅ All files listed in index.json exist and follow naming convention

#### 📦 Expected Languages
- 🇬🇧 English (en) - KJV, NIV
- 🇪🇸 Spanish (es) - RVR1960, NVI
- 🇵🇹 Portuguese (pt) - ARC, NVI
- 🇫🇷 French (fr) - LSG1910, TOB
- 🇯🇵 Japanese (ja) - 新改訳2003, リビングバイブル
- 🇨🇳 Chinese (zh) - 和合本1919, 新译本

#### 📁 File Naming Convention
- Format: `{study_name}_{language}_001.json`
- Example: `born_again_en_001.json`

#### 🖥️ Usage

```bash
# From the discovery folder
python3 scripts/validate_translations.py
# Make it executable (optional)
chmod +x scripts/validate_translations.py
./scripts/validate_translations.py
```

#### 🟢 Expected Output
- **Phase A Report**: Index validation results
- **Phase B Report**: Translation files validation (only if Phase A passes)
- Statistics (total files, languages, studies, pending translations)
- Information messages, warnings, and errors
- Exit code: `0` = All validations passed, `1` = Errors found

#### ⚙️ Requirements
- Python 3.6 or higher
- Standard library only (no external dependencies)

---

## ➕ Adding New Translations

1. 📝 Update index.json with the new study entry
2. ✅ Ensure all required fields are present
3. 📂 Add translation files to appropriate language folders
4. 🔄 Run validation — it will automatically use index.json as source of truth
5. 🟡 Fix any PENDING translations as needed

### 🟡 Understanding PENDING Status
- Studies with incomplete translations are reported as PENDING in Phase A
- Shows which languages are missing for each study
- Helps track translation progress
- Does not cause validation failure (only a warning)
