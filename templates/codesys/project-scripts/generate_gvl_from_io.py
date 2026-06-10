# -*- coding: utf-8 -*-
"""
generate_gvl_from_io.py — I/O listesinden (CSV) GVL_IO uretimi.

NE YAPAR
    Bir io_list.csv dosyasini okur (Tag,Adres,Tip,Yon,Task,Aciklama,Olcek_Not)
    ve CODESYS GVL_IO icin Structured Text (ST) deklarasyonu uretir.
    Cikti, Yon (DI/DO/AI/AO) kategorilerine ayrilmis, hizalanmis
    "Tag  AT %Adres : Tip;  // Aciklama" satirlarindan olusur.

CALISMA MODLARI (iki modlu tasarim)
    1) STANDALONE (CPython / IronPython, CODESYS olmadan):
         python generate_gvl_from_io.py io_list.csv 01_GVL_IO.st
       CSV -> ST uretim mantigi saf fonksiyonlardadir (build_gvl_declaration),
       bu sayede CODESYS API'si olmadan test edilebilir.

    2) CODESYS ICINDE (Script Engine):
         Tools > Scripting > Execute Script File... > bu dosya
       Acik projede Application altinda GVL_IO bulur/olusturur ve
       textual_declaration.replace() ile ureteni yazar.
       NOT: CODESYS'e CSV yolunu vermek icin asagidaki CSV_PATH sabitini
            duzenleyin ya da --scriptargs ile gecirin.

IRONPYTHON 2.7 UYUMU
    f-string / walrus / type-hint kullanilmaz. print() fonksiyon stili icin
    from __future__ import print_function eklenmistir. Dosya I/O codecs ile
    utf-8 olarak yapilir (Python 2 str/unicode tuzagindan kacinmak icin).
"""
from __future__ import print_function

import sys
import os
import codecs

# CODESYS icinde calistirilirken kullanilacak varsayilan CSV yolu.
# Standalone modda komut satiri argumani (sys.argv[1]) onceliklidir.
CSV_PATH = r"projects\EXAMPLE_conveyor\io_list.csv"


# ----------------------------------------------------------------------------
# SAF MANTIK (CODESYS API'siz, test edilebilir)
# ----------------------------------------------------------------------------

# Yon kodu -> (bolum basligi, siralama oncelik) eslemesi.
# Bilinmeyen Yon degerleri "DIGER" altinda toplanir.
_SECTION_ORDER = ["DI", "DO", "AI", "AO", "DIGER"]
_SECTION_TITLE = {
    "DI": "Dijital Girisler (DI)",
    "DO": "Dijital Cikislar (DO)",
    "AI": "Analog Girisler (AI)",
    "AO": "Analog Cikislar (AO)",
    "DIGER": "Diger / Siniflandirilmamis",
}


def parse_io_csv(text):
    """CSV metnini satir-sozluk listesine cevirir (saf, dosyasiz).

    Beklenen baslik: Tag,Adres,Tip,Yon,Task,Aciklama,Olcek_Not
    Bos satirlar ve basliklar atlanir. csv modulune bagimli degildir
    (IronPython'da da sorunsuz calissin diye basit ayristirma).
    Aciklama/Olcek_Not icinde virgul olabilecegi icin son alan
    maxsplit ile birlestirilir.
    """
    rows = []
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    header = None
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if header is None:
            header = [h.strip() for h in line.split(",")]
            continue
        # Baslik kadar alana bol; fazla virgulleri son alanda birlestir.
        parts = line.split(",")
        ncol = len(header)
        if len(parts) > ncol:
            parts = parts[: ncol - 1] + [",".join(parts[ncol - 1:])]
        # Eksik alanlari bos string ile tamamla.
        while len(parts) < ncol:
            parts.append("")
        row = {}
        for i, col in enumerate(header):
            row[col] = parts[i].strip()
        if not row.get("Tag"):
            continue
        rows.append(row)
    return rows


def _format_var_line(row, tag_w, addr_w, tip_w):
    """Tek bir GVL degisken satirini hizali olarak bicimler.

    Bicim:  TAG<pad> AT %ADRES<pad> : TIP<pad>;   // Aciklama
    Adres bos ise AT bloklari atlanir (sembolik degisken).
    """
    tag = row.get("Tag", "")
    addr = row.get("Adres", "").strip()
    tip = row.get("Tip", "BOOL") or "BOOL"
    aciklama = row.get("Aciklama", "").strip()
    olcek = row.get("Olcek_Not", "").strip()

    note = aciklama
    if olcek:
        note = (note + " | " if note else "") + olcek

    if addr:
        line = "    {tag} AT {addr} : {tip};".format(
            tag=tag.ljust(tag_w),
            addr=addr.ljust(addr_w),
            tip=tip.ljust(tip_w),
        )
    else:
        # Adressiz (sembolik) degisken: AT yok.
        line = "    {tag} : {tip};".format(
            tag=tag.ljust(tag_w + addr_w + 4),  # AT %... bloklari kadar kaydir
            tip=tip.ljust(tip_w),
        )

    if note:
        line = line + "   // " + note
    return line.rstrip()


def build_gvl_declaration(rows, gvl_name="GVL_IO"):
    """Satir listesinden tam GVL ST deklarasyon metnini uretir (saf fonksiyon).

    DI/DO/AI/AO bolumlerine ayirir, her bolum icinde CSV sirasini korur.
    Hizalama icin her bolumdeki en uzun tag/adres/tip genisligi kullanilir.
    """
    # Yon -> satirlar
    sections = {}
    for row in rows:
        yon = (row.get("Yon", "") or "").strip().upper()
        if yon not in _SECTION_TITLE:
            yon = "DIGER"
        sections.setdefault(yon, []).append(row)

    out = []
    out.append("// " + "=" * 60)
    out.append("// {} — io_list.csv'den otomatik uretildi".format(gvl_name))
    out.append("// Adresler io_list.csv ile BIREBIR tutarli olmalidir.")
    out.append("// Tek-yazar disiplini: cikislari yalniz ilgili PRG yazar.")
    out.append("// !! Bu dosya uretilmistir; elle duzenleme uzerine yazilabilir. !!")
    out.append("// " + "=" * 60)
    out.append("{attribute 'qualified_only'}")
    out.append("VAR_GLOBAL")

    first = True
    for yon in _SECTION_ORDER:
        sec_rows = sections.get(yon)
        if not sec_rows:
            continue
        # Bolum genisliklerini hesapla (hizalama icin).
        tag_w = max(len(r.get("Tag", "")) for r in sec_rows)
        addr_w = max(len((r.get("Adres", "") or "").strip()) for r in sec_rows)
        tip_w = max(len((r.get("Tip", "") or "BOOL")) for r in sec_rows)
        if not first:
            out.append("")
        first = False
        out.append("    // --- {} ---".format(_SECTION_TITLE[yon]))
        for r in sec_rows:
            out.append(_format_var_line(r, tag_w, addr_w, tip_w))

    out.append("END_VAR")
    return "\n".join(out) + "\n"


def generate_st_from_csv_text(csv_text, gvl_name="GVL_IO"):
    """Kolaylik sarmalayici: CSV metni -> ST metni (saf, test icin ideal)."""
    rows = parse_io_csv(csv_text)
    return build_gvl_declaration(rows, gvl_name=gvl_name)


def read_csv_file(path):
    """CSV dosyasini utf-8 olarak okur (IronPython 2.7 uyumlu)."""
    f = codecs.open(path, "r", encoding="utf-8")
    try:
        return f.read()
    finally:
        f.close()


def write_st_file(path, content):
    """ST ciktisini utf-8 olarak yazar."""
    f = codecs.open(path, "w", encoding="utf-8")
    try:
        f.write(content)
    finally:
        f.close()


# ----------------------------------------------------------------------------
# CODESYS ENTEGRASYONU (Script Engine icinde calisirken)
# ----------------------------------------------------------------------------

def _running_in_codesys():
    """Script Engine ortaminda miyiz? 'projects' global'i implicit import edilir."""
    try:
        projects  # noqa: F821  (Script Engine tarafindan saglanir)
        return True
    except NameError:
        return False


def apply_to_codesys(csv_path, gvl_name="GVL_IO"):
    """Acik CODESYS projesinde GVL_IO'yu bulur/olusturur ve icerigi yazar.

    Bu fonksiyon yalniz Script Engine icinde cagrilabilir (projects, PouType...
    global'leri orada saglanir). py_compile gecsin diye API isimleri
    fonksiyon govdesinde, guard'li olarak kullanilir.
    """
    # projects: Script Engine tarafindan implicit saglanan global.
    proj = projects.primary  # noqa: F821
    if proj is None:
        raise Exception("Acik proje yok. IDE'de bir proje acik olmali "
                        "ya da headless modda projects.open() gerekir.")

    found = proj.find("Application", recursive=True)
    if not found:
        raise Exception("Application nesnesi projede bulunamadi.")
    app = found[0]

    csv_text = read_csv_file(csv_path)
    declaration = generate_st_from_csv_text(csv_text, gvl_name=gvl_name)

    # Idempotent: GVL varsa al, yoksa olustur.
    existing = app.find(gvl_name, recursive=True)
    if existing:
        gvl = existing[0]
        print("GVL zaten var, icerigi guncelleniyor: {}".format(gvl_name))
    else:
        gvl = app.create_gvl(gvl_name)
        print("GVL olusturuldu: {}".format(gvl_name))

    gvl.textual_declaration.replace(declaration)
    print("GVL_IO {} degisken bolumu ile yazildi.".format(gvl_name))

    # Uretim dogrulugu yalniz derleme ile olculur (bkz. knowledge Not 5).
    try:
        result = proj.compile()
        print("Derleme sonucu: {}".format("BASARILI" if result else "HATALI"))
    except Exception as ex:  # noqa: BLE001
        print("Derleme cagrisi hatasi: {}".format(str(ex)))

    projects.save()  # noqa: F821
    print("Proje kaydedildi.")


# ----------------------------------------------------------------------------
# GIRIS NOKTASI
# ----------------------------------------------------------------------------

def _main():
    # CODESYS icinde mi yoksa standalone mi?
    if _running_in_codesys():
        # Script Engine: args --scriptargs ile gelebilir; yoksa CSV_PATH.
        csv_path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
        print("[CODESYS] CSV: {}".format(csv_path))
        apply_to_codesys(csv_path)
        return

    # Standalone: python generate_gvl_from_io.py <in.csv> [out.st]
    if len(sys.argv) < 2:
        print("Kullanim: python generate_gvl_from_io.py <io_list.csv> [cikti.st]")
        print("CSV verilmezse varsayilan: {}".format(CSV_PATH))
        in_path = CSV_PATH
    else:
        in_path = sys.argv[1]

    out_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(in_path):
        print("HATA: CSV bulunamadi: {}".format(in_path))
        sys.exit(1)

    csv_text = read_csv_file(in_path)
    st = generate_st_from_csv_text(csv_text)

    if out_path:
        write_st_file(out_path, st)
        print("Yazildi: {} ({} satir)".format(out_path, st.count("\n")))
    else:
        # stdout'a bas (dogrulama / pipe icin).
        print(st)


if __name__ == "__main__":
    _main()
