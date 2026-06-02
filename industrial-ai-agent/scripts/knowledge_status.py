#!/usr/bin/env python3
"""
knowledge_status.py
Bilgi tabanının olgunluk seviyelerini gösterir.
Kullanım: python scripts/knowledge_status.py
"""
import json
from pathlib import Path

INDEX = Path(__file__).parent.parent / 'knowledge' / '_index.json'

SEVIYE_RENK = {
    'Stub'  : '\033[90m',   # gri
    'Temel' : '\033[33m',   # sarı
    'Orta'  : '\033[36m',   # cyan
    'İleri' : '\033[34m',   # mavi
    'Uzman' : '\033[32m',   # yeşil
}
RESET = '\033[0m'

def print_domain(name, data, indent=0):
    pad = '  ' * indent
    if isinstance(data, dict):
        seviye = data.get('seviye', '')
        baslik = data.get('başlık', name)
        if seviye:
            renk = SEVIYE_RENK.get(seviye, '')
            print(f"{pad}{renk}[{seviye:6}]{RESET}  {baslik}")
        for k, v in data.items():
            if k not in ('seviye', 'başlık', 'açıklama', 'description'):
                if isinstance(v, dict):
                    print(f"{pad}  /{k}")
                    print_domain(k, v, indent + 2)

def main():
    data = json.loads(INDEX.read_text())
    print(f"\n{'='*60}")
    print(f"  BİLGİ TABANI DURUM RAPORU")
    print(f"{'='*60}\n")

    counts = {'Stub': 0, 'Temel': 0, 'Orta': 0, 'İleri': 0, 'Uzman': 0}

    def count_stubs(d):
        if isinstance(d, dict):
            s = d.get('seviye')
            if s in counts:
                counts[s] += 1
            for v in d.values():
                count_stubs(v)

    count_stubs(data['domains'])

    total = sum(counts.values())
    filled = total - counts['Stub']
    print(f"  Toplam konu: {total}")
    print(f"  Doldurulmuş: {filled} ({int(filled/total*100)}%)\n")
    for s, c in counts.items():
        renk = SEVIYE_RENK.get(s, '')
        bar = '█' * c
        print(f"  {renk}{s:6}{RESET}  {bar} ({c})")

    print(f"\n{'='*60}")
    print("  DOMAIN DETAYI")
    print(f"{'='*60}\n")
    for domain, content in data['domains'].items():
        print(f"\n  [{domain.upper()}]")
        print_domain(domain, content, 2)
    print()

if __name__ == '__main__':
    main()
