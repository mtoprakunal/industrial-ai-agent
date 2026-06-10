// ============================================================
// GVL_IO — Fiziksel Giris/Cikis degiskenleri
// Adresler io_list.csv ile BIREBIR tutarli olmalidir.
// Tek-yazar disiplini: cikislari yalniz ilgili PRG yazar.
// ============================================================
{attribute 'qualified_only'}
VAR_GLOBAL
    // --- Dijital Girisler (DI) ---
    ZN1_SEL_01_Auto    AT %IX0.0 : BOOL;   // Bolge 1 Oto/Manuel
    ZN1_PBS_01_Start   AT %IX0.1 : BOOL;
    ZN1_PBS_01_Stop    AT %IX0.2 : BOOL;   // NC: 1=normal, 0=basili
    ZN1_JAM_01_Sensor  AT %IX0.3 : BOOL;
    ZN1_PEY_01_Present AT %IX0.4 : BOOL;
    ZN2_SEL_02_Auto    AT %IX0.5 : BOOL;
    ZN2_PBS_02_Start   AT %IX0.6 : BOOL;
    ZN2_PBS_02_Stop    AT %IX0.7 : BOOL;
    ZN2_JAM_02_Sensor  AT %IX1.0 : BOOL;
    ZN2_PEY_02_Present AT %IX1.1 : BOOL;
    ZN3_SEL_03_Auto    AT %IX1.2 : BOOL;
    ZN3_PBS_03_Start   AT %IX1.3 : BOOL;
    ZN3_PBS_03_Stop    AT %IX1.4 : BOOL;
    ZN3_JAM_03_Sensor  AT %IX1.5 : BOOL;
    ZN3_PEY_03_Present AT %IX1.6 : BOOL;
    PLT_EST_01_OK      AT %IX1.7 : BOOL;   // Acil durdurma zinciri saglam (NC=1)
    PLT_RST_01_PB      AT %IX2.0 : BOOL;   // Reset / hata kabul
    PLT_PMT_01_Run     AT %IX2.1 : BOOL;   // Calistirma izni (NC)

    // --- Dijital Cikislar (DO) ---
    ZN1_MTR_01_Run     AT %QX0.0 : BOOL;
    ZN1_LMP_01_Run     AT %QX0.1 : BOOL;
    ZN1_LMP_01_Flt     AT %QX0.2 : BOOL;
    ZN2_MTR_02_Run     AT %QX0.3 : BOOL;
    ZN2_LMP_02_Run     AT %QX0.4 : BOOL;
    ZN2_LMP_02_Flt     AT %QX0.5 : BOOL;
    ZN3_MTR_03_Run     AT %QX0.6 : BOOL;
    ZN3_LMP_03_Run     AT %QX0.7 : BOOL;
    ZN3_LMP_03_Flt     AT %QX1.0 : BOOL;
    PLT_BCN_01_Run     AT %QX1.1 : BOOL;
    PLT_BCN_01_Flt     AT %QX1.2 : BOOL;
    PLT_HRN_01_Alarm   AT %QX1.3 : BOOL;

    // --- Analog Girisler (AI) — 4-20mA takometre ---
    ZN1_TAC_01_Speed   AT %IW2 : INT;
    ZN2_TAC_02_Speed   AT %IW3 : INT;
    ZN3_TAC_03_Speed   AT %IW4 : INT;
END_VAR
