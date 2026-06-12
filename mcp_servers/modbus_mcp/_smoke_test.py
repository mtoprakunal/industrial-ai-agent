"""modbus_mcp uçtan-uca duman testi.

Yerel bir Modbus TCP simülatörü başlatır, sunucu modülünün gerçek araç
handler'larını ona karşı çalıştırır. Gerçek cihaz gerektirmez.
Çalıştırma:  .venv\\Scripts\\python.exe mcp_servers\\modbus_mcp\\_smoke_test.py
"""

import asyncio
import importlib.util
import json
import os

HOST, PORT = "127.0.0.1", 5020

# Sunucu modülünü dosyadan yükle.
_here = os.path.dirname(__file__)
_spec = importlib.util.spec_from_file_location("mserver", os.path.join(_here, "server.py"))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


async def start_simulator():
    # pymodbus 3.13 yeni simülatör API'si (SimData/SimDevice).
    # SimDevice 4-tuple alan sırası: (coils, discrete_inputs, holding, input).
    from pymodbus.simulator import DataType, SimData, SimDevice
    from pymodbus.server import StartAsyncTcpServer

    coils = SimData(0, values=[False, True, False, True, False, False], datatype=DataType.BITS)
    discrete = SimData(0, values=[True, False, True, False], datatype=DataType.BITS)
    holding = SimData(0, values=[10, 20, 30, 40, 50], datatype=DataType.REGISTERS)
    inputs = SimData(0, values=[0, 0, 0, 0], datatype=DataType.REGISTERS)

    device = SimDevice(1, simdata=([coils], [discrete], [holding], [inputs]))
    return asyncio.create_task(
        StartAsyncTcpServer(context=device, address=(HOST, PORT))
    )


def show(label, result):
    print(f"\n>>> {label}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


async def main():
    sim = await start_simulator()
    await asyncio.sleep(0.7)  # simülatörün dinlemeye başlamasını bekle

    ok = True
    try:
        show("connect", await m._do_connect({"host": HOST, "port": PORT, "unit_id": 1}))

        r = show("read_holding_registers(0,5)", await m._read_holding_registers({"address": 0, "count": 5}))
        ok &= r.get("registers") == [10, 20, 30, 40, 50]

        show("write_register(addr=1, [1234])", await m._write_register({"address": 1, "values": [1234]}))
        show("write_register(addr=2, [111,222])", await m._write_register({"address": 2, "values": [111, 222]}))

        r = show("read_holding_registers(0,5) [yaz sonrası]", await m._read_holding_registers({"address": 0, "count": 5}))
        ok &= r.get("registers") == [10, 1234, 111, 222, 50]

        r = show("read_coils(0,6)", await m._read_coils({"address": 0, "count": 6}))
        ok &= r.get("bits") == [False, True, False, True, False, False]

        show("write_coil(addr=0, [True])", await m._write_coil({"address": 0, "values": [True]}))
        show("write_coil(addr=2, [True,True])", await m._write_coil({"address": 2, "values": [True, True]}))
        r = show("read_coils(0,6) [yaz sonrası]", await m._read_coils({"address": 0, "count": 6}))
        ok &= r.get("bits") == [True, True, True, True, False, False]

        r = show("read_coils(0,4, discrete_input)", await m._read_coils({"address": 0, "count": 4, "input_type": "discrete_input"}))
        ok &= r.get("bits") == [True, False, True, False]

        # Hata yolu: bağlı değilken okuma
        show("disconnect", await m._do_disconnect({}))
        show("read after disconnect (hata bekleniyor)", await _safe_read())

    finally:
        sim.cancel()
        try:
            from pymodbus.server import ServerAsyncStop
            await ServerAsyncStop()
        except Exception:
            pass

    print("\n" + ("=" * 40))
    print("SONUC:", "[PASS] TUM DEGER KONTROLLERI GECTI" if ok else "[FAIL] BAZI KONTROLLER BASARISIZ")
    print("=" * 40)
    return 0 if ok else 1


async def _safe_read():
    try:
        return await m._read_holding_registers({"address": 0, "count": 1})
    except Exception as exc:  # _ensure_connected RuntimeError fırlatır
        return {"beklenen_hata": str(exc)}


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
