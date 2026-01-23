# Devotional Scripts

This folder contains scripts for managing and validating devotional JSON files.

## Scripts

### fix_devotional_ids.py

**Purpose**: Fixes incorrect ID format in devotional JSON files and validates all files for duplicates.

**Problem Solved**: Japanese and Chinese devotional files had incorrect ID formats that only included version and date, missing the critical chapter and verse information needed for unique identification.

**What it does**:
1. Fixes ID format in Japanese and Chinese files (2025 and 2026)
2. Converts IDs from format: `"リビングバイブル-20250801"` to `"galatians2v20LB20250801"`
3. Validates all language files for duplicate IDs
4. Generates a comprehensive report

**Usage**:
```bash
python3 scripts/fix_devotional_ids.py
```

**Output**:
- Fixes all JA and ZH files in place
- Creates report at `scripts/id_fix_report.txt`
- Shows progress and statistics during execution

**ID Format**:
Correct format: `{book}{chapter}v{verse}{version}{date}`
- Example: `"galatians2v20LB20250801"`
  - Book: galatians
  - Chapter: 2
  - Verse: 20
  - Version: LB (リビングバイブル)
  - Date: 20250801 (August 1, 2025)

**Files Fixed**:
- Devocional_year_2025_ja_リビングバイブル.json (365 entries)
- Devocional_year_2025_ja_新改訳2003.json (365 entries)
- Devocional_year_2025_zh_和合本1919.json (365 entries)
- Devocional_year_2025_zh_新译本.json (365 entries)
- Devocional_year_2026_ja_リビングバイブル.json (365 entries)
- Devocional_year_2026_ja_新改訳2003.json (365 entries)
- Devocional_year_2026_zh_和合本1919.json (10 entries)
- Devocional_year_2026_zh_新译本.json (365 entries)

**Total**: 2,565 entries fixed across 8 files

## Report

The script generates a detailed report showing:
- Number of files processed
- Number of entries fixed
- Number of entries validated
- Any duplicate IDs found
- Any errors encountered

Example output:
```
Files Processed:     8
Entries Fixed:       2565
Entries Validated:   7673
Errors Encountered:  0
```
