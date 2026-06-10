# Tests

İki tür test içerir:

## 1. `integrity/` — Otomatik Bütünlük Testleri

Bilgi tabanının ve agent beyninin yapısal değişmezlerini doğrular. **Sıfır bağımlılık**
(stdlib `unittest`).

```bash
python tests/run_tests.py        # tümünü çalıştır
python tests/run_tests.py -v     # ayrıntılı
```

Neyi garanti eder:

| Modül | Doğruladığı |
|-------|-------------|
| `test_knowledge_index.py` | `_index.json` yapısı, seviyeler, domain/alt-kategori dizinlerinin diskte varlığı |
| `test_knowledge_docs.py` | Her belge `_template.md` frontmatter formatına uyuyor + index↔belge sayı tutarlılığı |
| `test_graph.py` | `_graph.json` kenarları tanımlı ilişki tipi kullanıyor ve gerçek konulara işaret ediyor |
| `test_rules.py` | `agent/rules.json` yapısı + ihlal edilemez emniyet/timing kurallarının yerinde olması |
| `test_add_knowledge.py` | `scripts/add_knowledge.py` mantığı (saf fonksiyonlar + geçici index üzerinde uçtan uca) |

> Bu testler `agent/rules.json`'daki emniyet kurallarının veya bilgi tabanı tutarlılığının
> sessizce bozulmasını yakalar. Yeni bilgi belgesi eklerken bunları çalıştır — `_index.json`
> ile diskin uyumsuzluğunu anında görürsün.

## 2. `scenarios/` — Agent Davranış Senaryoları

Agent'ın akıl yürütme kalitesini değerlendiren, insan/LLM-judge ile okunmak üzere
hazırlanmış senaryolar (otomatik koşmaz). Detay: [`scenarios/README.md`](scenarios/README.md).
