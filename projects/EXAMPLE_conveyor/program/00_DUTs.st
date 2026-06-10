// ============================================================
// DUT (Data Unit Types) — Numaralandirmalar
// Proje: EXAMPLE_Conveyor_Line1
// Aciklama: Bolge mod ve durum makinesi tipleri
// ============================================================

// Bolge calisma modu
TYPE E_ZoneMode :
(
    MODE_MANUAL := 0,   // Operator buton ile kontrol
    MODE_AUTO   := 1    // Otomatik sira / fotosel ile
) := MODE_MANUAL;
END_TYPE

// Bolge durum makinesi
TYPE E_ZoneState :
(
    STATE_IDLE     := 0,    // Bekliyor, motor kapali
    STATE_STARTING := 1,    // Baslatma gecisi
    STATE_RUNNING  := 2,    // Calisiyor
    STATE_STOPPING := 3,    // Durdurma gecisi
    STATE_JAMMED   := 4,    // Sikisma - reset bekliyor
    STATE_FAULT    := 5     // Hata (hiz/diger) - reset bekliyor
) := STATE_IDLE;
END_TYPE
