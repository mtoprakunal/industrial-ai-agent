"""
test_graph.py
knowledge/_graph.json butunlugu: yapi, iliski tipleri, kenar hedeflerinin gecerliligi.
"""
import unittest

from _common import load_graph, load_index, iter_leaves


def index_topic_paths(index):
    """Index'teki tum konu yollarini 'domain/sub/key' string seti olarak verir."""
    paths = set()
    for path, _ in iter_leaves(index):
        # _synthesis leaf'i 'domain/sub/_synthesis' ve aile koku 'domain/sub' uretir
        full = '/'.join(path)
        paths.add(full)
        if path[-1] == '_synthesis':
            paths.add('/'.join(path[:-1]))
    return paths


class TestGraph(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.graph = load_graph()
        cls.valid_paths = index_topic_paths(load_index())

    def test_graph_has_required_keys(self):
        for key in ('relationship_types', 'edges'):
            self.assertIn(key, self.graph, f"_graph.json '{key}' anahtari eksik")

    def test_edges_have_required_fields(self):
        for i, edge in enumerate(self.graph['edges']):
            for field in ('from', 'to', 'ilişki'):
                self.assertIn(field, edge, f"Kenar #{i}: '{field}' alani eksik")

    def test_edge_relationship_types_are_defined(self):
        defined = set(self.graph['relationship_types'].keys())
        for i, edge in enumerate(self.graph['edges']):
            self.assertIn(edge['ilişki'], defined,
                          f"Kenar #{i}: tanimsiz iliski tipi -> {edge['ilişki']}")

    def test_edge_endpoints_resolve_to_index_topics(self):
        # Her from/to ya tam bir konu yolu ya da gecerli bir konu ailesi (prefix) olmali.
        for i, edge in enumerate(self.graph['edges']):
            for side in ('from', 'to'):
                target = edge[side]
                ok = (target in self.valid_paths or
                      any(p == target or p.startswith(target + '/') or
                          target.startswith(p + '/') for p in self.valid_paths))
                self.assertTrue(
                    ok, f"Kenar #{i} '{side}': index'te bulunamayan hedef -> {target}")


if __name__ == '__main__':
    unittest.main()
