"""
test_add_knowledge.py
scripts/add_knowledge.py mantigi: saf fonksiyonlar + gercek dosya/index entegrasyonu.
Entegrasyon testi GERCEK index'e dokunmaz — gecici bir kopya uzerinde calisir.
"""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import add_knowledge as ak  # runner scripts/ dizinini yola ekler
from _common import INDEX as REAL_INDEX, TEMPLATE as REAL_TEMPLATE


class TestPureFunctions(unittest.TestCase):

    def test_topic_key_strips_md(self):
        self.assertEqual(ak.topic_key('01_basics.md'), '01_basics')
        self.assertEqual(ak.topic_key('01_basics'), '01_basics')
        self.assertEqual(ak.topic_key('  conveyor.md '), 'conveyor')

    def test_render_template_fills_placeholders(self):
        tmpl = ("KONU        : [Konunun adı]\n"
                "KATEGORİ    : [protocols | codesys | hmi | hardware | "
                "networking | standards | applications | decisions]\n"
                "SEVİYE      : [Stub | Temel | Orta | İleri | Uzman]\n"
                "SON_GÜNCELLEME: [YYYY-MM-DD]\n")
        out = ak.render_template(tmpl, 'Test Konu', 'protocols', 'Temel',
                                 today='2026-06-10')
        self.assertIn('Test Konu', out)
        self.assertIn('protocols', out)
        self.assertIn('Temel', out)
        self.assertIn('2026-06-10', out)
        self.assertNotIn('[Konunun adı]', out)
        self.assertNotIn('[YYYY-MM-DD]', out)

    def test_insert_topic_adds_leaf_without_subcat(self):
        index = {'domains': {'standards': {'description': 'x'}}, 'last_updated': '2000-01-01'}
        action = ak.insert_topic(index, 'standards', '', '04_isa95',
                                 'ISA-95', 'Stub', today='2026-06-10')
        self.assertEqual(action, 'added')
        self.assertEqual(index['domains']['standards']['04_isa95'],
                         {'seviye': 'Stub', 'başlık': 'ISA-95'})
        self.assertEqual(index['last_updated'], '2026-06-10')

    def test_insert_topic_adds_leaf_with_subcat(self):
        index = {'domains': {'protocols': {'description': 'x'}}}
        ak.insert_topic(index, 'protocols', 'opc-ua', '07_alarms',
                        'OPC-UA Alarmlari', 'Temel')
        self.assertEqual(index['domains']['protocols']['opc-ua']['07_alarms']['seviye'],
                         'Temel')

    def test_insert_topic_update_vs_add(self):
        index = {'domains': {'standards': {}}}
        self.assertEqual(ak.insert_topic(index, 'standards', '', 'k', 'K', 'Stub'), 'added')
        self.assertEqual(ak.insert_topic(index, 'standards', '', 'k', 'K', 'Uzman'), 'updated')
        self.assertEqual(index['domains']['standards']['k']['seviye'], 'Uzman')

    def test_insert_topic_rejects_bad_category(self):
        with self.assertRaises(ValueError):
            ak.insert_topic({'domains': {}}, 'bogus', '', 'k', 'K', 'Stub')

    def test_insert_topic_rejects_bad_level(self):
        with self.assertRaises(ValueError):
            ak.insert_topic({'domains': {}}, 'standards', '', 'k', 'K', 'SuperUzman')


class TestIntegration(unittest.TestCase):
    """Gercek index'in kopyasi uzerinde create_knowledge() ucu-uca."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='ak_test_'))
        kdir = self.tmp / 'knowledge'
        kdir.mkdir()
        # Gercek sablon ve index'i kopyala
        shutil.copy(REAL_TEMPLATE, kdir / '_template.md')
        shutil.copy(REAL_INDEX, kdir / '_index.json')
        # Modul globallerini gecici repoya yonlendir
        self._saved = (ak.BASE, ak.INDEX, ak.TEMPLATE)
        ak.BASE = self.tmp
        ak.INDEX = kdir / '_index.json'
        ak.TEMPLATE = kdir / '_template.md'

    def tearDown(self):
        ak.BASE, ak.INDEX, ak.TEMPLATE = self._saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_create_writes_doc_and_updates_index(self):
        before = json.loads(ak.INDEX.read_text())
        n_before = sum(1 for _ in _leaves(before))

        path, action = ak.create_knowledge(
            'Sparkplug B', 'protocols', 'mqtt', '03_sparkplug.md', 'Temel',
            today='2026-06-10')

        self.assertEqual(action, 'added')
        self.assertTrue(path.exists(), "Belge dosyasi olusturulmadi")
        doc = path.read_text()
        self.assertIn('Sparkplug B', doc)
        self.assertIn('Temel', doc)

        after = json.loads(ak.INDEX.read_text())
        self.assertEqual(after['domains']['protocols']['mqtt']['03_sparkplug'],
                         {'seviye': 'Temel', 'başlık': 'Sparkplug B'})
        self.assertEqual(after['last_updated'], '2026-06-10')
        self.assertEqual(sum(1 for _ in _leaves(after)), n_before + 1,
                         "Index leaf sayisi tam olarak 1 artmadi")

    def test_refuses_overwrite_without_force(self):
        ak.create_knowledge('A', 'standards', '', '09_x.md', 'Stub', today='2026-06-10')
        with self.assertRaises(FileExistsError):
            ak.create_knowledge('A', 'standards', '', '09_x.md', 'Stub', today='2026-06-10')
        # force ile gecmeli
        path, _ = ak.create_knowledge('A2', 'standards', '', '09_x.md', 'Orta',
                                      force=True, today='2026-06-10')
        self.assertIn('A2', path.read_text())


def _leaves(index):
    def walk(node):
        if not isinstance(node, dict):
            return
        if 'seviye' in node:
            yield node
            return
        for k, v in node.items():
            if k == 'description':
                continue
            yield from walk(v)
    for node in index.get('domains', {}).values():
        yield from walk(node)


if __name__ == '__main__':
    unittest.main()
