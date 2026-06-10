#!/usr/bin/env python3
"""
validate_datasheet.py
devices/*/datasheet.json dosyalarini agent/datasheet_schema.json'a gore dogrular.
Sifir bagimlilik (stdlib) — JSON Schema'nin alt kumesini destekler:
type, required, properties, items, enum, additionalProperties, minItems.

Kullanim:
    python scripts/validate_datasheet.py                 # tum cihazlar
    python scripts/validate_datasheet.py devices/PENKO_SGM820/datasheet.json
"""
import sys
import json
from pathlib import Path

BASE   = Path(__file__).parent.parent
SCHEMA = BASE / 'agent' / 'datasheet_schema.json'
DEVICES = BASE / 'devices'

_JSON_TYPES = {
    'object': dict, 'array': list, 'string': str,
    'number': (int, float), 'integer': int, 'boolean': bool, 'null': type(None),
}


def _type_ok(value, type_spec):
    types = type_spec if isinstance(type_spec, list) else [type_spec]
    for t in types:
        py = _JSON_TYPES.get(t)
        if py is None:
            continue
        # bool int'in alt sinifi; integer/number icin bool'u disla
        if t in ('integer', 'number') and isinstance(value, bool):
            continue
        if isinstance(value, py):
            return True
    return False


def validate(value, schema, path, errors):
    # type
    if 'type' in schema and not _type_ok(value, schema['type']):
        errors.append(f"{path}: tip hatali (beklenen {schema['type']}, gelen {type(value).__name__})")
        return  # tip yanlissa derine inme

    # enum (None degeri enum'da acikca varsa gecerli)
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f"{path}: gecersiz deger {value!r} (izinli: {schema['enum']})")

    if isinstance(value, dict):
        props = schema.get('properties', {})
        for req in schema.get('required', []):
            if req not in value:
                errors.append(f"{path}: zorunlu alan eksik -> {req}")
        if schema.get('additionalProperties') is False:
            for k in value:
                if k not in props:
                    errors.append(f"{path}: izin verilmeyen alan -> {k}")
        for k, v in value.items():
            if k in props:
                validate(v, props[k], f"{path}.{k}", errors)

    elif isinstance(value, list):
        if 'minItems' in schema and len(value) < schema['minItems']:
            errors.append(f"{path}: en az {schema['minItems']} eleman gerekli (gelen {len(value)})")
        item_schema = schema.get('items')
        if item_schema:
            for i, item in enumerate(value):
                validate(item, item_schema, f"{path}[{i}]", errors)


def validate_file(path, schema):
    try:
        data = json.loads(Path(path).read_text())
    except json.JSONDecodeError as e:
        return [f"{path}: gecersiz JSON -> {e}"]
    errors = []
    validate(data, schema, Path(path).parent.name, errors)
    return errors


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    schema = json.loads(SCHEMA.read_text())

    if argv:
        targets = [Path(a) for a in argv]
    else:
        targets = sorted(DEVICES.glob('*/datasheet.json'))

    if not targets:
        print("Dogrulanacak datasheet.json bulunamadi.")
        return 0

    total, failed = 0, 0
    for t in targets:
        total += 1
        errors = validate_file(t, schema)
        try:
            rel = t.resolve().relative_to(BASE)
        except ValueError:
            rel = t
        if errors:
            failed += 1
            print(f"\nHATA: {rel}")
            for e in errors:
                print(f"  • {e}")
        else:
            print(f"OK: {rel}")

    print(f"\n{'='*50}")
    print(f"Toplam: {total} | Hatali: {failed} | Gecerli: {total - failed}")
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
