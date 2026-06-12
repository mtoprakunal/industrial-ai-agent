"""opcua_mcp uçtan-uca duman testi.

Yerel bir asyncua OPC-UA sunucusu başlatır, sunucu modülünün gerçek araç
handler'larını ona karşı çalıştırır. Gerçek cihaz gerektirmez.
Çalıştırma:  .venv\\Scripts\\python.exe mcp_servers\\opcua_mcp\\_smoke_test.py
"""

import asyncio
import importlib.util
import json
import os

ENDPOINT = "opc.tcp://127.0.0.1:4860/smoke/"

_here = os.path.dirname(__file__)
_spec = importlib.util.spec_from_file_location("oserver", os.path.join(_here, "server.py"))
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)


def show(label, result):
    print(f"\n>>> {label}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


async def increment_counter(counter_node, ua, n=4, period=0.3):
    """Subscription penceresi sırasında sunucu tarafında değeri değiştirir."""
    for i in range(1, n + 1):
        await asyncio.sleep(period)
        await counter_node.write_value(ua.DataValue(ua.Variant(100 + i, ua.VariantType.Int32)))


async def main():
    from asyncua import Server, ua

    srv = Server()
    await srv.init()
    srv.set_endpoint(ENDPOINT)
    idx = await srv.register_namespace("smoke")

    machine = await srv.nodes.objects.add_object(idx, "Machine")
    temp = await machine.add_variable(idx, "Temperature", 23.5)
    await temp.set_writable()
    counter = await machine.add_variable(idx, "Counter", 0, ua.VariantType.Int32)
    await counter.set_writable()

    temp_id = temp.nodeid.to_string()
    counter_id = counter.nodeid.to_string()
    machine_id = machine.nodeid.to_string()

    ok = True
    async with srv:
        await asyncio.sleep(0.3)

        show("connect", await m._do_connect({"endpoint": ENDPOINT}))

        r = show("browse(Objects)", await m._browse({}))
        names = [c.get("browse_name") for c in r["children"]]
        ok &= "Machine" in names

        r = show("browse(Machine)", await m._browse({"node_id": machine_id}))
        names = [c.get("browse_name") for c in r["children"]]
        ok &= "Temperature" in names and "Counter" in names

        r = show("read([Temperature, Counter])", await m._read({"node_ids": [temp_id, counter_id]}))
        vals = {v["node_id"]: v.get("value") for v in r["values"]}
        ok &= abs(vals.get(temp_id, 0) - 23.5) < 1e-6
        ok &= vals.get(counter_id) == 0

        show("write(Counter=42, Int32)", await m._write({"node_id": counter_id, "value": 42, "data_type": "Int32"}))
        show("write(Temperature=99.9, auto-type)", await m._write({"node_id": temp_id, "value": 99.9}))

        r = show("read([Temperature, Counter]) [yaz sonrası]", await m._read({"node_ids": [temp_id, counter_id]}))
        vals = {v["node_id"]: v.get("value") for v in r["values"]}
        ok &= vals.get(counter_id) == 42
        ok &= abs(vals.get(temp_id, 0) - 99.9) < 1e-3

        # Subscription: pencere boyunca sunucu Counter'ı değiştirir.
        writer = asyncio.create_task(increment_counter(counter, ua, n=4, period=0.3))
        r = show("subscribe(Counter, 1500ms pencere)", await m._subscribe(
            {"node_ids": [counter_id], "interval_ms": 200, "duration_ms": 1500}
        ))
        await writer
        ok &= r["sample_count"] >= 2  # en az ilk değer + birkaç değişiklik

        show("disconnect", await m._do_disconnect({}))
        show("read after disconnect (hata bekleniyor)", await _safe_read(counter_id))

    print("\n" + ("=" * 40))
    print("SONUC:", "[PASS] TUM DEGER KONTROLLERI GECTI" if ok else "[FAIL] BAZI KONTROLLER BASARISIZ")
    print("=" * 40)
    return 0 if ok else 1


async def _safe_read(nid):
    try:
        return await m._read({"node_ids": [nid]})
    except Exception as exc:
        return {"beklenen_hata": str(exc)}


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
