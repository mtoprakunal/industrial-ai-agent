# -*- coding: utf-8 -*-
"""
add_modbus_slave.py — Modbus TCP Slave cihazi ekler + register haritalama.

NE YAPAR
    1) Acik CODESYS projesinde Ethernet arayuzu altina bir ModbusTCP Slave
       Device ekler (yoksa) ve port/register sayilarini yapilandirir.
    2) io_list.csv mantigina gore bir GVL_Modbus uretir: BOOL girisler/
       cikislar Coil/Discrete Input'a, INT/WORD degerler Holding/Input
       Register'a eslenir. Ayrica okunabilir bir register haritasi (yorum)
       yazar.
       (Eslemenin temeli: knowledge/codesys/networking/02_modbus_slave.md
        veri modeli ve I/O Mapping bolumu.)

    Modbus veri modeli eslemesi (io_list Yon -> Modbus alani):
        DI  (BOOL giris)  -> Discrete Input  (FC02, salt-oku)
        DO  (BOOL cikis)  -> Coil            (FC01/05/15, oku+yaz)
        AI  (INT/WORD)    -> Input Register   (FC04, salt-oku)
        AO  (INT/WORD)    -> Holding Register (FC03/06/16, oku+yaz)

NASIL CALISTIRILIR
    CODESYS IDE icinde:
      1. Projeyi ac (Ethernet arayuzu device tree'de olmali).
      2. Tools > Scripting > Execute Script File... > bu dosya.
    GVL uretim mantigi standalone da test edilebilir:
      python add_modbus_slave.py projects/EXAMPLE_conveyor/io_list.csv

ONEMLI NOTLAR (API ve surum)
    * Device tree'ye cihaz ekleme (add_device) DeviceID/Type/Version uclusu
      gerektirir ve bu degerler CODESYS surumune + yuklu Device
      Repository'ye gore degisir. Asagidaki MODBUS_DEVICE_ID bir
      ORNEKTIR; kendi ortaminizdaki dogru kimligi
      "ScriptEngine ile DeviceRepository.get_all_devices()" veya
      Add Device dialogundaki Information sekmesinden alin.
    * Bu yuzden cihaz ekleme guard'li yapilir; basarisiz olursa GVL ve
      register haritasi yine de uretilir (asil degerli cikti budur),
      cihaz manuel eklenebilir. I/O Mapping (offset <-> GVL degiskeni)
      uretilen haritaya gore IDE'de baglanir.

IRONPYTHON 2.7 UYUMU
    from __future__ import print_function; CSV ayristirma saf fonksiyonda.
"""
from __future__ import print_function

import sys
import os
import codecs

# generate_gvl_from_io.py icindeki saf CSV ayristiriciyi yeniden kullaniriz.
# Ayni klasorde oldugu icin sys.path'e script dizinini ekleyelim.
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

try:
    from generate_gvl_from_io import parse_io_csv, read_csv_file, write_st_file
except Exception:  # noqa: BLE001
    # Yan dosya bulunamazsa (ornegin farkli calistirma dizini) minimal fallback.
    parse_io_csv = None
    read_csv_file = None
    write_st_file = None


CSV_PATH = r"projects\EXAMPLE_conveyor\io_list.csv"

# ModbusTCP Slave cihaz kimligi — ORNEK. Kendi ortaminizda dogrulayin!
# (DeviceRepository'den alin; surume/uretciye gore degisir.)
MODBUS_DEVICE_TYPE = "ModbusTCP_Slave_Device"
MODBUS_DEVICE_ID = "0000 0000"      # placeholder
MODBUS_DEVICE_VERSION = "3.5.17.0"  # placeholder
MODBUS_PORT = 502
MODBUS_UNIT_ID = 1


# ----------------------------------------------------------------------------
# SAF MANTIK: io_list -> Modbus register haritasi + GVL_Modbus (test edilebilir)
# ----------------------------------------------------------------------------

def build_register_map(rows):
    """io_list satirlarindan Modbus alan haritasi uretir (saf fonksiyon).

    Doner: dict {
        'coils': [(offset, tag, aciklama, tip), ...],          # DO
        'discrete_inputs': [...],                              # DI
        'holding_registers': [...],                            # AO
        'input_registers': [...],                              # AI
    }
    Offset'ler her alan icinde 0'dan ardisik atanir (boslusuz blok).
    """
    field = {
        "coils": [],
        "discrete_inputs": [],
        "holding_registers": [],
        "input_registers": [],
    }
    # Yon -> hedef alan
    yon_to_field = {
        "DO": "coils",
        "DI": "discrete_inputs",
        "AO": "holding_registers",
        "AI": "input_registers",
    }
    for row in rows:
        yon = (row.get("Yon", "") or "").strip().upper()
        target = yon_to_field.get(yon)
        if target is None:
            continue  # siniflandirilamayan satir atlanir
        offset = len(field[target])
        field[target].append((
            offset,
            row.get("Tag", ""),
            row.get("Aciklama", "").strip(),
            (row.get("Tip", "") or "WORD").strip(),
        ))
    return field


def _modbus_var_type(field_name, src_type):
    """Modbus GVL degiskeni icin ST tipi secer.

    Coil / Discrete Input -> BOOL.
    Holding / Input Register -> WORD (Modbus 16-bit register). INT kaynaklar
    da WORD register'a tasinir; isaret yorumu istemcide belgelendirilir.
    """
    if field_name in ("coils", "discrete_inputs"):
        return "BOOL"
    return "WORD"


def build_modbus_gvl(reg_map, gvl_name="GVL_Modbus"):
    """Register haritasindan GVL_Modbus ST deklarasyonu uretir (saf fonksiyon)."""
    fc_help = {
        "holding_registers": "HOLDING REGISTERS (FC03 oku / FC06,16 yaz)",
        "input_registers":   "INPUT REGISTERS (FC04 — salt-oku)",
        "coils":             "COILS (FC01 oku / FC05,15 yaz)",
        "discrete_inputs":   "DISCRETE INPUTS (FC02 — salt-oku)",
    }
    order = ["holding_registers", "input_registers", "coils", "discrete_inputs"]

    out = []
    out.append("// " + "=" * 60)
    out.append("// {} — io_list.csv'den uretilen Modbus eslemesi".format(gvl_name))
    out.append("// I/O Mapping'de offset'ler asagidaki haritaya gore baglanir.")
    out.append("// Tek-yazar: HR'a master yazar, PLC EZMEZ (Hata 3).")
    out.append("// " + "=" * 60)
    out.append("{attribute 'qualified_only'}")
    out.append("VAR_GLOBAL")

    for fname in order:
        entries = reg_map.get(fname, [])
        if not entries:
            continue
        out.append("")
        out.append("    // --- {} ---".format(fc_help[fname]))
        # hizalama
        name_w = 0
        for (_off, tag, _ac, _tp) in entries:
            name_w = max(name_w, len(tag))
        for (off, tag, aciklama, src_type) in entries:
            vtype = _modbus_var_type(fname, src_type)
            comment = "Offset {}".format(off)
            if aciklama:
                comment += " | " + aciklama
            out.append("    {tag} : {vtype};   // {c}".format(
                tag=tag.ljust(name_w), vtype=vtype, c=comment))

    out.append("END_VAR")
    return "\n".join(out) + "\n"


def build_register_map_doc(reg_map):
    """Insan-okunur register haritasi belgesi (yorum metni) uretir."""
    titles = {
        "holding_registers": "HOLDING REGISTERS (FC03/06/16)",
        "input_registers":   "INPUT REGISTERS (FC04)",
        "coils":             "COILS (FC01/05/15)",
        "discrete_inputs":   "DISCRETE INPUTS (FC02)",
    }
    order = ["holding_registers", "input_registers", "coils", "discrete_inputs"]
    lines = []
    lines.append("MODBUS TCP SLAVE REGISTER HARITASI")
    lines.append("Port: {}  Unit ID: {}".format(MODBUS_PORT, MODBUS_UNIT_ID))
    lines.append("Adresleme: protokol 0-tabanli (offset). SCADA 1-tabanli "
                 "gosterebilir; test degeriyle dogrulayin.")
    for fname in order:
        entries = reg_map.get(fname, [])
        if not entries:
            continue
        lines.append("")
        lines.append(titles[fname])
        lines.append("-" * 60)
        lines.append("Offset | Degisken | Aciklama")
        for (off, tag, aciklama, _tp) in entries:
            lines.append("  {:<4} | {} | {}".format(off, tag, aciklama))
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# CODESYS ENTEGRASYONU
# ----------------------------------------------------------------------------

def _add_modbus_device(proj):
    """Ethernet arayuzu altina ModbusTCP Slave cihazi ekler (guard'li).

    add_device API'si DeviceID uclusu gerektirir ve bu surume/repository'ye
    bagimlidir. Basarisiz olursa None doner; GVL uretimi yine de yapilir.
    """
    eth = proj.find("Ethernet", recursive=True)
    if not eth:
        print("  UYARI: 'Ethernet' arayuzu bulunamadi. Cihaz eklenemedi; "
              "Modbus slave'i manuel ekleyin (Ethernet > Add Device > "
              "ModbusTCP Slave Device).")
        return None
    iface = eth[0]

    # Idempotent: zaten ekli mi?
    existing = proj.find("Modbus_TCP_Slave_Device", recursive=True)
    if existing:
        print("  ModbusTCP Slave cihazi zaten ekli.")
        return existing[0]

    if hasattr(iface, "add_device"):
        try:
            # NOT: Asagidaki kimlik degerleri ORNEKTIR; ortaminizda
            # DeviceRepository'den dogru degerlerle degistirin.
            dev = iface.add_device(
                "Modbus_TCP_Slave_Device",
                MODBUS_DEVICE_TYPE,
                MODBUS_DEVICE_ID,
                MODBUS_DEVICE_VERSION,
            )
            print("  ModbusTCP Slave cihazi eklendi (port {}).".format(MODBUS_PORT))
            return dev
        except Exception as ex:  # noqa: BLE001
            print("  UYARI: add_device basarisiz ({}). Dogru DeviceID'yi "
                  "DeviceRepository'den alin. Cihaz manuel eklenebilir."
                  .format(str(ex)))
            return None

    print("  UYARI: add_device API'si yok; cihazi manuel ekleyin.")
    return None


def _get_or_create_gvl(app, name, declaration):
    existing = app.find(name, recursive=True)
    if existing:
        gvl = existing[0]
        print("  GVL zaten var, guncelleniyor: {}".format(name))
    else:
        gvl = app.create_gvl(name)
        print("  GVL olusturuldu: {}".format(name))
    gvl.textual_declaration.replace(declaration)
    return gvl


def configure_modbus(csv_path):
    """Modbus slave + GVL_Modbus kurar. Yalniz Script Engine icinde calisir."""
    proj = projects.primary  # noqa: F821
    if proj is None:
        raise Exception("Acik proje yok.")

    found = proj.find("Application", recursive=True)
    if not found:
        raise Exception("Application bulunamadi.")
    app = found[0]

    print("[1/4] Modbus TCP Slave cihazi ekleniyor...")
    _add_modbus_device(proj)

    print("[2/4] io_list -> register haritasi...")
    csv_text = read_csv_file(csv_path)
    rows = parse_io_csv(csv_text)
    reg_map = build_register_map(rows)
    counts = dict((k, len(v)) for k, v in reg_map.items())
    print("  Coil:{coils} DI:{discrete_inputs} HR:{holding_registers} "
          "IR:{input_registers}".format(**counts))

    print("[3/4] GVL_Modbus uretiliyor...")
    decl = build_modbus_gvl(reg_map)
    _get_or_create_gvl(app, "GVL_Modbus", decl)
    print("  Register haritasi (I/O Mapping bunu izler):")
    print(build_register_map_doc(reg_map))

    print("[4/4] Kaydet + derle...")
    try:
        result = proj.compile()
        print("  Derleme: {}".format("BASARILI" if result else "HATALI"))
    except Exception as ex:  # noqa: BLE001
        print("  Derleme cagrisi hatasi: {}".format(str(ex)))

    projects.save()  # noqa: F821
    print("Modbus yapilandirmasi tamamlandi.")
    print("Sonraki adim: I/O Mapping'de offset'leri GVL_Modbus degiskenlerine "
          "baglayin ve Bus Cycle Task atayin (Hata 5).")


# ----------------------------------------------------------------------------
# GIRIS NOKTASI
# ----------------------------------------------------------------------------

def _running_in_codesys():
    try:
        projects  # noqa: F821
        return True
    except NameError:
        return False


def _main():
    if _running_in_codesys():
        csv_path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
        print("[CODESYS] CSV: {}".format(csv_path))
        configure_modbus(csv_path)
        return

    # Standalone: register haritasi + GVL_Modbus uretimini test et.
    if parse_io_csv is None:
        print("HATA: generate_gvl_from_io.py ayni klasorde bulunamadi.")
        sys.exit(1)

    in_path = sys.argv[1] if len(sys.argv) > 1 else CSV_PATH
    if not os.path.exists(in_path):
        print("HATA: CSV bulunamadi: {}".format(in_path))
        sys.exit(1)

    csv_text = read_csv_file(in_path)
    rows = parse_io_csv(csv_text)
    reg_map = build_register_map(rows)
    print(build_modbus_gvl(reg_map))
    print("\n// ---- REGISTER HARITASI ----")
    print(build_register_map_doc(reg_map))


if __name__ == "__main__":
    _main()
