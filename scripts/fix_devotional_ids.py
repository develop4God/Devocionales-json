#!/usr/bin/env python3
"""
ID Format Validator and Fixer for Devotional JSON Files

This script fixes the incorrect ID format in Japanese and Chinese devotional files.
The correct ID format must include: book+chapter+verse+bibleversion+date

Example correct format: "john15v5KJV20250801"
Example incorrect format: "リビングバイブル-20250801"
"""

import json
import re
import os
from typing import Dict, List, Tuple
from collections import defaultdict
import sys


class DevotionalIDFixer:
    """Fixes and validates devotional IDs"""
    
    # Constants
    MAX_BOOK_ABBREV_LENGTH = 15  # Maximum length for book abbreviations
    MAX_EXAMPLES_TO_SHOW = 3     # Number of example fixes to display
    
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.stats = {
            'files_processed': 0,
            'entries_fixed': 0,
            'entries_validated': 0,
            'errors': [],
            'duplicates': defaultdict(list)
        }
        
        # Bible book name mappings for different languages
        self.book_mappings = {
            # Japanese mappings
            'ガラテヤ人への手紙': 'galatians',
            'ヨハネの手紙第一': '1john',
            'ローマ人への手紙': 'romans',
            'エペソ人への手紙': 'ephesians',
            'ヨハネの福音書': 'john',
            'マタイの福音書': 'matthew',
            'マルコの福音書': 'mark',
            'ルカの福音書': 'luke',
            'ピリピ人への手紙': 'philippians',
            'コロサイ人への手紙': 'colossians',
            'テサロニケ人への手紙第一': '1thessalonians',
            'テサロニケ人への手紙第二': '2thessalonians',
            'テモテへの手紙第一': '1timothy',
            'テモテへの手紙第二': '2timothy',
            'テトスへの手紙': 'titus',
            'ピレモンへの手紙': 'philemon',
            'ヘブル人への手紙': 'hebrews',
            'ヤコブの手紙': 'james',
            'ペテロの手紙第一': '1peter',
            'ペテロの手紙第二': '2peter',
            'ヨハネの手紙第二': '2john',
            'ヨハネの手紙第三': '3john',
            'ユダの手紙': 'jude',
            'ヨハネの黙示録': 'revelation',
            '創世記': 'genesis',
            '出エジプト記': 'exodus',
            'レビ記': 'leviticus',
            '民数記': 'numbers',
            '申命記': 'deuteronomy',
            'ヨシュア記': 'joshua',
            '士師記': 'judges',
            'ルツ記': 'ruth',
            'サムエル記第一': '1samuel',
            'サムエル記第二': '2samuel',
            '列王記第一': '1kings',
            '列王記第二': '2kings',
            '歴代誌第一': '1chronicles',
            '歴代誌第二': '2chronicles',
            'エズラ記': 'ezra',
            'ネヘミヤ記': 'nehemiah',
            'エステル記': 'esther',
            'ヨブ記': 'job',
            '詩篇': 'psalms',
            '箴言': 'proverbs',
            '伝道者の書': 'ecclesiastes',
            '雅歌': 'songofsolomon',
            'イザヤ書': 'isaiah',
            'エレミヤ書': 'jeremiah',
            '哀歌': 'lamentations',
            'エゼキエル書': 'ezekiel',
            'ダニエル書': 'daniel',
            'ホセア書': 'hosea',
            'ヨエル書': 'joel',
            'アモス書': 'amos',
            'オバデヤ書': 'obadiah',
            'ヨナ書': 'jonah',
            'ミカ書': 'micah',
            'ナホム書': 'nahum',
            'ハバクク書': 'habakkuk',
            'ゼパニヤ書': 'zephaniah',
            'ハガイ書': 'haggai',
            'ゼカリヤ書': 'zechariah',
            'マラキ書': 'malachi',
            '使徒の働き': 'acts',
            'コリント人への手紙第一': '1corinthians',
            'コリント人への手紙第二': '2corinthians',
            
            # Chinese mappings
            '雅各书': 'james',
            '马太福音': 'matthew',
            '约翰福音': 'john',
            '约翰一书': '1john',
            '哥林多前书': '1corinthians',
            '哥林多后书': '2corinthians',
            '罗马书': 'romans',
            '以弗所书': 'ephesians',
            '腓立比书': 'philippians',
            '歌罗西书': 'colossians',
            '帖撒罗尼迦前书': '1thessalonians',
            '帖撒罗尼迦后书': '2thessalonians',
            '提摩太前书': '1timothy',
            '提摩太后书': '2timothy',
            '提多书': 'titus',
            '腓利门书': 'philemon',
            '希伯来书': 'hebrews',
            '彼得前书': '1peter',
            '彼得后书': '2peter',
            '约翰二书': '2john',
            '约翰三书': '3john',
            '犹大书': 'jude',
            '启示录': 'revelation',
            '马可福音': 'mark',
            '路加福音': 'luke',
            '使徒行传': 'acts',
            '加拉太书': 'galatians',
            '创世记': 'genesis',
            '出埃及记': 'exodus',
            '利未记': 'leviticus',
            '民数记': 'numbers',
            '申命记': 'deuteronomy',
            '约书亚记': 'joshua',
            '士师记': 'judges',
            '路得记': 'ruth',
            '撒母耳记上': '1samuel',
            '撒母耳记下': '2samuel',
            '列王纪上': '1kings',
            '列王纪下': '2kings',
            '历代志上': '1chronicles',
            '历代志下': '2chronicles',
            '以斯拉记': 'ezra',
            '尼希米记': 'nehemiah',
            '以斯帖记': 'esther',
            '约伯记': 'job',
            '诗篇': 'psalms',
            '箴言': 'proverbs',
            '传道书': 'ecclesiastes',
            '雅歌': 'songofsolomon',
            '以赛亚书': 'isaiah',
            '耶利米书': 'jeremiah',
            '耶利米哀歌': 'lamentations',
            '以西结书': 'ezekiel',
            '但以理书': 'daniel',
            '何西阿书': 'hosea',
            '约珥书': 'joel',
            '阿摩司书': 'amos',
            '俄巴底亚书': 'obadiah',
            '约拿书': 'jonah',
            '弥迦书': 'micah',
            '那鸿书': 'nahum',
            '哈巴谷书': 'habakkuk',
            '西番雅书': 'zephaniah',
            '哈该书': 'haggai',
            '撒迦利亚书': 'zechariah',
            '玛拉基书': 'malachi',
        }
        
        # Version abbreviations
        self.version_abbrev = {
            'リビングバイブル': 'LB',
            '新改訳2003': 'SHK2003',
            '和合本1919': 'CUV1919',
            '新译本': 'CNV',
            'KJV': 'KJV',
            'NIV': 'NIV',
            'NVI': 'NVI',
            'RVR1960': 'RVR1960',
            'LSG1910': 'LSG1910',
            'TOB': 'TOB',
            'ARC': 'ARC'
        }
    
    def extract_scripture_reference(self, versiculo: str) -> Tuple[str, str, str]:
        """
        Extract book, chapter, and verse from versiculo field.
        
        Examples:
        - "ガラテヤ人への手紙 2:20 リビングバイブル: ..." -> ("galatians", "2", "20")
        - "雅各书 2:17 和合本1919: ..." -> ("james", "2", "17")
        - "ローマ人への手紙 9:15-16 リビングバイブル: ..." -> ("romans", "9", "1516")
        """
        if not versiculo:
            return None, None, None
        
        # Try to match pattern: BookName Chapter:Verse(s) Version:
        # Pattern handles single verses (2:20) and ranges (9:15-16)
        pattern = r'^(.+?)\s+(\d+):(\d+(?:-\d+)?)\s+'
        match = re.match(pattern, versiculo)
        
        if not match:
            return None, None, None
        
        book_name = match.group(1).strip()
        chapter = match.group(2)
        verse_raw = match.group(3)
        
        # Convert book name to English abbreviation
        book_abbrev = self.book_mappings.get(book_name)
        if not book_abbrev:
            # If not in mapping, try to use a sanitized version
            book_abbrev = re.sub(r'[^\w]', '', book_name.lower())[:self.MAX_BOOK_ABBREV_LENGTH]
        
        # Handle verse ranges (e.g., "15-16" -> "1516")
        verse = verse_raw.replace('-', '')
        
        return book_abbrev, chapter, verse
    
    def generate_id(self, book: str, chapter: str, verse: str, version: str, date: str) -> str:
        """
        Generate ID in correct format: book+chapter+v+verse+version+date
        
        Example: "galatians2v20LB20250801"
        """
        if not all([book, chapter, verse, version, date]):
            return None
        
        # Get version abbreviation
        version_short = self.version_abbrev.get(version, version[:10])
        
        # Remove dashes from date
        date_clean = date.replace('-', '')
        
        # Generate ID
        return f"{book}{chapter}v{verse}{version_short}{date_clean}"
    
    def fix_file(self, filepath: str, dry_run: bool = False) -> Dict:
        """Fix IDs in a single devotional file"""
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Processing: {os.path.basename(filepath)}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            error_msg = f"Error reading {filepath}: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            return {'success': False, 'error': str(e)}
        
        fixed_count = 0
        error_count = 0
        
        # Navigate the nested structure
        if 'data' not in data:
            print("  ⚠️  No 'data' key found in file")
            return {'success': False, 'error': 'No data key'}
        
        for lang_key, lang_data in data['data'].items():
            for date_key, entries in lang_data.items():
                for entry in entries:
                    old_id = entry.get('id', '')
                    versiculo = entry.get('versiculo', '')
                    version = entry.get('version', '')
                    date = entry.get('date', '')
                    
                    # Extract scripture reference
                    book, chapter, verse = self.extract_scripture_reference(versiculo)
                    
                    if not all([book, chapter, verse]):
                        error_msg = f"Could not parse reference from: {versiculo[:100]}"
                        print(f"  ⚠️  {error_msg}")
                        self.stats['errors'].append(f"{filepath}: {error_msg}")
                        error_count += 1
                        continue
                    
                    # Generate new ID
                    new_id = self.generate_id(book, chapter, verse, version, date)
                    
                    if not new_id:
                        error_msg = f"Could not generate ID for date {date}"
                        print(f"  ⚠️  {error_msg}")
                        self.stats['errors'].append(f"{filepath}: {error_msg}")
                        error_count += 1
                        continue
                    
                    # Check if ID needs fixing
                    if old_id != new_id:
                        if not dry_run:
                            entry['id'] = new_id
                        fixed_count += 1
                        if fixed_count <= self.MAX_EXAMPLES_TO_SHOW:  # Show first few examples
                            print(f"  ✓ {old_id} -> {new_id}")
        
        if fixed_count > self.MAX_EXAMPLES_TO_SHOW:
            print(f"  ... and {fixed_count - self.MAX_EXAMPLES_TO_SHOW} more")
        
        # Write back to file if not dry run
        if not dry_run and fixed_count > 0:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  ✅ Fixed {fixed_count} entries")
            except Exception as e:
                error_msg = f"Error writing {filepath}: {str(e)}"
                print(f"  ❌ {error_msg}")
                self.stats['errors'].append(error_msg)
                return {'success': False, 'error': str(e)}
        elif dry_run:
            print(f"  📊 Would fix {fixed_count} entries")
        else:
            print(f"  ℹ️  No changes needed")
        
        if error_count > 0:
            print(f"  ⚠️  {error_count} errors encountered")
        
        self.stats['files_processed'] += 1
        self.stats['entries_fixed'] += fixed_count
        
        return {
            'success': True,
            'fixed_count': fixed_count,
            'error_count': error_count
        }
    
    def validate_file(self, filepath: str) -> Dict:
        """Validate IDs in a file and check for duplicates"""
        print(f"\nValidating: {os.path.basename(filepath)}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            error_msg = f"Error reading {filepath}: {str(e)}"
            print(f"  ❌ {error_msg}")
            self.stats['errors'].append(error_msg)
            return {'success': False, 'error': str(e)}
        
        id_count = defaultdict(int)
        validated_count = 0
        invalid_count = 0
        
        if 'data' not in data:
            print("  ⚠️  No 'data' key found in file")
            return {'success': False, 'error': 'No data key'}
        
        for lang_key, lang_data in data['data'].items():
            for date_key, entries in lang_data.items():
                for entry in entries:
                    entry_id = entry.get('id', '')
                    validated_count += 1
                    
                    # Count ID occurrences
                    id_count[entry_id] += 1
                    
                    # Basic validation: ID should have reasonable length and format
                    if len(entry_id) < 10 or not any(c.isdigit() for c in entry_id):
                        invalid_count += 1
                        if invalid_count <= 3:
                            print(f"  ⚠️  Suspicious ID: {entry_id}")
        
        # Check for duplicates
        duplicates = {id_val: count for id_val, count in id_count.items() if count > 1}
        
        if duplicates:
            print(f"  ⚠️  Found {len(duplicates)} duplicate IDs:")
            for id_val, count in list(duplicates.items())[:5]:
                print(f"     - {id_val}: {count} times")
                self.stats['duplicates'][filepath].append((id_val, count))
        else:
            print(f"  ✅ No duplicates found")
        
        if invalid_count > 0:
            print(f"  ⚠️  {invalid_count} potentially invalid IDs")
        
        print(f"  📊 Validated {validated_count} entries")
        self.stats['entries_validated'] += validated_count
        
        return {
            'success': True,
            'validated_count': validated_count,
            'duplicate_count': len(duplicates),
            'invalid_count': invalid_count
        }
    
    def generate_report(self, output_file: str = None):
        """Generate a comprehensive report of fixes and validation"""
        report = []
        report.append("=" * 80)
        report.append("DEVOTIONAL ID FIX AND VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"Files Processed:     {self.stats['files_processed']}")
        report.append(f"Entries Fixed:       {self.stats['entries_fixed']}")
        report.append(f"Entries Validated:   {self.stats['entries_validated']}")
        report.append(f"Errors Encountered:  {len(self.stats['errors'])}")
        report.append("")
        
        if self.stats['duplicates']:
            report.append("DUPLICATE IDs FOUND")
            report.append("-" * 80)
            for filepath, dups in self.stats['duplicates'].items():
                report.append(f"\n{os.path.basename(filepath)}:")
                for id_val, count in dups:
                    report.append(f"  - {id_val}: {count} occurrences")
            report.append("")
        
        if self.stats['errors']:
            report.append("ERRORS")
            report.append("-" * 80)
            for error in self.stats['errors']:
                report.append(f"  - {error}")
            report.append("")
        
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        print("\n" + report_text)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            print(f"\n📄 Report saved to: {output_file}")
        
        return report_text


def main():
    """Main execution function"""
    # Use relative path from script location or environment variable
    base_path = os.environ.get('DEVOTIONAL_PATH', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Initialize fixer
    fixer = DevotionalIDFixer(base_path)
    
    print("=" * 80)
    print("DEVOTIONAL ID FORMAT FIX SCRIPT")
    print("=" * 80)
    print("\nThis script will fix incorrect ID formats in JA and ZH devotional files.")
    print("Correct format: book+chapter+verse+version+date")
    print("Example: galatians2v20LB20250801")
    print("")
    
    # Files to fix (JA and ZH for 2025 and 2026)
    files_to_fix = [
        "Devocional_year_2025_ja_リビングバイブル.json",
        "Devocional_year_2025_ja_新改訳2003.json",
        "Devocional_year_2025_zh_和合本1919.json",
        "Devocional_year_2025_zh_新译本.json",
        "Devocional_year_2026_ja_リビングバイブル.json",
        "Devocional_year_2026_ja_新改訳2003.json",
        "Devocional_year_2026_zh_和合本1919.json",
        "Devocional_year_2026_zh_新译本.json",
    ]
    
    # All files to validate
    all_files = [
        # English
        "Devocional_year_2025_en_KJV.json",
        "Devocional_year_2025_en_NIV.json",
        "Devocional_year_2026_en_KJV.json",
        "Devocional_year_2026_en_NIV.json",
        # Spanish
        "Devocional_year_2025_es_NVI.json",
        "Devocional_year_2026_es_NVI.json",
        # Portuguese
        "Devocional_year_2025_pt_ARC.json",
        "Devocional_year_2025_pt_NVI.json",
        "Devocional_year_2026_pt_ARC.json",
        "Devocional_year_2026_pt_NVI.json",
        # French
        "Devocional_year_2025_fr_LSG1910.json",
        "Devocional_year_2025_fr_TOB.json",
        "Devocional_year_2026_fr_LSG1910.json",
        "Devocional_year_2026_fr_TOB.json",
        # Japanese
        "Devocional_year_2025_ja_リビングバイブル.json",
        "Devocional_year_2025_ja_新改訳2003.json",
        "Devocional_year_2026_ja_リビングバイブル.json",
        "Devocional_year_2026_ja_新改訳2003.json",
        # Chinese
        "Devocional_year_2025_zh_和合本1919.json",
        "Devocional_year_2025_zh_新译本.json",
        "Devocional_year_2026_zh_和合本1919.json",
        "Devocional_year_2026_zh_新译本.json",
    ]
    
    # Step 1: Fix JA and ZH files
    print("\n" + "=" * 80)
    print("STEP 1: FIXING JAPANESE AND CHINESE FILES")
    print("=" * 80)
    
    for filename in files_to_fix:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            fixer.fix_file(filepath, dry_run=False)
        else:
            print(f"\n⚠️  File not found: {filename}")
    
    # Step 2: Validate ALL files
    print("\n" + "=" * 80)
    print("STEP 2: VALIDATING ALL LANGUAGE FILES")
    print("=" * 80)
    
    for filename in all_files:
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            fixer.validate_file(filepath)
        else:
            print(f"\n⚠️  File not found: {filename}")
    
    # Step 3: Generate report
    print("\n" + "=" * 80)
    print("STEP 3: GENERATING REPORT")
    print("=" * 80)
    
    report_path = os.path.join(base_path, "scripts", "id_fix_report.txt")
    fixer.generate_report(report_path)
    
    print("\n✅ Script execution completed!")
    
    # Return exit code based on errors
    if fixer.stats['errors'] or fixer.stats['duplicates']:
        print("\n⚠️  Warning: Some issues were found. Please review the report.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
