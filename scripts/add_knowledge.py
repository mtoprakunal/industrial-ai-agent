#!/usr/bin/env python3
"""
add_knowledge.py
Yeni bilgi belgesi oluşturmak için yardımcı araç.
Kullanım: python scripts/add_knowledge.py
"""
import os, json, datetime
from pathlib import Path

BASE     = Path(__file__).parent.parent
TEMPLATE = BASE / 'knowledge' / '_template.md'
INDEX    = BASE / 'knowledge' / '_index.json'

KATEGORILER = ['protocols', 'codesys', 'hmi', 'hardware', 'networking', 'standards', 'applications', 'decisions']
SEVIYELER   = ['Stub', 'Temel', 'Orta', 'İleri', 'Uzman']

def main():
    print("\n=== Yeni Bilgi Belgesi Oluştur ===\n")
    konu     = input("Konu adı: ").strip()
    print(f"Kategori seçin: {', '.join(KATEGORILER)}")
    kategori = input("Kategori: ").strip()
    alt      = input("Alt kategori (boş bırakılabilir): ").strip()
    print(f"Seviye seçin: {', '.join(SEVIYELER)}")
    seviye   = input("Seviye [Stub]: ").strip() or 'Stub'
    dosya    = input("Dosya adı (örn: 01_konu.md): ").strip()

    path_parts = ['knowledge', kategori]
    if alt:
        path_parts.append(alt)
    path_parts.append(dosya)

    full_path = BASE / '/'.join(path_parts)
    full_path.parent.mkdir(parents=True, exist_ok=True)

    template = TEMPLATE.read_text()
    content = template.replace('[Konunun adı]', konu)
    content = content.replace('[protocols | codesys | hmi | hardware | networking | standards | applications | decisions]', kategori)
    content = content.replace('[Stub | Temel | Orta | İleri | Uzman]', seviye)
    content = content.replace('[YYYY-MM-DD]', datetime.date.today().isoformat())

    full_path.write_text(content)
    print(f"\nBelge oluşturuldu: {full_path}")
    print("_index.json ve _graph.json dosyalarını güncellemeyi unutma!")

if __name__ == '__main__':
    main()
