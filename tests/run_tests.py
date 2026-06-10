#!/usr/bin/env python3
"""
run_tests.py
Tum otomatik butunluk (integrity) testlerini calistirir. Sifir bagimlilik (stdlib unittest).

Kullanim:
    python tests/run_tests.py            # tum integrity testleri
    python tests/run_tests.py -v         # ayrintili

Bu runner agent'in BEYNINI ve BILGI TABANINI tutarli tutan degismezleri dogrular:
- knowledge/_index.json gecerli, seviyeler tanimli, domain'ler diskte var
- her bilgi belgesi _template.md frontmatter formatina uyuyor
- knowledge/_graph.json kenarlari gercek konulara isaret ediyor
- agent/rules.json yapisi ve kritik emniyet/timing kurallari yerinde
- scripts/add_knowledge.py mantigi dogru calisiyor

Davranissal senaryolar (tests/scenarios/) burada calismaz — onlar agent'in
kalitesini niteliksel degerlendirmek icindir; bkz. tests/scenarios/README.md.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parent


def main():
    # scripts/ paket degil; add_knowledge importu icin yola ekle
    sys.path.insert(0, str(REPO / 'scripts'))
    sys.path.insert(0, str(HERE))

    verbosity = 2 if '-v' in sys.argv else 1
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(HERE / 'integrity'),
                            pattern='test_*.py',
                            top_level_dir=str(HERE / 'integrity'))
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
