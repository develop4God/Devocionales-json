#!/usr/bin/env python3
"""
Script to correct prayer closings in devotional JSON files.
This script focuses on specific common issues found in the validation.
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, Tuple

# Correct prayer closings for each language (standardized)
CORRECT_CLOSINGS = {
    'es': 'En el nombre de Jesús, amén.',
    'en': 'In the name of Jesus, amen.',
    'pt': 'Em nome de Jesus, amém.',
    'fr': 'Au nom de Jésus, amen.',
    'zh': '奉耶稣的名祷告，阿们。',
    'ja': 'イエス・キリストの御名によってお祈りします。アーメン。'
}


class DevotionalCorrector:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = None
        self.corrections = []
        self.stats = {
            'total_entries': 0,
            'corrected_entries': 0,
            'unchanged_entries': 0
        }
        
    def load_json(self) -> bool:
        """Load and parse JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def save_json(self) -> bool:
        """Save corrected JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def correct_spanish_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct Spanish prayer closings."""
        # Common incorrect patterns in Spanish
        patterns_to_fix = [
            # "En tu nombre" variations
            (r',?\s*[Ee]n\s+tu\s+nombre,?\s*amén\.?\s*$', ', En el nombre de Jesús, amén.'),
            (r',?\s*[Ee]n\s+[Tt]u\s+nombre,?\s+Jesús,?\s*amén\.?\s*$', ', En el nombre de Jesús, amén.'),
            # Case issues
            (r',?\s*en\s+el\s+nombre\s+de\s+Jesús,?\s*amén\.?\s*$', ', En el nombre de Jesús, amén.'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            if re.search(pattern, prayer_text):
                new_text = re.sub(pattern, replacement, prayer_text).strip()
                return (new_text, True)
        
        return (prayer_text, False)
    
    def correct_english_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct English prayer closings."""
        patterns_to_fix = [
            # "We ask" variations with adjectives
            (r',?\s*[Ww]e\s+ask\s+(all\s+)?th(is|ese\s+things)\s+in\s+the\s+(powerful|precious|redeeming|mighty|holy|blessed)?\s*(and\s+\w+)?\s*name\s+of\s+Jesus,?\s*amen\.?\s*$', ', In the name of Jesus, amen.'),
            (r',?\s*[Ww]e\s+ask\s+(all\s+)?th(is|ese\s+things)\s+in\s+the\s+name\s+of\s+Jesus,?\s*amén\.?\s*$', ', In the name of Jesus, amen.'),
            # "amén" should be "amen" in English
            (r',?\s*[Ii]n\s+the\s+name\s+of\s+Jesus,?\s*amén\.?\s*$', ', In the name of Jesus, amen.'),
            (r',?\s*[Ii]n\s+Jesus[\'\']?\s*name,?\s*amen\.?\s*$', ', In the name of Jesus, amen.'),
            # "In Your name" variations
            (r',?\s*[Ii]n\s+[Yy]our\s+name,?\s*amen\.?\s*$', ', In the name of Jesus, amen.'),
            (r',?\s*[Ii]n\s+[Yy]our\s+name,?\s*amén\.?\s*$', ', In the name of Jesus, amen.'),
            # Case issues
            (r',?\s*in\s+the\s+name\s+of\s+Jesus,?\s*amen\.?\s*$', ', In the name of Jesus, amen.'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            if re.search(pattern, prayer_text):
                new_text = re.sub(pattern, replacement, prayer_text).strip()
                return (new_text, True)
        
        return (prayer_text, False)
    
    def correct_portuguese_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct Portuguese prayer closings."""
        patterns_to_fix = [
            # Spanish closings in Portuguese files (most common issue!)
            (r',?\s*en\s+el\s+nombre\s+de\s+Jes[uú]s,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            # "Em Teu nome" variations
            (r',?\s*[Ee]m\s+[Tt]eu\s+nome,?\s*Jesus,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            (r',?\s*[Ee]m\s+[Tt]eu\s+santo\s+nome,?\s*Jesus,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            (r',?\s*[Ee]m\s+[Tt]eu\s+nome,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            (r',?\s*[Ee]m\s+[Tt]eu\s+nome,?\s*eu\s+oro,?\s*amém\.?\s*$', ', Em nome de Jesus, amém.'),
            (r',?\s*[Ee]m\s+teu\s+(santo\s+)?nome,?\s+oramos\.?\s*[Aa]mém\.?\s*$', ', Em nome de Jesus, amém.'),
            # "Em Cristo Jesus" variations
            (r',?\s*[Ee]m\s+Cristo\s+Jesus,?\s*eu\s+oro,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            (r',?\s*[Ee]m\s+Jesus,?\s+pedimos,?\s*amém\.?\s*$', ', Em nome de Jesus, amém.'),
            # Wrong accent (amén instead of amém)
            (r',?\s*[Ee]m\s+nome\s+de\s+Jesus,?\s*amén\.?\s*$', ', Em nome de Jesus, amém.'),
            # Case issues
            (r',?\s*em\s+nome\s+de\s+Jesus,?\s*amém\.?\s*$', ', Em nome de Jesus, amém.'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            if re.search(pattern, prayer_text):
                new_text = re.sub(pattern, replacement, prayer_text).strip()
                return (new_text, True)
        
        return (prayer_text, False)
    
    def correct_french_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct French prayer closings."""
        patterns_to_fix = [
            # "dans le nom" should be "au nom"
            (r',?\s*[Dd]ans\s+le\s+nom\s+de\s+Jésus,?\s*amen\.?\s*$', ', Au nom de Jésus, amen.'),
            (r',?\s*[Dd]ans\s+le\s+nom\s+de\s+Jésus,?\s*amén\.?\s*$', ', Au nom de Jésus, amen.'),
            # "en le nom" should be "au nom"
            (r',?\s*[Ee]n\s+le\s+nom\s+de\s+Jésus,?\s*amén\.?\s*$', ', Au nom de Jésus, amen.'),
            (r',?\s*[Ee]n\s+le\s+nom\s+de\s+Jésus,?\s*amen\.?\s*$', ', Au nom de Jésus, amen.'),
            # "en ce nom" should be "au nom"
            (r',?\s*[Ee]n\s+ce\s+nom\s+de\s+Jésus,?\s*amen\.?\s*$', ', Au nom de Jésus, amen.'),
            (r',?\s*[Ee]n\s+ce\s+nom\s+de\s+Jésus,?\s*amén\.?\s*$', ', Au nom de Jésus, amen.'),
            # Wrong accent (amén instead of amen)
            (r',?\s*[Aa]u\s+nom\s+de\s+Jésus,?\s*amén\.?\s*$', ', Au nom de Jésus, amen.'),
            # "Amen" instead of "amen"
            (r',?\s*[Aa]u\s+nom\s+de\s+Jésus,?\s*Amen\.?\s*$', ', Au nom de Jésus, amen.'),
            # Case issues
            (r',?\s*au\s+nom\s+de\s+Jésus,?\s*amen\.?\s*$', ', Au nom de Jésus, amen.'),
        ]
        
        for pattern, replacement in patterns_to_fix:
            if re.search(pattern, prayer_text):
                new_text = re.sub(pattern, replacement, prayer_text).strip()
                return (new_text, True)
        
        return (prayer_text, False)
    
    def correct_chinese_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct Chinese prayer closings - do not modify, too many variations."""
        # Chinese has many acceptable variations, so we won't modify
        return (prayer_text, False)
    
    def correct_japanese_prayer_closing(self, prayer_text: str) -> Tuple[str, bool]:
        """Correct Japanese prayer closings - do not modify, too many variations."""
        # Japanese has many acceptable variations, so we won't modify
        return (prayer_text, False)
    
    def correct_prayer_closing(self, prayer_text: str, lang: str) -> Tuple[str, bool]:
        """
        Correct the prayer closing based on language.
        Returns (corrected_text, was_changed)
        """
        if not prayer_text or lang not in CORRECT_CLOSINGS:
            return (prayer_text, False)
        
        # Call language-specific correction function
        if lang == 'es':
            return self.correct_spanish_prayer_closing(prayer_text)
        elif lang == 'en':
            return self.correct_english_prayer_closing(prayer_text)
        elif lang == 'pt':
            return self.correct_portuguese_prayer_closing(prayer_text)
        elif lang == 'fr':
            return self.correct_french_prayer_closing(prayer_text)
        elif lang == 'zh':
            return self.correct_chinese_prayer_closing(prayer_text)
        elif lang == 'ja':
            return self.correct_japanese_prayer_closing(prayer_text)
        
        return (prayer_text, False)
    
    def correct_entry(self, entry: Dict, date: str, lang: str) -> None:
        """Correct a single devotional entry."""
        self.stats['total_entries'] += 1
        entry_id = entry.get('id', 'unknown')
        
        # Check and correct prayer (oracion field)
        if 'oracion' in entry:
            original = entry['oracion']
            corrected, changed = self.correct_prayer_closing(original, lang)
            
            if changed:
                entry['oracion'] = corrected
                self.corrections.append({
                    'file': self.file_path.name,
                    'date': date,
                    'entry_id': entry_id,
                    'field': 'oracion',
                    'original_closing': original[-100:] if len(original) > 100 else original,
                    'corrected_closing': corrected[-100:] if len(corrected) > 100 else corrected
                })
                self.stats['corrected_entries'] += 1
            else:
                self.stats['unchanged_entries'] += 1
    
    def correct_all(self) -> bool:
        """Correct all entries in the file."""
        if not self.load_json():
            return False
        
        # Extract language from filename
        filename = self.file_path.name
        lang_match = re.search(r'_([a-z]{2})_', filename)
        if not lang_match:
            print(f"Cannot determine language from filename: {filename}")
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
        
        # Correct each entry
        for date, entries in dates.items():
            if isinstance(entries, list):
                for entry in entries:
                    self.correct_entry(entry, date, lang)
        
        # Save if corrections were made
        if self.stats['corrected_entries'] > 0:
            return self.save_json()
        
        return True
    
    def get_report(self) -> str:
        """Generate a correction report."""
        report = []
        report.append(f"\n{'='*80}")
        report.append(f"Correction Report: {self.file_path.name}")
        report.append(f"{'='*80}")
        report.append(f"Total entries: {self.stats['total_entries']}")
        report.append(f"Corrected entries: {self.stats['corrected_entries']}")
        report.append(f"Unchanged entries: {self.stats['unchanged_entries']}")
        
        if self.corrections:
            report.append(f"\nCorrections made: {len(self.corrections)}")
            report.append("-" * 80)
            for correction in self.corrections[:5]:  # Show first 5
                report.append(f"\nDate: {correction['date']}")
                report.append(f"Entry ID: {correction['entry_id']}")
                report.append(f"Original: ...{correction['original_closing']}")
                report.append(f"Corrected: ...{correction['corrected_closing']}")
                report.append("-" * 40)
            if len(self.corrections) > 5:
                report.append(f"\n... and {len(self.corrections) - 5} more corrections")
        else:
            report.append("\n✓ No corrections needed!")
        
        return '\n'.join(report)


def main():
    """Main function to run corrections on all devotional files."""
    base_path = Path('/home/runner/work/Devocionales-json/Devocionales-json')
    
    # Define files to correct
    languages = ['es', 'en', 'pt', 'fr', 'zh', 'ja']
    years = ['2025', '2026']
    
    all_correctors = []
    
    print("=" * 80)
    print("DEVOTIONAL JSON CORRECTION TOOL")
    print("=" * 80)
    
    # Find all relevant files
    for year in years:
        for lang in languages:
            # Find files matching the pattern
            pattern = f"Devocional_year_{year}_{lang}_*.json"
            files = list(base_path.glob(pattern))
            
            for file_path in files:
                print(f"\nCorrecting: {file_path.name}")
                corrector = DevotionalCorrector(file_path)
                corrector.correct_all()
                all_correctors.append(corrector)
                print(corrector.get_report())
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    
    total_files = len(all_correctors)
    total_entries = sum(c.stats['total_entries'] for c in all_correctors)
    total_corrections = sum(c.stats['corrected_entries'] for c in all_correctors)
    
    print(f"Files processed: {total_files}")
    print(f"Total entries: {total_entries}")
    print(f"Total corrections: {total_corrections}")
    
    if total_corrections == 0:
        print("\n✓ All files are correct!")
        return 0
    else:
        print(f"\n✓ Made {total_corrections} corrections successfully!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
