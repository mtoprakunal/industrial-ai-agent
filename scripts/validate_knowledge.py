#!/usr/bin/env python3
"""
validate_knowledge.py
Bilgi belgelerinin _template.md formatına uygunluğunu kontrol eder.
Kullanım: python scripts/validate_knowledge.py
"""
import os
from pathlib import Path

BASE = Path(__file__).parent.parent / 'knowledge'
REQUIRED_FIELDS = ['KONU', 'KATEGORI', 'SEVIYE', 'SON_GÜNCELLEME']

def validate_file(path):
    errors = []
    content = path.read_text()
    if not content.startswith('---'):
        errors.append("Frontmatter (---) eksik")
        return errors
    for field in REQUIRED_FIELDS:
        if field not in content:
            errors.append(f"Zorunlu alan eksik: {field}")
    return errors

def main():
    total, failed = 0, 0
    for md in BASE.rglob('*.md'):
        if md.name.startswith('_'):
            continue
        total += 1
        errors = validate_file(md)
        if errors:
            failed += 1
            rel = md.relative_to(BASE)
            print(f"\nHATA: {rel}")
            for e in errors:
                print(f"  • {e}")

    print(f"\n{'='*50}")
    print(f"Toplam: {total} belge | Hatalı: {failed} | Geçerli: {total-failed}")

if __name__ == '__main__':
    main()
