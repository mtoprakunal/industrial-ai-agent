# -*- coding: utf-8 -*-
"""
create_basic_structure.py — Bos projede temel CODESYS yapisi olusturur.

NE YAPAR
    Acik bir CODESYS projesinde Application altinda:
      * Task konfigurasyonu: Fast (2ms), Control (10ms), Slow (100ms)
      * GVL_IO     (fiziksel giris/cikis degiskenleri)
      * GVL_Const  (sabitler / konfigurasyon)
      * MAIN       (PROGRAM PRG, kontrol dongusu iskeleti)
    olusturur ve task'lara MAIN'i baglar.
    Idempotent: var olan nesneler atlanir, kullaniciya loglanir.

NASIL CALISTIRILIR
    CODESYS IDE icinde:
      1. Bos / sablon proje ac.
      2. Tools > Scripting > Execute Script File...
      3. Bu dosyayi sec.

IRONPYTHON 2.7 UYUMU
    from __future__ import print_function ile print() fonksiyon stili.
    Script Engine global'leri (projects, PouType, system) fonksiyon
    govdesinde, guard'li kullanilir; bu sayede CPython'da
    py_compile sozdizimi denetimi sorunsuz gecer.

NOT — TASK API
    CODESYS task olusturma API'si surume gore degisir. Task Configuration
    nesnesi uzerinde dogrudan "create_task" her surumde olmayabilir; bu
    yuzden once mevcut task aranir, bulunamazsa create_task denenir ve
    basarisiz olursa kullaniciya manuel adim onerilir (asagidaki
    _ensure_task'a bakin). Cycle araliklari mikrosaniye cinsindendir.
"""
from __future__ import print_function

import sys


# Task tanimlari: ad, cycle (ms), oncelik (kucuk = yuksek oncelik).
TASK_DEFS = [
    {"name": "Task_Fast",    "interval_ms": 2,   "priority": 1},
    {"name": "Task_Control", "interval_ms": 10,  "priority": 5},
    {"name": "Task_Slow",    "interval_ms": 100, "priority": 10},
]


# --- GVL ve PRG iskelet icerikleri (ST) ---

GVL_IO_DECL = """// ============================================================
// GVL_IO — Fiziksel Giris/Cikis degiskenleri
// Bu dosya bir iskelettir; gercek I/O icin generate_gvl_from_io.py kullanin.
// ============================================================
{attribute 'qualified_only'}
VAR_GLOBAL
    // --- Dijital Girisler (DI) ---
    // ZN1_PBS_01_Start AT %IX0.0 : BOOL;

    // --- Dijital Cikislar (DO) ---
    // ZN1_MTR_01_Run   AT %QX0.0 : BOOL;

    // --- Analog Girisler (AI) ---
    // ZN1_TAC_01_Speed AT %IW0   : INT;
END_VAR
"""

GVL_CONST_DECL = """// ============================================================
// GVL_Const — Sabitler ve konfigurasyon degerleri
// VAR_GLOBAL CONSTANT: derleme aninda sabit, runtime'da degismez.
// ============================================================
{attribute 'qualified_only'}
VAR_GLOBAL CONSTANT
    // Cycle / zaman sabitleri
    cFastCycle    : TIME := T#2MS;
    cControlCycle : TIME := T#10MS;
    cSlowCycle    : TIME := T#100MS;

    // Olcekleme ornekleri
    cAnalogRawMin : INT  := 0;
    cAnalogRawMax : INT  := 27648;   // tipik 4-20mA tam olcek (cihaza bagli)
END_VAR
"""

MAIN_DECL = """PROGRAM MAIN
VAR
    xFirstScan : BOOL := TRUE;   // ilk cevrim bayragi
END_VAR
"""

MAIN_IMPL = """// ============================================================
// MAIN — kontrol dongusu giris noktasi (Task_Control'e bagli)
// Alt programlar buradan sirayla cagrilir.
// ============================================================

IF xFirstScan THEN
    // Tek seferlik baslangic islemleri
    xFirstScan := FALSE;
END_IF

// (* Buraya kontrol mantigi / alt PRG cagrilari gelir *)
// PRG_ZoneControl();
// PRG_Diagnostics();
"""


# ----------------------------------------------------------------------------
# YARDIMCILAR
# ----------------------------------------------------------------------------

def _get_app(proj):
    """Application nesnesini guvenli sekilde dondurur."""
    found = proj.find("Application", recursive=True)
    if not found:
        raise Exception("Application nesnesi projede bulunamadi. "
                        "Once bir PLC cihazi + Application ekleyin.")
    return found[0]


def _get_or_create_gvl(app, name, declaration):
    """GVL varsa al + guncelle, yoksa olustur (idempotent)."""
    existing = app.find(name, recursive=True)
    if existing:
        gvl = existing[0]
        print("  GVL zaten var, guncelleniyor: {}".format(name))
    else:
        gvl = app.create_gvl(name)
        print("  GVL olusturuldu: {}".format(name))
    gvl.textual_declaration.replace(declaration)
    return gvl


def _get_or_create_main(app):
    """MAIN PROGRAM POU'yu olusturur/gunceller (idempotent)."""
    existing = app.find("MAIN", recursive=True)
    if existing:
        prg = existing[0]
        print("  MAIN zaten var, guncelleniyor.")
    else:
        # PouType global'i Script Engine tarafindan saglanir.
        prg = app.create_pou("MAIN", PouType.Program)  # noqa: F821
        print("  MAIN olusturuldu (PROGRAM).")
    prg.textual_declaration.replace(MAIN_DECL)
    prg.textual_implementation.replace(MAIN_IMPL)
    return prg


def _find_task_config(proj):
    """Task Configuration nesnesini dondurur (yoksa None)."""
    found = proj.find("Task Configuration", recursive=True)
    return found[0] if found else None


def _ensure_task(task_config, task_def):
    """Bir task'i bulur ya da olusturur; parametrelerini ayarlar.

    Task olusturma API'si surume gore degisir:
      * Bazi surumlerde task_config.create_task(name) mevcuttur.
      * set_interval / set_priority metotlari her surumde olmayabilir.
    Bu yuzden hasattr ile yoklayip, desteklenmiyorsa uyari basariz.
    """
    name = task_def["name"]
    interval_us = task_def["interval_ms"] * 1000  # ms -> us

    existing = task_config.find(name, recursive=False)
    if existing:
        task = existing[0]
        print("  Task zaten var: {}".format(name))
    else:
        if hasattr(task_config, "create_task"):
            task = task_config.create_task(name)
            print("  Task olusturuldu: {} ({}ms)".format(name, task_def["interval_ms"]))
        else:
            print("  UYARI: create_task API'si yok. Task'i manuel ekleyin: {} "
                  "({}ms, Prio:{})".format(name, task_def["interval_ms"],
                                           task_def["priority"]))
            return None

    # Cycle araligi (us) — API destekliyorsa.
    if hasattr(task, "set_interval"):
        try:
            task.set_interval(interval_us)
        except Exception as ex:  # noqa: BLE001
            print("    Cycle ayari atlandi ({}): {}".format(name, str(ex)))
    else:
        print("    Not: set_interval yok; cycle'i ({}ms) manuel ayarlayin."
              .format(task_def["interval_ms"]))

    # Oncelik — API destekliyorsa.
    if hasattr(task, "set_priority"):
        try:
            task.set_priority(task_def["priority"])
        except Exception as ex:  # noqa: BLE001
            print("    Oncelik ayari atlandi ({}): {}".format(name, str(ex)))

    return task


def _bind_main_to_control(task_config, prg_name="MAIN", task_name="Task_Control"):
    """MAIN'i Task_Control'un cagri listesine ekler (API destekliyorsa).

    POU-Task baglama API'si (add_pou_call vb.) surume gore degisir.
    Bulunamazsa kullaniciya manuel adim onerilir.
    """
    found = task_config.find(task_name, recursive=False)
    if not found:
        print("  UYARI: {} bulunamadi; {} baglanamadi.".format(task_name, prg_name))
        return
    task = found[0]
    if hasattr(task, "add_pou_call"):
        try:
            task.add_pou_call(prg_name)
            print("  {} -> {} cagri listesine eklendi.".format(prg_name, task_name))
            return
        except Exception as ex:  # noqa: BLE001
            print("  POU baglama atlandi: {}".format(str(ex)))
    print("  Not: {} icine {} cagrisini manuel ekleyin (Add Call)."
          .format(task_name, prg_name))


# ----------------------------------------------------------------------------
# ANA AKIS
# ----------------------------------------------------------------------------

def build_basic_structure():
    """Temel proje yapisini kurar. Yalniz Script Engine icinde calisir."""
    proj = projects.primary  # noqa: F821
    if proj is None:
        raise Exception("Acik proje yok. IDE'de bir proje acik olmali.")

    app = _get_app(proj)

    print("[1/4] GVL'ler olusturuluyor...")
    _get_or_create_gvl(app, "GVL_IO", GVL_IO_DECL)
    _get_or_create_gvl(app, "GVL_Const", GVL_CONST_DECL)

    print("[2/4] MAIN PRG olusturuluyor...")
    _get_or_create_main(app)

    print("[3/4] Task'lar yapilandiriliyor...")
    tc = _find_task_config(proj)
    if tc is None:
        print("  UYARI: Task Configuration bulunamadi. Task'lar atlandi. "
              "Cihaz/Application sablonunda Task Configuration olmali.")
    else:
        for td in TASK_DEFS:
            _ensure_task(tc, td)
        _bind_main_to_control(tc, "MAIN", "Task_Control")

    print("[4/4] Kaydet + derle...")
    try:
        result = proj.compile()
        print("  Derleme: {}".format("BASARILI" if result else "HATALI"))
    except Exception as ex:  # noqa: BLE001
        print("  Derleme cagrisi hatasi: {}".format(str(ex)))

    projects.save()  # noqa: F821
    print("Temel yapi tamamlandi ve proje kaydedildi.")


def _main():
    try:
        projects  # noqa: F821
    except NameError:
        print("Bu script CODESYS Script Engine icinde calistirilmalidir "
              "(Tools > Scripting > Execute Script File).")
        sys.exit(1)
    build_basic_structure()


if __name__ == "__main__":
    _main()
