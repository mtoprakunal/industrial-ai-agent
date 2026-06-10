#!/usr/bin/env python3
"""
add_knowledge.py
Yeni bilgi belgesi olusturur VE _index.json'u otomatik gunceller.

Kullanim (interaktif):
    python scripts/add_knowledge.py

Kullanim (non-interaktif / scriptlenebilir):
    python scripts/add_knowledge.py \
        --konu "OPC-UA Alarmlari" --kategori protocols --alt opc-ua \
        --dosya 07_alarms.md --seviye Temel

Notlar:
- _index.json otomatik guncellenir (leaf konu eklenir, last_updated bugune cekilir).
- _graph.json BAGLANTILARI ELLE eklenmelidir: kenarlar (edge) iliski yorumu
  gerektirir, otomatiklestirilemez. Script eklenmesi gereken kenarlari hatirlatir.
"""
import sys
import json
import argparse
import datetime
from pathlib import Path

BASE     = Path(__file__).parent.parent
TEMPLATE = BASE / 'knowledge' / '_template.md'
INDEX    = BASE / 'knowledge' / '_index.json'

KATEGORILER = ['protocols', 'codesys', 'hmi', 'hardware',
               'networking', 'standards', 'applications', 'decisions',
               'inovance', 'examples', 'safety']
SEVIYELER   = ['Stub', 'Temel', 'Orta', 'İleri', 'Uzman']


# --------------------------------------------------------------------------
# Saf (yan etkisiz) yardimcilar — testlerden dogrudan cagrilabilir
# --------------------------------------------------------------------------
def topic_key(dosya):
    """Dosya adindan index anahtarini cikarir: '01_basics.md' -> '01_basics'."""
    name = dosya.strip()
    if name.endswith('.md'):
        name = name[:-3]
    return name


def render_template(template_text, konu, kategori, seviye, today=None):
    """Sablon metnini verilen alanlarla doldurur (dosyaya yazmaz)."""
    today = today or datetime.date.today().isoformat()
    content = template_text.replace('[Konunun adı]', konu)
    content = content.replace(
        '[protocols | codesys | hmi | hardware | networking | standards | applications | decisions]',
        kategori)
    content = content.replace('[Stub | Temel | Orta | İleri | Uzman]', seviye)
    content = content.replace('[YYYY-MM-DD]', today)
    return content


def insert_topic(index, kategori, alt, key, konu, seviye, today=None):
    """
    index sozlugune (yerinde) yeni leaf konu ekler veya gunceller.
    domains[kategori]  (alt yoksa)        -> { key: {seviye, başlık} }
    domains[kategori][alt] (alt varsa)    -> { key: {seviye, başlık} }
    last_updated bugune cekilir.

    Donus: 'added' | 'updated'  (konu yeni mi yoksa mevcut mu).
    ValueError: kategori/seviye gecersizse.
    """
    if kategori not in KATEGORILER:
        raise ValueError(f"Gecersiz kategori: {kategori!r}. Gecerli: {KATEGORILER}")
    if seviye not in SEVIYELER:
        raise ValueError(f"Gecersiz seviye: {seviye!r}. Gecerli: {SEVIYELER}")

    today = today or datetime.date.today().isoformat()
    domains = index.setdefault('domains', {})
    domain = domains.setdefault(kategori, {'description': kategori})

    # Hedef kapsayici: alt-kategori varsa onun altina, yoksa dogrudan domain'e
    container = domain
    if alt:
        sub = domain.get(alt)
        if not isinstance(sub, dict):
            sub = {}
            domain[alt] = sub
        container = sub

    leaf = {'seviye': seviye, 'başlık': konu}
    action = 'updated' if key in container else 'added'
    container[key] = leaf
    index['last_updated'] = today
    return action


# --------------------------------------------------------------------------
# Dosya islemleri (yan etkili)
# --------------------------------------------------------------------------
def doc_path(kategori, alt, dosya):
    parts = ['knowledge', kategori]
    if alt:
        parts.append(alt)
    parts.append(dosya)
    return BASE / '/'.join(parts)


def create_knowledge(konu, kategori, alt, dosya, seviye, force=False, today=None):
    """
    .md belgesini olusturur ve _index.json'u gunceller.
    Donus: (md_path, index_action)
    """
    today = today or datetime.date.today().isoformat()
    key = topic_key(dosya)

    path = doc_path(kategori, alt, dosya)
    if path.exists() and not force:
        raise FileExistsError(
            f"Belge zaten var: {path}\n  Uzerine yazmak icin --force kullanin.")

    # 1) .md belgesi
    template_text = TEMPLATE.read_text()
    content = render_template(template_text, konu, kategori, seviye, today)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)

    # 2) _index.json
    index = json.loads(INDEX.read_text())
    action = insert_topic(index, kategori, alt, key, konu, seviye, today)
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')

    return path, action


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def prompt_interactive():
    print("\n=== Yeni Bilgi Belgesi Olustur ===\n")
    konu = input("Konu adi: ").strip()
    print(f"Kategori secin: {', '.join(KATEGORILER)}")
    kategori = input("Kategori: ").strip()
    alt = input("Alt kategori (bos birakilabilir): ").strip()
    print(f"Seviye secin: {', '.join(SEVIYELER)}")
    seviye = input("Seviye [Stub]: ").strip() or 'Stub'
    dosya = input("Dosya adi (orn: 01_konu.md): ").strip()
    return konu, kategori, alt, dosya, seviye


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Yeni bilgi belgesi olustur ve _index.json'u guncelle.")
    parser.add_argument('--konu')
    parser.add_argument('--kategori', choices=KATEGORILER)
    parser.add_argument('--alt', default='')
    parser.add_argument('--dosya')
    parser.add_argument('--seviye', choices=SEVIYELER, default='Stub')
    parser.add_argument('--force', action='store_true',
                        help="Mevcut belgenin uzerine yaz.")
    args = parser.parse_args(argv)

    # Zorunlu alanlar verilmemisse interaktif moda dus
    if not (args.konu and args.kategori and args.dosya):
        konu, kategori, alt, dosya, seviye = prompt_interactive()
        force = args.force
    else:
        konu, kategori, alt, dosya, seviye, force = (
            args.konu, args.kategori, args.alt, args.dosya, args.seviye, args.force)

    try:
        path, action = create_knowledge(konu, kategori, alt, dosya, seviye, force=force)
    except (ValueError, FileExistsError) as e:
        print(f"\nHATA: {e}")
        return 1

    rel = path.relative_to(BASE)
    fiil = "eklendi" if action == 'added' else "guncellendi"
    print(f"\n  [OK] Belge olusturuldu : {rel}")
    print(f"  [OK] _index.json       : konu {fiil} ({kategori}"
          f"{'/' + alt if alt else ''}/{topic_key(dosya)} = {seviye})")
    print("\n  HATIRLATMA: _graph.json kenarlarini (BAGLANTILAR) elle ekleyin —")
    print("  iliski tipi (gerektirir/kullanir/alternatif/tamamlar/detaylandirir)")
    print("  insan yargisi gerektirir, otomatiklestirilemez.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
