// ============================================================
// commands.js — Yazma komutları (client → server)
// ------------------------------------------------------------
// Butona basınca WSClient üzerinden bir write mesajı gönderir.
// İki davranış:
//   - kind: 'pulse'  → değeri yaz, kısa süre sonra otomatik false yaz
//                       (RESET gibi tek atımlık komutlar için).
//   - kind: 'toggle' → değeri yaz (gateway/PLC durumu yönetir).
//
// Güvenlik: bağlantı CONNECTED değilse buton zaten kilitli (ui.js),
// burada da ikinci kontrol yapılır. Gönderim başarısızsa kullanıcı
// görsel uyarı alır.
// ============================================================

window.Commands = (function () {
    'use strict';

    const WS = window.WSClient;
    const PULSE_MS = 400; // pulse komutlarda otomatik geri-alma süresi

    function execute(cmd, btn) {
        // Bağlantı güvenliği
        if (WS.getStatus() !== WS.STATUS.CONNECTED) {
            flash(btn, 'fail');
            console.warn('Komut iptal: bağlantı CONNECTED değil.');
            return;
        }

        const ok = WS.send({
            type: cmd.wtype,      // WRITE_COIL | WRITE_REGISTER
            tag: cmd.tag,
            value: cmd.value
            // Üretimde: sessionToken alanı burada eklenmeli (yetki).
        });

        if (!ok) {
            flash(btn, 'fail');
            return;
        }
        flash(btn, 'ok');

        // Pulse komut: kısa süre sonra karşıt değeri yaz (tek atım).
        if (cmd.kind === 'pulse') {
            const offValue = (typeof cmd.value === 'boolean') ? !cmd.value : 0;
            setTimeout(() => {
                WS.send({ type: cmd.wtype, tag: cmd.tag, value: offValue });
            }, PULSE_MS);
        }
    }

    // Butona kısa görsel geri bildirim (onay/başarısız).
    function flash(btn, kind) {
        if (!btn) return;
        const cls = kind === 'ok' ? 'cmd-ok' : 'cmd-fail';
        btn.classList.add(cls);
        setTimeout(() => btn.classList.remove(cls), 500);
    }

    return { execute };
})();
