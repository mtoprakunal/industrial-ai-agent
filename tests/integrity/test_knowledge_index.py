"""
test_knowledge_index.py
knowledge/_index.json butunlugu: yapi, seviyeler, domain dizin varligi.
"""
import re
import unittest

from _common import (load_index, iter_leaves, KNOWLEDGE,
                     SEVIYELER, KATEGORILER)


class TestKnowledgeIndex(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.index = load_index()

    def test_index_valid_json_with_required_keys(self):
        for key in ('version', 'maturity_levels', 'last_updated', 'domains'):
            self.assertIn(key, self.index, f"_index.json '{key}' anahtari eksik")

    def test_maturity_levels_match_canonical(self):
        self.assertEqual(self.index['maturity_levels'], SEVIYELER,
                         "maturity_levels kanonik SEVIYELER listesiyle eslesmiyor")

    def test_last_updated_is_iso_date(self):
        self.assertRegex(self.index['last_updated'], r'^\d{4}-\d{2}-\d{2}$',
                         "last_updated YYYY-MM-DD formatinda degil")

    def test_all_domains_are_known_categories(self):
        for dom in self.index['domains']:
            self.assertIn(dom, KATEGORILER, f"Bilinmeyen domain: {dom}")

    def test_every_leaf_has_valid_seviye(self):
        leaves = list(iter_leaves(self.index))
        self.assertGreater(len(leaves), 0, "Index'te hic leaf konu yok")
        for path, leaf in leaves:
            self.assertIn(leaf['seviye'], SEVIYELER,
                          f"{'/'.join(path)} gecersiz seviye: {leaf['seviye']}")

    def test_every_domain_directory_exists(self):
        for dom in self.index['domains']:
            self.assertTrue((KNOWLEDGE / dom).is_dir(),
                            f"Domain dizini diskte yok: knowledge/{dom}/")

    def test_subcategory_directories_exist(self):
        # Leaf olmayan (alt-kategori) dugumlerin dizini diskte olmali
        for dom, node in self.index['domains'].items():
            for k, v in node.items():
                if k == 'description' or not isinstance(v, dict):
                    continue
                if 'seviye' in v:
                    continue  # leaf — dosya testi ayri modulde
                self.assertTrue((KNOWLEDGE / dom / k).is_dir(),
                                f"Alt-kategori dizini yok: knowledge/{dom}/{k}/")


if __name__ == '__main__':
    unittest.main()
