#!/usr/bin/env python3
"""
Comprehensive validation script for discovery study translations.

This script validates:
1. JSON format validity
2. No mixed languages in content
3. Structural consistency across translations
4. Field completeness and accuracy
5. Proper language codes and Bible versions
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import Counter

# Expected languages and their Bible versions
# Note: Some studies may use different Bible versions
EXPECTED_LANGUAGES = {
    'en': ['KJV', 'NIV'],  # Allow both KJV and NIV for English
    'es': ['RVR1960', 'NVI'],  # Allow both RVR1960 and NVI for Spanish
    'pt': ['ARC', 'NVI'],  # Allow both ARC and NVI for Portuguese
    'fr': ['LSG1910', 'TOB'],  # Allow both LSG1910 and TOB for French
    'ja': ['新改訳2003', 'リビングバイブル'],  # Allow both versions for Japanese
    'zh': ['和合本1919', '新译本']  # Allow both versions for Chinese
}

# Expected study IDs
EXPECTED_STUDIES = [
    'born_again_001',
    'cana_wedding_001',
    'cup_of_wrath_001',
    'gethsemane_agony_001',
    'lamb_of_god_001',
    'logos_creation_001',
    'morning_star_001',
    'natanael_fig_tree_001',
    'new_covenant_cup_001',
    'passed_from_death_001',
    'saints_resurrected_001',
    'temple_cleansing_001',
    'veil_torn_001'
]

# Language character patterns for detection
LANGUAGE_PATTERNS = {
    'en': re.compile(r'[a-zA-Z]{3,}'),  # English words
    'es': re.compile(r'[a-zA-Z]{3,}'),  # Spanish words (similar to English)
    'pt': re.compile(r'[a-zA-Z]{3,}'),  # Portuguese words (similar to English)
    'fr': re.compile(r'[a-zA-Z]{3,}'),  # French words (similar to English)
    'ja': re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+'),  # Japanese
    'zh': re.compile(r'[\u4E00-\u9FFF]+')  # Chinese
}


class ValidationReport:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        self.stats = {
            'total_files': 0,
            'valid_json': 0,
            'invalid_json': 0,
            'languages_found': set(),
            'studies_found': set()
        }

    def add_error(self, message: str):
        self.errors.append(f"❌ ERROR: {message}")

    def add_warning(self, message: str):
        self.warnings.append(f"⚠️  WARNING: {message}")

    def add_info(self, message: str):
        self.info.append(f"ℹ️  INFO: {message}")

    def print_report(self):
        print("\n" + "=" * 80)
        print("VALIDATION REPORT")
        print("=" * 80)
        
        print(f"\n📊 STATISTICS:")
        print(f"  Total files checked: {self.stats['total_files']}")
        print(f"  Valid JSON files: {self.stats['valid_json']}")
        print(f"  Invalid JSON files: {self.stats['invalid_json']}")
        print(f"  Languages found: {', '.join(sorted(self.stats['languages_found']))}")
        print(f"  Studies found: {len(self.stats['studies_found'])}")

        if self.info:
            print(f"\nℹ️  INFORMATION ({len(self.info)}):")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for msg in self.warnings:
                print(f"  {msg}")

        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for msg in self.errors:
                print(f"  {msg}")
            print("\n" + "=" * 80)
            return False
        else:
            print(f"\n✅ ALL VALIDATIONS PASSED!")
            print("=" * 80)
            return True


def load_json_file(filepath: Path, report: ValidationReport) -> Dict:
    """Load and validate JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            report.stats['valid_json'] += 1
            return data
    except json.JSONDecodeError as e:
        report.add_error(f"Invalid JSON in {filepath.name}: {e}")
        report.stats['invalid_json'] += 1
        return None
    except Exception as e:
        report.add_error(f"Error reading {filepath.name}: {e}")
        report.stats['invalid_json'] += 1
        return None


def detect_language_mix(text: str, expected_lang: str, report: ValidationReport, context: str) -> bool:
    """Detect if text contains mixed languages."""
    if not text or len(text.strip()) < 3:
        return True
    
    # For Asian languages, check if they're present
    if expected_lang in ['ja', 'zh']:
        pattern = LANGUAGE_PATTERNS[expected_lang]
        if not pattern.search(text):
            report.add_warning(f"{context}: Expected {expected_lang} characters but found none in: {text[:50]}...")
            return False
    
    # For Latin-based languages, check for unexpected characters
    elif expected_lang in ['en', 'es', 'pt', 'fr']:
        # Check if Asian characters are present (shouldn't be)
        if LANGUAGE_PATTERNS['ja'].search(text) or LANGUAGE_PATTERNS['zh'].search(text):
            report.add_error(f"{context}: Found Asian characters in {expected_lang} text: {text[:50]}...")
            return False
    
    return True


def validate_structure(data: Dict, lang: str, filename: str, report: ValidationReport) -> bool:
    """Validate the structure of a discovery study file."""
    required_fields = ['id', 'type', 'date', 'title', 'subtitle', 'language', 
                       'version', 'estimated_reading_minutes', 'key_verse', 
                       'cards', 'tags', 'metadata']
    
    is_valid = True
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            report.add_error(f"{filename}: Missing required field '{field}'")
            is_valid = False
    
    # Validate language and version
    if data.get('language') != lang:
        report.add_error(f"{filename}: Language mismatch - expected '{lang}', got '{data.get('language')}'")
        is_valid = False
    
    expected_versions = EXPECTED_LANGUAGES.get(lang)
    if expected_versions:
        if isinstance(expected_versions, list):
            if data.get('version') not in expected_versions:
                report.add_error(f"{filename}: Bible version mismatch - expected one of {expected_versions}, got '{data.get('version')}'")
                is_valid = False
        else:
            if data.get('version') != expected_versions:
                report.add_error(f"{filename}: Bible version mismatch - expected '{expected_versions}', got '{data.get('version')}'")
                is_valid = False
    
    # Validate cards array
    if 'cards' in data:
        if not isinstance(data['cards'], list):
            report.add_error(f"{filename}: 'cards' should be an array")
            is_valid = False
        elif len(data['cards']) == 0:
            report.add_error(f"{filename}: 'cards' array is empty")
            is_valid = False
    
    # Validate tags array
    if 'tags' in data:
        if not isinstance(data['tags'], list):
            report.add_error(f"{filename}: 'tags' should be an array")
            is_valid = False
        elif len(data['tags']) == 0:
            report.add_warning(f"{filename}: 'tags' array is empty")
    
    # Validate metadata
    if 'metadata' in data:
        if 'themes' not in data['metadata']:
            report.add_warning(f"{filename}: Missing 'themes' in metadata")
    
    return is_valid


def validate_content_translation(en_data: Dict, trans_data: Dict, lang: str, 
                                  filename: str, report: ValidationReport):
    """Validate that translation has same structure as English version."""
    
    # Compare number of cards
    en_cards = len(en_data.get('cards', []))
    trans_cards = len(trans_data.get('cards', []))
    if en_cards != trans_cards:
        report.add_error(f"{filename}: Card count mismatch - EN has {en_cards}, {lang.upper()} has {trans_cards}")
    
    # Compare number of tags
    en_tags = len(en_data.get('tags', []))
    trans_tags = len(trans_data.get('tags', []))
    if en_tags != trans_tags:
        report.add_error(f"{filename}: Tag count mismatch - EN has {en_tags}, {lang.upper()} has {trans_tags}")
    
    # Compare number of themes
    en_themes = len(en_data.get('metadata', {}).get('themes', []))
    trans_themes = len(trans_data.get('metadata', {}).get('themes', []))
    if en_themes != trans_themes:
        report.add_error(f"{filename}: Theme count mismatch - EN has {en_themes}, {lang.upper()} has {trans_themes}")
    
    # Validate each card structure
    for i, (en_card, trans_card) in enumerate(zip(en_data.get('cards', []), 
                                                   trans_data.get('cards', []))):
        if en_card.get('type') != trans_card.get('type'):
            report.add_error(f"{filename}: Card {i+1} type mismatch")
        
        if en_card.get('order') != trans_card.get('order'):
            report.add_error(f"{filename}: Card {i+1} order mismatch")
        
        # Check for content translation (shouldn't be empty)
        if 'content' in en_card:
            trans_content = trans_card.get('content', '')
            if not trans_content or trans_content == en_card['content']:
                report.add_warning(f"{filename}: Card {i+1} content may not be translated")


def validate_no_english_in_translation(data: Dict, lang: str, filename: str, 
                                       report: ValidationReport):
    """Check that non-English files don't contain English content."""
    if lang == 'en':
        return
    
    # Check tags for English
    tags = data.get('tags', [])
    english_pattern = re.compile(r'^[a-z_]+$')  # English-style tag pattern
    
    # For non-Latin languages, tags should not be all lowercase English
    if lang in ['ja', 'zh']:
        english_tags = [tag for tag in tags if english_pattern.match(str(tag))]
        if english_tags:
            report.add_error(f"{filename}: Found English tags in {lang.upper()}: {', '.join(english_tags[:3])}")
    
    # Check themes for English
    themes = data.get('metadata', {}).get('themes', [])
    if lang in ['ja', 'zh']:
        for theme in themes:
            if not LANGUAGE_PATTERNS[lang].search(str(theme)):
                # Check if it looks like English
                if re.search(r'\b[A-Z][a-z]+(\s+[a-z]+){2,}\b', str(theme)):
                    report.add_warning(f"{filename}: Theme may be in English: {theme[:50]}")


def validate_filename_format(filepath: Path, lang: str, report: ValidationReport) -> bool:
    """Validate that filename follows the correct naming convention."""
    filename = filepath.name
    
    # Expected pattern: {study_name}_{lang_code}_001.json
    # Examples: cana_wedding_en_001.json, gethsemane_agony_es_001.json
    pattern = re.compile(r'^[a-z_]+_(' + '|'.join(EXPECTED_LANGUAGES.keys()) + r')_001\.json$')
    
    if not pattern.match(filename):
        report.add_error(f"{filename}: Invalid filename format. Expected pattern: {{study_name}}_{{lang}}_001.json")
        return False
    
    # Verify the language code in filename matches the directory
    lang_in_filename = filename.split('_')[-2]
    if lang_in_filename != lang:
        report.add_error(f"{filename}: Language code mismatch - file is in {lang}/ directory but filename contains '{lang_in_filename}'")
        return False
    
    return True


def main():
    # Get discovery directory
    script_dir = Path(__file__).parent
    discovery_dir = script_dir.parent
    
    report = ValidationReport()
    
    print("🔍 Starting Discovery Studies Validation...")
    print(f"📁 Discovery directory: {discovery_dir}")
    
    # Store all loaded data for cross-validation
    all_studies = {}
    
    # Validate each language folder
    for lang, expected_versions in EXPECTED_LANGUAGES.items():
        lang_dir = discovery_dir / lang
        
        if not lang_dir.exists():
            report.add_warning(f"Missing language folder: {lang}")
            continue
        
        report.stats['languages_found'].add(lang)
        if isinstance(expected_versions, list):
            report.add_info(f"Checking {lang.upper()} folder with versions: {', '.join(expected_versions)}")
        else:
            report.add_info(f"Checking {lang.upper()} folder with {expected_versions}")
        
        # Load all files for this language
        lang_studies = {}
        
        # Get all JSON files in this language directory
        for filepath in lang_dir.glob('*_001.json'):
            filename = filepath.name
            # Extract study_id from filename (e.g., "born_again_en_001.json" -> "born_again_001")
            study_base = filename.replace(f'_{lang}_001.json', '_001')
            
            report.stats['total_files'] += 1
            
            # Validate filename format
            validate_filename_format(filepath, lang, report)
            
            # Load and validate JSON
            data = load_json_file(filepath, report)
            if data is None:
                continue
            
            # Validate structure
            validate_structure(data, lang, filename, report)
            
            # Store for cross-validation
            lang_studies[study_base] = data
            
            # Validate no English in translations
            validate_no_english_in_translation(data, lang, filename, report)
            
            # Track study IDs
            if data.get('id'):
                report.stats['studies_found'].add(data['id'])
        
        all_studies[lang] = lang_studies
    
    # Cross-validate translations against English
    if 'en' in all_studies:
        for lang in ['es', 'pt', 'fr', 'ja', 'zh']:
            if lang not in all_studies:
                continue
            
            for study_id in EXPECTED_STUDIES:
                if study_id in all_studies['en'] and study_id in all_studies[lang]:
                    filename = f"{study_id.replace('_001', '')}_{lang}_001.json"
                    validate_content_translation(
                        all_studies['en'][study_id],
                        all_studies[lang][study_id],
                        lang,
                        filename,
                        report
                    )
    
    # Validate index.json
    index_path = discovery_dir / 'index.json'
    if index_path.exists():
        report.add_info("Validating index.json")
        index_data = load_json_file(index_path, report)
        if index_data and 'studies' in index_data:
            index_study_ids = {study['id'] for study in index_data['studies']}
            if index_study_ids != set(EXPECTED_STUDIES):
                missing = set(EXPECTED_STUDIES) - index_study_ids
                extra = index_study_ids - set(EXPECTED_STUDIES)
                if missing:
                    report.add_error(f"index.json missing studies: {missing}")
                if extra:
                    report.add_warning(f"index.json has extra studies: {extra}")
            
            # Check that files listed in index actually exist
            for study in index_data['studies']:
                study_id = study.get('id')
                files = study.get('files', {})
                for lang, filename in files.items():
                    filepath = discovery_dir / lang / filename
                    if not filepath.exists():
                        report.add_error(f"index.json: Study {study_id} lists {lang}/{filename} but file doesn't exist")
    else:
        report.add_error("index.json not found")
    
    # Print report and return exit code
    success = report.print_report()
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
