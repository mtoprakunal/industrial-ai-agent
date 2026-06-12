# CODESYS MCP Sunucusu

CODESYS proje üretimi ve script engine otomasyonu için MCP araç katmanı.
Spec'ten proje iskeleti, PLCopen XML üretimi ve derleme doğrulaması.

> **Durum:** STUB — araçlar listelenir, çağrılar `[STUB]` döndürür.

## Araçlar

| Araç | Açıklama |
|------|----------|
| `codesys_generate_project` | Spec'ten proje iskeleti (task/GVL/FB) |
| `codesys_list_pous` | POU listele (Program/FB/Function) |
| `codesys_generate_plcopen_xml` | ST → PLCopen XML |
| `codesys_run_script` | Script engine (IronPython) komutu |
| `codesys_compile_check` | Derleme/sözdizimi doğrulaması |

## İmplementasyon Notları (sonraki adım)

- Üretim formatları: `st_source` (varsayılan), `plcopen_xml`, `script_engine`
  (`rules.json` → `project_output.generation_formats`).
- Script engine, CODESYS kurulumuyla birlikte gelen IronPython arayüzüdür;
  headless üretim için `CODESYS.exe --runscript` çağrılabilir.
- Şablonlar: `/templates/codesys/` (plcopen-xml, project-scripts, st-snippets).
- Doğrulama agent'ın `quality_checklist.md` kriterleriyle örtüşmeli.

## İlgili Bilgi Tabanı

- `/knowledge/codesys/project-generation/` (Uzman seviye)
- `/knowledge/codesys/programming/`, `/knowledge/codesys/task-structure/`
- `/templates/codesys/`
