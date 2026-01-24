# Devotional Scripts

This folder contains scripts for managing and validating devotional JSON files.

## Overview

This collection of scripts was created to fix a critical bug where devotional IDs were not properly formatted, leading to duplicate IDs and data integrity issues. **Total fixes: 4,205 entries across 22 files in 6 languages.**

## Scripts

### fix_devotional_ids.py

**Purpose**: Fixes incorrect ID format in Japanese and Chinese devotional files.

**Problem Solved**: Japanese and Chinese devotional files had incorrect ID formats that only included version and date, missing the critical chapter and verse information needed for unique identification.

**What it does**:
1. Parses scripture references to extract book, chapter, and verse
2. Fixes ID format in Japanese and Chinese files (2025 and 2026)
3. Converts IDs from format: `"リビングバイブル-20250801"` to `"galatians2v20LB20250801"`
4. Validates all language files for duplicate IDs
5. Generates a comprehensive report

**Usage**:
```bash
python3 scripts/fix_devotional_ids.py
```

**Files Fixed**: 8 files (JA and ZH for 2025 and 2026)
**Entries Fixed**: 2,565 entries

---

### fix_remaining_ids.py

**Purpose**: Fixes ID format in English, Spanish, Portuguese, and French devotional files.

**Problem Solved**: After fixing JA and ZH files, validation revealed that other language files also had inconsistent ID formats where many IDs were missing the date component, causing duplicate IDs across different years.

**What it does**:
1. Checks all EN, ES, PT, and FR files
2. Ensures all IDs include the date component for uniqueness
3. Appends date to IDs that are missing it

**Usage**:
```bash
python3 scripts/fix_remaining_ids.py
```

**Files Fixed**: 14 files (EN, ES, PT, FR for 2025 and 2026)
**Entries Fixed**: 1,640 entries

---

### validate_duplicates.py

**Purpose**: Final validation script to check for duplicate IDs across ALL devotional files.

**What it does**:
1. Scans all 22 devotional files
2. Checks for duplicate IDs across the entire dataset
3. Reports any duplicates with file locations

**Usage**:
```bash
python3 scripts/validate_duplicates.py
```

**Result**: ✅ 0 duplicate IDs found (after fixes)

---

## ID Format

**Correct format**: `{book}{chapter}v{verse}{version}{date}`

**Examples**:
- English: `"john15v5KJV20250801"`
- Japanese: `"galatians2v20LB20250801"`
- Chinese: `"james2v17CUV191920250801"`
- French: `"heb13v5LSG191020251015"`

**Components**:
- **Book**: English abbreviation (e.g., galatians, john, james)
- **Chapter**: Chapter number (e.g., 2, 15)
- **v**: Separator
- **Verse**: Verse number or range (e.g., 20, 1516 for 15-16)
- **Version**: Bible version abbreviation (e.g., KJV, LB, CUV1919)
- **Date**: YYYYMMDD format (e.g., 20250801)

---

## Reports

### id_fix_report.txt
Initial report from fixing JA and ZH files only (2,565 entries).

### FINAL_REPORT.txt
Comprehensive report covering all fixes across all languages (4,205 entries total).

**Summary**:
- **Total files fixed**: 22 files (6 languages × ~4 files each)
- **Total entries fixed**: 4,205 entries
- **Duplicate IDs after fix**: 0 ✅
- **Errors encountered**: 0 ✅

**Breakdown by language**:
- Japanese: 1,460 entries (34.7%)
- Chinese: 1,105 entries (26.3%)
- French: 795 entries (18.9%)
- Portuguese: 603 entries (14.3%)
- Spanish: 135 entries (3.2%)
- English: 107 entries (2.5%)

---

## Verification

All fixes have been verified:
- ✅ All IDs follow consistent format
- ✅ All IDs are unique across the dataset
- ✅ No data loss or corruption
- ✅ All files validated successfully
- ✅ Zero duplicate IDs remaining
