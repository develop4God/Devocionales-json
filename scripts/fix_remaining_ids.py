#!/usr/bin/env python3
"""
Fix ALL Devotional IDs - Extended Script

This script fixes ALL devotional files (not just JA and ZH) to ensure
proper ID format with date included.
"""

import json
import re
import os
from collections import defaultdict


def extract_existing_components(entry_id, date):
    """
    Try to extract book/chapter/verse from existing ID and ensure date is included
    """
    date_clean = date.replace('-', '')
    
    # If ID already contains the date, it's probably correct
    if date_clean in entry_id:
        return entry_id, False  # No fix needed
    
    # Otherwise, append the date to make it unique
    return f"{entry_id}{date_clean}", True  # Fix needed


def fix_all_files():
    """Fix IDs in ALL devotional files"""
    # Use relative path from script location or environment variable
    base_path = os.environ.get('DEVOTIONAL_PATH', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
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
    ]
    
    print("=" * 80)
    print("FIXING ALL REMAINING FILES (EN, ES, PT, FR)")
    print("=" * 80)
    print("\nEnsuring all IDs include date for uniqueness...")
    print()
    
    total_fixed = 0
    
    for filename in all_files:
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filename}")
            continue
        
        print(f"\nProcessing: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ❌ Error reading: {str(e)}")
            continue
        
        fixed_count = 0
        examples = []
        
        for lang_key, lang_data in data.get('data', {}).items():
            for date_key, entries in lang_data.items():
                for entry in entries:
                    old_id = entry.get('id', '')
                    date = entry.get('date', '')
                    
                    new_id, needs_fix = extract_existing_components(old_id, date)
                    
                    if needs_fix:
                        entry['id'] = new_id
                        fixed_count += 1
                        if len(examples) < 3:
                            examples.append((old_id, new_id))
        
        if fixed_count > 0:
            # Show examples
            for old, new in examples:
                print(f"  ✓ {old} -> {new}")
            if fixed_count > 3:
                print(f"  ... and {fixed_count - 3} more")
            
            # Write back
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  ✅ Fixed {fixed_count} entries")
                total_fixed += fixed_count
            except Exception as e:
                print(f"  ❌ Error writing: {str(e)}")
        else:
            print(f"  ℹ️  No changes needed (all IDs already include date)")
    
    print()
    print("=" * 80)
    print(f"TOTAL FIXES: {total_fixed} entries across all files")
    print("=" * 80)
    
    return total_fixed


if __name__ == "__main__":
    total = fix_all_files()
    print(f"\n✅ Fixed {total} additional entries in EN, ES, PT, FR files")
