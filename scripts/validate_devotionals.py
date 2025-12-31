#!/usr/bin/env python3
"""
Script to validate language integrity and prayer closings in devotional JSON files.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Language detection patterns (simple heuristics)
LANGUAGE_PATTERNS = {
    'es': {
        'patterns': [
            r'\b(el|la|los|las|de|del|que|y|es|en|por|para|con|un|una)\b',
            r'\b(Dios|Señor|Padre|Cristo|Jesús|ción|dad|mente)\b'
        ],
        'min_matches': 3
    },
    'en': {
        'patterns': [
            r'\b(the|of|and|to|in|is|that|for|it|with|as|be|this|by)\b',
            r'\b(God|Lord|Father|Christ|Jesus|tion|ness|ment)\b'
        ],
        'min_matches': 3
    },
    'pt': {
        'patterns': [
            r'\b(o|a|os|as|de|que|e|do|da|em|um|uma|para|com|não)\b',
            r'\b(Deus|Senhor|Pai|Cristo|Jesus|ção|dade|mente)\b'
        ],
        'min_matches': 3
    },
    'fr': {
        'patterns': [
            r'\b(le|la|les|de|du|des|et|un|une|dans|pour|avec|est|que)\b',
            r'\b(Dieu|Seigneur|Père|Christ|Jésus|tion|ité|ment)\b'
        ],
        'min_matches': 3
    },
    'zh': {
        'patterns': [
            r'[上帝神主耶稣基督圣灵天父]',
            r'[\u4e00-\u9fff]{2,}'  # Chinese characters
        ],
        'min_matches': 5
    },
    'ja': {
        'patterns': [
            r'[神主イエスキリスト聖霊父]',
            r'[\u3040-\u309f\u30a0-\u30ff]{2,}'  # Hiragana and Katakana
        ],
        'min_matches': 5
    }
}

# Expected prayer closings for each language
PRAYER_CLOSINGS = {
    'es': [
        r'[Ee]n el nombre de Jesús,?\s*amén\.?$',
        r'[Ee]n nombre de Jesús,?\s*amén\.?$'
    ],
    'en': [
        r'[Ii]n the name of Jesus,?\s*amen\.?$'
    ],
    'pt': [
        r'[Ee]m nome de Jesus,?\s*amén\.?$',
        r'[Ee]m nome de Jesus,?\s*amém\.?$',
        r'[Ee]m o nome de Jesus,?\s*amén\.?$',
        r'[Ee]m o nome de Jesus,?\s*amém\.?$'
    ],
    'fr': [
        r'[Aa]u nom de Jésus,?\s*amen\.?$',
        r'[Ee]n le nom de Jésus,?\s*amen\.?$',
        r'[Ee]n le nom de Jésus,?\s*amén\.?$',
        r'[Dd]ans le nom de Jésus,?\s*amen\.?$'
    ],
    'zh': [
        r'[奉在].*耶稣.*[的]?名.*[祷告祈求],?\s*[阿啊]们[。\.!！]?$',
        r'[奉在].*主.*[的]?名.*[祷告祈求],?\s*[阿啊]们[。\.!！]?$'
    ],
    'ja': [
        r'イエス.*名.*祈.*アーメン[。\.]?$',
        r'主.*名.*祈.*アーメン[。\.]?$',
        r'キリスト.*名.*アーメン[。\.]?$'
    ]
}

class DevotionalValidator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = None
        self.issues = []
        self.stats = {
            'total_entries': 0,
            'language_mismatches': 0,
            'prayer_closing_issues': 0,
            'valid_entries': 0
        }
        
    def load_json(self) -> bool:
        """Load and parse JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except Exception as e:
            self.issues.append(f"Error loading file: {e}")
            return False
    
    def detect_language(self, text: str, expected_lang: str) -> Tuple[bool, int]:
        """
        Detect if text matches expected language.
        Returns (is_match, confidence_score)
        """
        if not text or len(text.strip()) < 50:
            return (True, 0)  # Too short to validate reliably
        
        if expected_lang not in LANGUAGE_PATTERNS:
            return (True, 0)  # Unknown language, skip
        
        patterns = LANGUAGE_PATTERNS[expected_lang]['patterns']
        min_matches = LANGUAGE_PATTERNS[expected_lang].get('min_matches', 3)
        
        # For longer texts, require more matches
        if len(text) > 200:
            min_matches = min_matches * 2
        
        total_matches = 0
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            total_matches += len(matches)
        
        # Check if we have enough matches for this language
        is_match = total_matches >= min_matches
        return (is_match, total_matches)
    
    def check_prayer_closing(self, prayer_text: str, expected_lang: str) -> bool:
        """Check if prayer ends with correct closing for the language."""
        if not prayer_text:
            return False
        
        # Clean up the text
        prayer_text = prayer_text.strip()
        
        if expected_lang not in PRAYER_CLOSINGS:
            return True  # Unknown language, skip validation
        
        closings = PRAYER_CLOSINGS[expected_lang]
        
        for closing_pattern in closings:
            if re.search(closing_pattern, prayer_text, re.IGNORECASE | re.MULTILINE):
                return True
        
        return False
    
    def validate_entry(self, entry: Dict, date: str, lang: str) -> None:
        """Validate a single devotional entry."""
        self.stats['total_entries'] += 1
        entry_id = entry.get('id', 'unknown')
        has_issues = False
        
        # Fields to check for language integrity
        # Only check longer content fields (reflexion and oracion)
        # para_meditar items are often short Bible verses and cause false positives
        fields_to_check = {
            'reflexion': entry.get('reflexion', ''),
            # oracion checked separately for closing
        }
        
        # Validate language for each field
        for field_name, text in fields_to_check.items():
            is_match, score = self.detect_language(text, lang)
            if not is_match:
                self.issues.append({
                    'file': self.file_path.name,
                    'date': date,
                    'entry_id': entry_id,
                    'field': field_name,
                    'issue': 'Possible incorrect language',
                    'expected_lang': lang,
                    'confidence': score,
                    'sample': text[:100] + '...' if len(text) > 100 else text
                })
                self.stats['language_mismatches'] += 1
                has_issues = True
        
        # Validate prayer closing
        oracion = entry.get('oracion', '')
        if oracion and not self.check_prayer_closing(oracion, lang):
            # Extract the last 100 characters to show the closing
            closing_sample = oracion[-100:] if len(oracion) > 100 else oracion
            self.issues.append({
                'file': self.file_path.name,
                'date': date,
                'entry_id': entry_id,
                'field': 'oracion',
                'issue': 'Incorrect prayer closing',
                'expected_lang': lang,
                'closing_sample': closing_sample
            })
            self.stats['prayer_closing_issues'] += 1
            has_issues = True
        
        if not has_issues:
            self.stats['valid_entries'] += 1
    
    def validate(self) -> bool:
        """Validate all entries in the file."""
        if not self.load_json():
            return False
        
        # Extract language from filename
        filename = self.file_path.name
        
        # Try to extract language code from filename
        lang_match = re.search(r'_([a-z]{2})_', filename)
        if not lang_match:
            self.issues.append({
                'file': filename,
                'issue': 'Cannot determine language from filename'
            })
            return False
        
        lang = lang_match.group(1)
        
        # Navigate the JSON structure
        if 'data' in self.data:
            data_section = self.data['data']
            if lang in data_section:
                dates = data_section[lang]
            else:
                # Sometimes the language key might be different
                dates = data_section.get(list(data_section.keys())[0], {})
        else:
            # Assume direct date structure
            dates = self.data
        
        # Validate each entry
        for date, entries in dates.items():
            if isinstance(entries, list):
                for entry in entries:
                    self.validate_entry(entry, date, lang)
        
        return True
    
    def get_report(self) -> str:
        """Generate a validation report."""
        report = []
        report.append(f"\n{'='*80}")
        report.append(f"Validation Report: {self.file_path.name}")
        report.append(f"{'='*80}")
        report.append(f"Total entries: {self.stats['total_entries']}")
        report.append(f"Valid entries: {self.stats['valid_entries']}")
        report.append(f"Language mismatches: {self.stats['language_mismatches']}")
        report.append(f"Prayer closing issues: {self.stats['prayer_closing_issues']}")
        
        if self.issues:
            report.append(f"\nIssues found: {len(self.issues)}")
            report.append("-" * 80)
            for issue in self.issues:
                report.append(f"\nDate: {issue.get('date', 'N/A')}")
                report.append(f"Entry ID: {issue.get('entry_id', 'N/A')}")
                report.append(f"Field: {issue.get('field', 'N/A')}")
                report.append(f"Issue: {issue.get('issue', 'N/A')}")
                if 'sample' in issue:
                    report.append(f"Sample: {issue['sample']}")
                if 'closing_sample' in issue:
                    report.append(f"Closing: {issue['closing_sample']}")
                report.append("-" * 40)
        else:
            report.append("\n✓ No issues found!")
        
        return '\n'.join(report)


def main():
    """Main function to run validation on all devotional files."""
    base_path = Path('/home/runner/work/Devocionales-json/Devocionales-json')
    
    # Define files to validate
    languages = ['es', 'en', 'pt', 'fr', 'zh', 'ja']
    years = ['2025', '2026']
    
    all_validators = []
    
    print("=" * 80)
    print("DEVOTIONAL JSON VALIDATION TOOL")
    print("=" * 80)
    
    # Find all relevant files
    for year in years:
        for lang in languages:
            # Find files matching the pattern
            pattern = f"Devocional_year_{year}_{lang}_*.json"
            files = list(base_path.glob(pattern))
            
            for file_path in files:
                print(f"\nValidating: {file_path.name}")
                validator = DevotionalValidator(file_path)
                validator.validate()
                all_validators.append(validator)
                print(validator.get_report())
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    
    total_files = len(all_validators)
    total_entries = sum(v.stats['total_entries'] for v in all_validators)
    total_issues = sum(len(v.issues) for v in all_validators)
    total_lang_issues = sum(v.stats['language_mismatches'] for v in all_validators)
    total_prayer_issues = sum(v.stats['prayer_closing_issues'] for v in all_validators)
    
    print(f"Files validated: {total_files}")
    print(f"Total entries: {total_entries}")
    print(f"Total issues: {total_issues}")
    print(f"  - Language mismatches: {total_lang_issues}")
    print(f"  - Prayer closing issues: {total_prayer_issues}")
    
    if total_issues == 0:
        print("\n✓ All files validated successfully!")
        return 0
    else:
        print(f"\n⚠ Found {total_issues} issues that need attention")
        return 1


if __name__ == '__main__':
    sys.exit(main())
