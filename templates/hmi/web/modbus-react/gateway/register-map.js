// ============================================================================
//  register-map.js — Modbus adres haritasi (tag <-> register/coil esleme)
// ============================================================================
//
//  Bu dosya, PLC io_list.csv mantigini Modbus adres uzayina tasir.
//  Kendi projeniz icin TEK degistirmeniz gereken yer burasidir; server.js
//  bu haritayi okuyarak hangi blogu okuyacagini ve yazmayi otomatik cikarir.
//
//  Modbus adres modeli (4 ayri adres uzayi, hepsi 0-tabanli):
//  ┌──────────────────┬──────┬──────────┬─────────────────────────────────┐
//  │ Bolge            │ FC   │ Yon      │ io_list.csv karsiligi           │
//  ├──────────────────┼──────┼──────────┼─────────────────────────────────┤
//  │ Coil             │ 01/05│ R/W bool │ DO (%QX) — motor, lamba, korna  │
//  │ Discrete Input   │ 02   │ R   bool │ DI (%IX) — buton, sensor, secici│
//  │ Input Register   │ 04   │ R   16bit│ AI (%IW) — takometre, olcum     │
//  │ Holding Register │ 03/06│ R/W 16bit│ Setpoint, komut, recete         │
//  └──────────────────┴──────┴──────────┴─────────────────────────────────┘
//
//  ONEMLI (knowledge/02_modbus_clients_js Not 5): Modbus okumasi SUREKLI bir
//  adres blogu okur, deliklerin uzerinden gecemez. Bu yuzden ilgili tag'leri
//  adres uzayinda yan yana yerlestirin ve okuma bloklarini bosluksuz tutun.
// ============================================================================

// --- Decode/scale yardimcilari (16-bit ham register -> anlamli deger) ---

/** Modbus INT16 isaretsiz okunur; isaretli (signed) yorumlamak icin. */
export function toInt16(raw) {
  return raw > 32767 ? raw - 65536 : raw;
}

/**
 * 4-20mA olcek donusumu (io_list: "4mA=0 / 20mA=120 m/min").
 * PLC analog kart ham degeri tipik 0..27648 (Siemens) veya 0..32767 verir.
 * Bu sablonda PLC'nin degeri 4-20mA penceresinde 0..32767'ye olceklendigini
 * varsayiyoruz; gercek karta gore rawMin/rawMax'i ayarlayin.
 */
export function scale4_20mA(raw, engMin, engMax, rawMin = 0, rawMax = 32767) {
  const clamped = Math.max(rawMin, Math.min(rawMax, raw));
  return engMin + ((clamped - rawMin) / (rawMax - rawMin)) * (engMax - engMin);
}

// ============================================================================
//  TAG HARITASI
//  type:    "COIL" | "DI" | "IR" | "HR"
//  address: ilgili adres uzayinda 0-tabanli adres
//  writable: yalnizca COIL ve HR icin true olabilir
//  kind:    "bool" | "int" | "analog"  (frontend gosterim ipucu)
//  scale:   HR/IR icin lineer bolme (ham / scale). Orn. scale:10 -> *0.1
//  decode:  ozel cozucu fonksiyon (raw) => number  (scale yerine)
//  unit, label, plcTag: meta bilgi (frontend ve dokumantasyon icin)
// ============================================================================

export const TAG_MAP = {
  // -------------------------------------------------------------------------
  // DO -> COIL (FC01 oku / FC05 yaz) — io_list %QX cikislari
  // -------------------------------------------------------------------------
  zn1_motor_run:  { type: "COIL", address: 0, writable: true, kind: "bool", label: "Bolge 1 Motor", plcTag: "ZN1_MTR_01_Run" },
  zn1_lamp_run:   { type: "COIL", address: 1, writable: true, kind: "bool", label: "Bolge 1 Calisiyor Lambasi", plcTag: "ZN1_LMP_01_Run" },
  zn1_lamp_fault: { type: "COIL", address: 2, writable: true, kind: "bool", label: "Bolge 1 Hata Lambasi", plcTag: "ZN1_LMP_01_Flt" },
  zn2_motor_run:  { type: "COIL", address: 3, writable: true, kind: "bool", label: "Bolge 2 Motor", plcTag: "ZN2_MTR_02_Run" },
  zn2_lamp_run:   { type: "COIL", address: 4, writable: true, kind: "bool", label: "Bolge 2 Calisiyor Lambasi", plcTag: "ZN2_LMP_02_Run" },
  zn2_lamp_fault: { type: "COIL", address: 5, writable: true, kind: "bool", label: "Bolge 2 Hata Lambasi", plcTag: "ZN2_LMP_02_Flt" },
  zn3_motor_run:  { type: "COIL", address: 6, writable: true, kind: "bool", label: "Bolge 3 Motor", plcTag: "ZN3_MTR_03_Run" },
  zn3_lamp_run:   { type: "COIL", address: 7, writable: true, kind: "bool", label: "Bolge 3 Calisiyor Lambasi", plcTag: "ZN3_LMP_03_Run" },
  zn3_lamp_fault: { type: "COIL", address: 8, writable: true, kind: "bool", label: "Bolge 3 Hata Lambasi", plcTag: "ZN3_LMP_03_Flt" },
  beacon_run:     { type: "COIL", address: 9, writable: true, kind: "bool", label: "Kule Isigi Calisiyor", plcTag: "PLT_BCN_01_Run" },
  beacon_fault:   { type: "COIL", address: 10, writable: true, kind: "bool", label: "Kule Isigi Hata", plcTag: "PLT_BCN_01_Flt" },
  horn_alarm:     { type: "COIL", address: 11, writable: true, kind: "bool", label: "Sesli Alarm Korna", plcTag: "PLT_HRN_01_Alarm" },

  // -------------------------------------------------------------------------
  // DI -> DISCRETE INPUT (FC02 oku, salt okunur) — io_list %IX girisleri
  // -------------------------------------------------------------------------
  zn1_sel_auto:   { type: "DI", address: 0, kind: "bool", label: "Bolge 1 Oto Secici", plcTag: "ZN1_SEL_01_Auto" },
  zn1_pb_start:   { type: "DI", address: 1, kind: "bool", label: "Bolge 1 Baslat", plcTag: "ZN1_PBS_01_Start" },
  zn1_pb_stop:    { type: "DI", address: 2, kind: "bool", label: "Bolge 1 Durdur", plcTag: "ZN1_PBS_01_Stop" },
  zn1_jam:        { type: "DI", address: 3, kind: "bool", label: "Bolge 1 Sikisma", plcTag: "ZN1_JAM_01_Sensor", alarm: { priority: "HIGH", text: "Bolge 1 sikisma algilandi" } },
  zn1_present:    { type: "DI", address: 4, kind: "bool", label: "Bolge 1 Malzeme Var", plcTag: "ZN1_PEY_01_Present" },
  zn2_sel_auto:   { type: "DI", address: 5, kind: "bool", label: "Bolge 2 Oto Secici", plcTag: "ZN2_SEL_02_Auto" },
  zn2_pb_start:   { type: "DI", address: 6, kind: "bool", label: "Bolge 2 Baslat", plcTag: "ZN2_PBS_02_Start" },
  zn2_pb_stop:    { type: "DI", address: 7, kind: "bool", label: "Bolge 2 Durdur", plcTag: "ZN2_PBS_02_Stop" },
  zn2_jam:        { type: "DI", address: 8, kind: "bool", label: "Bolge 2 Sikisma", plcTag: "ZN2_JAM_02_Sensor", alarm: { priority: "HIGH", text: "Bolge 2 sikisma algilandi" } },
  zn2_present:    { type: "DI", address: 9, kind: "bool", label: "Bolge 2 Malzeme Var", plcTag: "ZN2_PEY_02_Present" },
  zn3_sel_auto:   { type: "DI", address: 10, kind: "bool", label: "Bolge 3 Oto Secici", plcTag: "ZN3_SEL_03_Auto" },
  zn3_pb_start:   { type: "DI", address: 11, kind: "bool", label: "Bolge 3 Baslat", plcTag: "ZN3_PBS_03_Start" },
  zn3_pb_stop:    { type: "DI", address: 12, kind: "bool", label: "Bolge 3 Durdur", plcTag: "ZN3_PBS_03_Stop" },
  zn3_jam:        { type: "DI", address: 13, kind: "bool", label: "Bolge 3 Sikisma", plcTag: "ZN3_JAM_03_Sensor", alarm: { priority: "HIGH", text: "Bolge 3 sikisma algilandi" } },
  zn3_present:    { type: "DI", address: 14, kind: "bool", label: "Bolge 3 Malzeme Var", plcTag: "ZN3_PEY_03_Present" },
  // PLT_EST_01_OK: NC=1 saglikli. Deger 0 ise acil durdurma devrede -> alarm.
  estop_ok:       { type: "DI", address: 15, kind: "bool", invertAlarm: true, label: "Acil Durdurma Zinciri", plcTag: "PLT_EST_01_OK", alarm: { priority: "CRITICAL", text: "Acil durdurma devrede / zincir kopuk" } },
  reset_pb:       { type: "DI", address: 16, kind: "bool", label: "Reset Butonu", plcTag: "PLT_RST_01_PB" },
  permit_run:     { type: "DI", address: 17, kind: "bool", invertAlarm: true, label: "Calistirma Izni", plcTag: "PLT_PMT_01_Run", alarm: { priority: "CRITICAL", text: "Koruma kapisi acik / calistirma izni yok" } },

  // -------------------------------------------------------------------------
  // AI -> INPUT REGISTER (FC04 oku, salt okunur) — io_list %IW girisleri
  //   4-20mA takometre: 4mA=0, 20mA=120 m/min
  // -------------------------------------------------------------------------
  zn1_speed: { type: "IR", address: 0, kind: "analog", unit: "m/dk", decode: (raw) => scale4_20mA(raw, 0, 120), label: "Bolge 1 Hiz", plcTag: "ZN1_TAC_01_Speed" },
  zn2_speed: { type: "IR", address: 1, kind: "analog", unit: "m/dk", decode: (raw) => scale4_20mA(raw, 0, 120), label: "Bolge 2 Hiz", plcTag: "ZN2_TAC_02_Speed" },
  zn3_speed: { type: "IR", address: 2, kind: "analog", unit: "m/dk", decode: (raw) => scale4_20mA(raw, 0, 120), label: "Bolge 3 Hiz", plcTag: "ZN3_TAC_03_Speed" },

  // -------------------------------------------------------------------------
  // HOLDING REGISTER (FC03 oku / FC06 yaz) — setpoint ve komutlar
  //   io_list'te yok; tipik bir HMI'da operatorun yazdigi degerler buraya.
  //   scale:10 -> kullanici 45.0 girer, register'a 450 yazilir.
  // -------------------------------------------------------------------------
  zn1_speed_sp: { type: "HR", address: 0, writable: true, kind: "analog", scale: 10, unit: "m/dk", min: 0, max: 120, step: 0.5, label: "Bolge 1 Hiz Setpoint" },
  zn2_speed_sp: { type: "HR", address: 1, writable: true, kind: "analog", scale: 10, unit: "m/dk", min: 0, max: 120, step: 0.5, label: "Bolge 2 Hiz Setpoint" },
  zn3_speed_sp: { type: "HR", address: 2, writable: true, kind: "analog", scale: 10, unit: "m/dk", min: 0, max: 120, step: 0.5, label: "Bolge 3 Hiz Setpoint" },
};

// ============================================================================
//  Okuma bloklarini TAG_MAP'ten otomatik cikar.
//  Her adres uzayi icin min..max araligini bulup TEK blok olarak okuruz
//  (knowledge Optimizasyon madde 1: bitisik register'lari tek istekte oku).
//  Adres uzayinda buyuk delikler varsa burayi elle bloklara bolun (Not 5).
// ============================================================================
function buildBlock(type) {
  const addrs = Object.values(TAG_MAP)
    .filter((t) => t.type === type)
    .map((t) => t.address);
  if (addrs.length === 0) return null;
  const start = Math.min(...addrs);
  const end = Math.max(...addrs);
  return { start, count: end - start + 1 };
}

export const READ_BLOCKS = {
  COIL: buildBlock("COIL"),
  DI: buildBlock("DI"),
  IR: buildBlock("IR"),
  HR: buildBlock("HR"),
};

/**
 * Ham Modbus okuma sonuclarini tag -> deger sozlugune cevirir.
 * @param {object} raw { coils:[], discrete:[], input:[], holding:[] } (blok offsetli diziler)
 * @returns {Record<string, {value:any, raw:number}>}
 */
export function decodeAll(raw) {
  const out = {};
  for (const [tag, def] of Object.entries(TAG_MAP)) {
    const block = READ_BLOCKS[def.type];
    if (!block) continue;
    const idx = def.address - block.start;

    let arr;
    switch (def.type) {
      case "COIL": arr = raw.coils; break;
      case "DI": arr = raw.discrete; break;
      case "IR": arr = raw.input; break;
      case "HR": arr = raw.holding; break;
    }
    if (!arr || arr[idx] === undefined) continue;

    const rawVal = arr[idx];
    let value;
    if (def.kind === "bool") {
      value = !!rawVal;
    } else if (def.decode) {
      value = def.decode(rawVal);
    } else if (def.scale) {
      value = toInt16(rawVal) / def.scale;
    } else {
      value = toInt16(rawVal);
    }
    out[tag] = { value, raw: rawVal };
  }
  return out;
}

/**
 * Bir DI/COIL tag'inin "alarm aktif" olup olmadigini hesaplar.
 * invertAlarm=true ise deger FALSE oldugunda alarm aktif (orn. NC saglikli sinyal).
 */
export function isAlarmActive(def, value) {
  if (!def.alarm) return false;
  return def.invertAlarm ? value === false : value === true;
}
