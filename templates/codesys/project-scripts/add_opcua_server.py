# -*- coding: utf-8 -*-
"""
add_opcua_server.py — Symbol Configuration + OPC UA yayini ekler.

NE YAPAR
    Acik CODESYS projesinde:
      * Application altinda Symbol Configuration nesnesi olusturur (yoksa).
        (CODESYS yerlesik OPC UA sunucusu, IEC degiskenlerini Symbol
         Configuration uzerinden Address Space'e yansitir — bkz.
         knowledge/codesys/networking/01_opcua_server.md "Hizli Yol".)
      * Yayinlanacak GVL'leri sembol setine alir (varsayilan: GVL_HMI okur/yazar,
        GVL_Diagnostics salt-oku). Saldiri yuzeyini kucuk tutmak icin tum
        degiskenleri degil yalniz secili GVL'leri acar (Not 5: sembol patlamasi).

NASIL CALISTIRILIR
    CODESYS IDE icinde:
      1. Projeyi ac (PLC cihazi + Application hazir olmali).
      2. Tools > Scripting > Execute Script File... > bu dosya.
    Ardindan: Build > Download > Start. OPC UA NodeId formati:
      ns=4;s=|var|<RuntimeName>.Application.GVL_HMI.<Tag>

ONEMLI NOTLAR (API ve surum)
    * Symbol Configuration olusturma ve ICINE hangi degiskenlerin girecegini
      programatik secme API'si CODESYS surumune gore degisir. create_*
      isimleri her surumde ayni olmayabilir; bu yuzden once mevcut nesne
      aranir, olusturma birden fazla bilinen yontemle denenir, basarisiz
      olursa kullaniciya manuel adim onerilir.
    * Hangi GVL'lerin sembol setine girecegi cogu surumde "remote access"
      attribute'u ya da editor secimi ile yonetilir. En tasinabilir yontem:
      yayinlanacak GVL deklarasyonuna {attribute 'symbol := 'readwrite''}
      pragmasi eklemektir; bu script o pragma'yi GVL basina enjekte eder.
    * SP17+ anonymous erisim varsayilan kapali. Test icin client'ta
      kullanici/sifre ya da CODESYSControl.cfg AllowAnonymous=1 gerekir
      (bkz. knowledge dokumani Hata 1). Bu ayar runtime tarafindadir,
      scriptlenmez; burada yalniz yayin yapisi kurulur.

IRONPYTHON 2.7 UYUMU
    from __future__ import print_function; Script Engine global'leri guard'li.
"""
from __future__ import print_function

import sys


# Yayinlanacak GVL'ler ve erisim seviyesi.
#   "readwrite" -> OPC UA client okuyup yazabilir (komut/HMI degiskenleri)
#   "read"      -> yalniz okuma (telemetri / teshis)
PUBLISH_GVLS = [
    {"name": "GVL_HMI", "access": "readwrite"},
    {"name": "GVL_Diagnostics", "access": "read"},
]


def _get_app(proj):
    found = proj.find("Application", recursive=True)
    if not found:
        raise Exception("Application nesnesi bulunamadi.")
    return found[0]


def _ensure_symbol_configuration(app):
    """Symbol Configuration nesnesini bulur ya da olusturur (idempotent).

    Olusturma API'si surume gore degisir; birkac bilinen yol denenir.
    Bulunamaz/olusturulamazsa None doner ve manuel adim onerilir.
    """
    found = app.find("Symbol Configuration", recursive=True)
    if found:
        print("  Symbol Configuration zaten var.")
        return found[0]

    # Yontem 1: ozel yardimci (bazi surumler)
    if hasattr(app, "create_symbol_configuration"):
        try:
            sc = app.create_symbol_configuration()
            print("  Symbol Configuration olusturuldu (create_symbol_configuration).")
            return sc
        except Exception as ex:  # noqa: BLE001
            print("  create_symbol_configuration basarisiz: {}".format(str(ex)))

    # Yontem 2: genel create_object / GUID tabanli ekleme (surume bagli)
    if hasattr(app, "create_object"):
        try:
            sc = app.create_object("Symbol Configuration")
            print("  Symbol Configuration olusturuldu (create_object).")
            return sc
        except Exception as ex:  # noqa: BLE001
            print("  create_object basarisiz: {}".format(str(ex)))

    print("  UYARI: Symbol Configuration programatik olusturulamadi. "
          "Manuel ekleyin: Application > Add Object > Symbol Configuration.")
    return None


def _inject_symbol_pragma(app, gvl_name, access):
    """Yayinlanacak GVL'nin deklarasyonuna symbol pragma'si ekler.

    Sembol setine girisin en tasinabilir yolu: GVL deklarasyon blogunun
    basina {attribute 'symbol := 'readwrite''} (veya 'read') eklemek.
    Bu attribute, derleyiciye degiskenleri Symbol Configuration'a dahil
    etmesini soyler. Idempotent: pragma zaten varsa tekrar eklenmez.
    """
    found = app.find(gvl_name, recursive=True)
    if not found:
        print("  Atlandi (GVL yok): {}".format(gvl_name))
        return False
    gvl = found[0]

    decl = gvl.textual_declaration.text
    pragma = "{attribute 'symbol := '" + access + "''}"

    if "symbol :=" in decl:
        print("  {} zaten symbol pragma'sina sahip, atlandi.".format(gvl_name))
        return True

    # Pragma'yi VAR_GLOBAL satirinin hemen ustune koy.
    lines = decl.split("\n")
    out = []
    inserted = False
    for line in lines:
        if (not inserted) and line.strip().upper().startswith("VAR_GLOBAL"):
            out.append(pragma)
            inserted = True
        out.append(line)
    if not inserted:
        # VAR_GLOBAL bulunamadiysa basa ekle.
        out = [pragma] + lines

    gvl.textual_declaration.replace("\n".join(out))
    print("  {} -> OPC UA yayini ({}) eklendi.".format(gvl_name, access))
    return True


def configure_opcua():
    """OPC UA yayin yapisini kurar. Yalniz Script Engine icinde calisir."""
    proj = projects.primary  # noqa: F821
    if proj is None:
        raise Exception("Acik proje yok.")

    app = _get_app(proj)

    print("[1/3] Symbol Configuration...")
    _ensure_symbol_configuration(app)

    print("[2/3] GVL'ler yayina aliniyor...")
    any_published = False
    for spec in PUBLISH_GVLS:
        if _inject_symbol_pragma(app, spec["name"], spec["access"]):
            any_published = True
    if not any_published:
        print("  UYARI: Hicbir GVL yayinlanmadi. PUBLISH_GVLS listesini "
              "projedeki GVL adlarina gore guncelleyin.")

    print("[3/3] Kaydet + derle...")
    try:
        result = proj.compile()
        print("  Derleme: {}".format("BASARILI" if result else "HATALI"))
    except Exception as ex:  # noqa: BLE001
        print("  Derleme cagrisi hatasi: {}".format(str(ex)))

    projects.save()  # noqa: F821
    print("OPC UA yapilandirmasi tamamlandi.")
    print("Sonraki adim: Build > Download > Start.")
    print("SP17+ ise client'ta kullanici/sifre ya da AllowAnonymous=1 gerekir.")


def _main():
    try:
        projects  # noqa: F821
    except NameError:
        print("Bu script CODESYS Script Engine icinde calistirilmalidir "
              "(Tools > Scripting > Execute Script File).")
        sys.exit(1)
    configure_opcua()


if __name__ == "__main__":
    _main()
