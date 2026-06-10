# Ag Topolojisi — `[PROJE_ADI]`

> Bu sablon, projenin ag topolojisini, IP planini, port/protokol kullanimini ve
> IEC 62443 zone/conduit guvenlik notlarini belgeler. Her `[doldurulacak]` alanini
> projeye gore degistirin.

## 1. Topoloji Diyagrami (ASCII)

```
                         [ Kurumsal Ag / IT (Level 4) ]
                                      |
                              +---------------+
                              |   Firewall    |   <-- Conduit (IT/OT siniri)
                              |  (Gateway)    |
                              +---------------+
                                      |
        ============================ OT Ag (Level 3 - SCADA) ============================
                                      |
                              +---------------+
                              |   Managed     |
                              |   Switch L3   |
                              +---------------+
                               |      |      |
                  +------------+      |      +-------------+
                  |                   |                    |
          +--------------+   +----------------+   +-----------------+
          |   PLC /      |   |  HMI Istemci 1 |   |  HMI Istemci 2  |
          |  CODESYS     |   |  (Web/Browser) |   |  (Web/Browser)  |
          |  SoftPLC     |   +----------------+   +-----------------+
          | OPC-UA Server|
          +--------------+
                  |
        ==== Saha Agi (Level 1/2 - I/O) ====
                  |
          +----------------+
          |  Uzak I/O /    |
          |  VFD / Sensor  |
          +----------------+
```

> Diyagrami gercek mimariye gore guncelle. PLC, switch, HMI istemcileri, gateway/firewall
> ve varsa uzak I/O dropleri gosterilmeli.

## 2. VLAN / Segment Tablosu

| Segment | VLAN ID | Amac | IEC 62443 Zone |
|---------|---------|------|----------------|
| IT / Kurumsal | `[..]` | Ofis agi | Enterprise (Level 4) |
| SCADA / Izleme | `[..]` | HMI, OPC-UA istemcileri | Operations (Level 3) |
| Kontrol | `[..]` | PLC, kontroldoru | Control (Level 1/2) |
| Saha / I/O | `[..]` | Uzak I/O, VFD, sensorler | Field (Level 0/1) |

## 3. IP Plan Tablosu

| Cihaz | Rol | IP Adresi | Subnet | Gateway | VLAN |
|-------|-----|-----------|--------|---------|------|
| PLC / SoftPLC | OPC-UA Server | `[doldurulacak]` | `[..]` | `[..]` | `[..]` |
| Managed Switch | Altyapi | `[doldurulacak]` | `[..]` | `[..]` | `[..]` |
| HMI Istemci 1 | OPC-UA Client | `[doldurulacak]` | `[..]` | `[..]` | `[..]` |
| HMI Istemci 2 | OPC-UA Client | `[doldurulacak]` | `[..]` | `[..]` | `[..]` |
| Gateway / Firewall | IT/OT siniri | `[doldurulacak]` | `[..]` | `[..]` | `[..]` |

## 4. Port / Protokol Tablosu

| Protokol | Port | Tasima | Kaynak | Hedef | Not |
|----------|------|--------|--------|-------|-----|
| OPC-UA | 4840 | TCP | HMI istemcileri | PLC | Yapilandirilmis veri, guvenlik politikasi onerilir |
| Modbus TCP | 502 | TCP | `[..]` | `[..]` | Basit register erisimi (kullaniliyorsa) |
| HTTPS | 443 | TCP | Tarayici | Web HMI | Web HMI sunumu |
| HTTP | 80 | TCP | `[..]` | `[..]` | Yalniz dahili / sifrelenmemis - production'da kapat |
| `[..]` | `[..]` | `[..]` | `[..]` | `[..]` | `[doldurulacak]` |

> Yalniz fiilen kullanilan portlari acik birak. Kullanilmayan protokol satirlarini sil.

## 5. Guvenlik Notlari (IEC 62443 Zone / Conduit)

- **Zone ayrimi:** IT ve OT aglari firewall ile ayrilmali; aralarindaki tek gecis
  noktasi (conduit) tanimlanmali. `[doldurulacak]`
- **Conduit kurallari:** Sadece izin verilen port/protokoller (orn. OPC-UA 4840)
  IT/OT siniri uzerinden gecmeli; geri kalan trafik varsayilan olarak engellenmeli.
- **En az ayricalik:** Her cihaz yalniz ihtiyaci olan portlara erisebilmeli.
- **OPC-UA guvenligi:** Sertifika tabanli kimlik dogrulama ve `SignAndEncrypt`
  guvenlik politikasi etkinlestirilmeli; anonim erisim kapatilmali. `[doldurulacak]`
- **Yonetimsel erisim:** Switch/firewall yonetim arayuzleri ayri yonetim VLAN'inda
  tutulmali.
- **Yama / sertlestirme:** Kullanilmayan servisler ve portlar kapatilmali. `[doldurulacak]`
