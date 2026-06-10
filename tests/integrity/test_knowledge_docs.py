"""
test_knowledge_docs.py
Her bilgi belgesi _template.md frontmatter formatina uyuyor mu + index ile sayi tutarliligi.
Bu, scripts/validate_knowledge.py mantiginin otomatik test karsiligidir.
"""
import re
import unittest

from _common import (content_docs, load_index, iter_leaves,
                     TEMPLATE, SEVIYELER)

REQUIRED_FIELDS = ['KONU', 'KATEGORİ', 'SEVİYE', 'SON_GÜNCELLEME']
SEVIYE_RE = re.compile(r'^SEVİYE\s*:\s*(.+?)\s*$', re.MULTILINE)


class TestKnowledgeDocs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.docs = content_docs()
        cls.index = load_index()

    def test_docs_exist(self):
        self.assertGreater(len(self.docs), 0, "Hic icerik belgesi bulunamadi")

    def test_template_uses_turkish_fields(self):
        # Sablonun kendisi de zorunlu alanlari Turkce karakterle icermeli
        tmpl = TEMPLATE.read_text()
        for field in REQUIRED_FIELDS:
            self.assertIn(field, tmpl, f"_template.md '{field}' alanini icermiyor")

    def test_every_doc_has_frontmatter_and_required_fields(self):
        for doc in self.docs:
            content = doc.read_text()
            rel = doc.relative_to(TEMPLATE.parent)
            self.assertTrue(content.startswith('---'),
                            f"{rel}: frontmatter (---) ile baslamiyor")
            for field in REQUIRED_FIELDS:
                self.assertIn(field, content,
                              f"{rel}: zorunlu alan eksik -> {field}")

    def test_every_doc_seviye_is_valid(self):
        for doc in self.docs:
            content = doc.read_text()
            rel = doc.relative_to(TEMPLATE.parent)
            m = SEVIYE_RE.search(content)
            self.assertIsNotNone(m, f"{rel}: SEVİYE satiri okunamadi")
            self.assertIn(m.group(1), SEVIYELER,
                          f"{rel}: gecersiz SEVİYE -> {m.group(1)}")

    def test_doc_count_matches_indexed_topics(self):
        # Degismez: index'teki _synthesis olmayan leaf sayisi == icerik belgesi sayisi.
        # (Her belgelenmis konu indekslenir, her indekslenen konu belgelenir.)
        indexed = [p for p, _ in iter_leaves(self.index) if p[-1] != '_synthesis']
        self.assertEqual(
            len(indexed), len(self.docs),
            f"Index'teki konu sayisi ({len(indexed)}) ile belge sayisi "
            f"({len(self.docs)}) uyusmuyor — biri digerinde eksik/fazla.")


if __name__ == '__main__':
    unittest.main()
