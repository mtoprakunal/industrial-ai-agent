"""
_common.py
Integrity testleri icin ortak yol sabitleri ve yardimcilar.
"""
import json
from pathlib import Path

REPO       = Path(__file__).resolve().parents[2]
KNOWLEDGE  = REPO / 'knowledge'
INDEX      = KNOWLEDGE / '_index.json'
GRAPH      = KNOWLEDGE / '_graph.json'
TEMPLATE   = KNOWLEDGE / '_template.md'
RULES      = REPO / 'agent' / 'rules.json'

SEVIYELER  = ['Stub', 'Temel', 'Orta', 'İleri', 'Uzman']
KATEGORILER = ['protocols', 'codesys', 'hmi', 'hardware',
               'networking', 'standards', 'applications', 'decisions',
               'inovance', 'examples', 'safety']

DEVICES_INDEX = REPO / 'devices' / '_index.json'


def load_index():
    return json.loads(INDEX.read_text())


def device_paths():
    """devices/_index.json'daki cihaz dizinlerini 'devices/<dir>' seti olarak verir
    (graph'ta cihaz kütüphanesine cross-referans kenarlarını çözmek için)."""
    if not DEVICES_INDEX.exists():
        return set()
    idx = json.loads(DEVICES_INDEX.read_text())
    return {f"devices/{d['dir']}" for d in idx.get('devices', [])}


def load_graph():
    return json.loads(GRAPH.read_text())


def content_docs():
    """Icerik belgeleri: _ ile baslamayan tum .md dosyalari (README dahil)."""
    return [p for p in KNOWLEDGE.rglob('*.md') if not p.name.startswith('_')]


def iter_leaves(index):
    """
    Index'teki her leaf konuyu (path_parcalari, leaf_dict) olarak uretir.
    Leaf = 'seviye' anahtari iceren dict.
    """
    def walk(node, path):
        if not isinstance(node, dict):
            return
        if 'seviye' in node:
            yield path, node
            return
        for k, v in node.items():
            if k == 'description':
                continue
            if isinstance(v, dict):
                yield from walk(v, path + [k])
    for dom, node in index.get('domains', {}).items():
        yield from walk(node, [dom])
