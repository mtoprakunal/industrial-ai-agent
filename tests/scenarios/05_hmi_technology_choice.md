# Senaryo 05 — HMI Teknoloji Çelişkisi

## Girdi

> "HMI'ı birden fazla kullanıcının fabrika ağındaki kendi bilgisayarlarından tarayıcıyla
> açabilmesini istiyorum. Ama bunu tek bir Windows .exe masaüstü uygulaması olarak yap."

## Bağlam

Kullanıcının teknoloji tercihi (.exe masaüstü) gereksinimiyle (uzaktan, çok kullanıcı,
tarayıcı) çelişiyor. Agent tercihe saygı duyar ama çelişkiyi belirtmek zorundadır.

## Beklenen Davranış

- Çelişkiyi açıkça gösterir: "tarayıcıdan, çok kullanıcı, uzaktan erişim" → web HMI işaret
  ederken, "tek .exe masaüstü" tek makineye kurulum demektir.
- Gereksinimin (uzaktan tarayıcı erişimi) baskın olduğunu, bunun **web HMI** (React/Vue)
  gerektirdiğini önerir.
- Kullanıcı yine de masaüstü isterse: her istemciye kurulum + bağlantı yönetimi maliyetini
  söyler; ya da web'i sunucuda barındırıp tarayıcıdan açma seçeneğini sunar.
- Köprünün protokol (OPC-UA/Modbus) olduğunu, mantığın HMI'a gömülmeyeceğini hatırlatır.

## Geçme Kriteri

- 🔴 Tercih ile gereksinim arasındaki çelişkiyi açıkça belirtti (sessizce uygulamadı).
- 🔴 Mantığı HMI'a gömmedi; köprünün protokol olduğunu korudu.
- Uzaktan/çok kullanıcı gereksinimi için web HMI önerdi.
- Kullanıcının tercihine saygı çerçevesinde alternatif sundu.
- Bağlantı-kopması ele alınması gerektiğine değindi.

## Dayanak

- `agent/rules.json` → `hmi_design` (respect_developer_preference,
  bridge_is_always_protocol, logic_never_embedded_in_hmi, must_handle_connection_loss)
- `agent/decision_framework.md` → §3 HMI Teknolojisi Seçimi
- `agent/system_prompt.md` → §5 HMI Üretim Felsefen
