import { NAMOZLAR } from "../data.js";
import { keyingiNamozniHisobla, rangniAniqla } from "../hisoblash.js";
import { ARAB, DISPLAY, HALQA_RADIUS, HALQA_UZUNLIK, UTIL, ikki } from "../theme.js";

function qolganMatni(soniya) {
  const daq = Math.floor(soniya / 60);
  const son = soniya % 60;
  return `${ikki(daq)}:${ikki(son)}`;
}

export default function BoshEkran({ vaqtlar, hozir, daraja, suralar, ochRoyxat, ochQoida, ochSura }) {
  const keyingiNamoz = keyingiNamozniHisobla(vaqtlar, hozir);
  const qolganSoniya = keyingiNamoz ? Math.max(0, Math.round((keyingiNamoz.vaqt - hozir) / 1000)) : null;
  const oynaSoniya = keyingiNamoz?.oldingiVaqt
    ? Math.round((keyingiNamoz.vaqt - keyingiNamoz.oldingiVaqt) / 1000)
    : 40 * 60;
  const ulush = qolganSoniya === null ? 0 : Math.max(0, Math.min(1, qolganSoniya / oynaSoniya));
  const r = rangniAniqla(qolganSoniya);

  const joriyNamoz = keyingiNamoz ? NAMOZLAR[keyingiNamoz.indeks] : null;
  const tavsiyaRaqam = joriyNamoz?.sura?.[daraja];
  const tavsiyaSura = suralar.find((s) => s.raqam === tavsiyaRaqam);

  return (
    <div style={{ maxWidth: 480, margin: "0 auto", padding: "20px 20px 40px" }}>
      <div style={{ marginBottom: 4, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <p style={{ fontFamily: DISPLAY, fontSize: 16, color: r.matn, margin: 0 }}>{vaqtlar.shahar}</p>
        <p style={{ fontFamily: DISPLAY, fontSize: 22, color: r.matn, margin: 0 }}>
          {ikki(hozir.getHours())}
          <span style={{ color: r.xira }}>:</span>
          {ikki(hozir.getMinutes())}
          <span style={{ color: r.xira, fontSize: 15 }}>:{ikki(hozir.getSeconds())}</span>
        </p>
      </div>
      <div style={{ marginBottom: 24, paddingBottom: 12, borderBottom: `1px solid ${r.xira}22` }} />

      <div style={{ marginBottom: 20, display: "flex", justifyContent: "center" }}>
        <div style={{ position: "relative", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <svg width="248" height="248" style={{ transform: "rotate(-90deg)" }}>
            <circle cx="124" cy="124" r={HALQA_RADIUS} fill="none" stroke={r.xira} strokeWidth="1" opacity="0.22" />
            <circle
              cx="124" cy="124" r={HALQA_RADIUS} fill="none" stroke={r.urgu} strokeWidth="2.5" strokeLinecap="round"
              strokeDasharray={HALQA_UZUNLIK} strokeDashoffset={HALQA_UZUNLIK * (1 - ulush)}
              style={{ transition: "stroke-dashoffset .9s linear" }}
            />
          </svg>
          <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            {joriyNamoz ? (
              <>
                <p style={{ fontFamily: ARAB, fontSize: 19, color: r.xira, marginBottom: 2 }}>{joriyNamoz.arab}</p>
                <p style={{ fontFamily: DISPLAY, fontSize: 25, color: r.matn, marginBottom: 8 }}>{joriyNamoz.nom}</p>
                <p style={{ fontFamily: DISPLAY, fontSize: 50, color: r.urgu, lineHeight: 1 }}>{qolganMatni(qolganSoniya)}</p>
                <p style={{ fontSize: 8.5, letterSpacing: ".2em", color: r.xira, marginTop: 8, textTransform: "uppercase" }}>qoldi</p>
              </>
            ) : (
              <p style={{ fontFamily: DISPLAY, fontSize: 20, color: r.matn, textAlign: "center", padding: "0 24px" }}>
                Bugungi namozlar tugadi
              </p>
            )}
          </div>
        </div>
      </div>

      <p style={{ marginBottom: 20, textAlign: "center", fontSize: 9.5, letterSpacing: ".22em", color: r.xira, textTransform: "uppercase" }}>
        {r.holat}
      </p>

      {joriyNamoz && (
        <div style={{ marginBottom: 20, display: "flex", flexWrap: "wrap", alignItems: "center", justifyContent: "center", gap: 6 }}>
          {joriyNamoz.rakat.map((x, i) => {
            const asosiy = x.turi === "farz" || x.turi === "vitr";
            return (
              <div
                key={i}
                style={{
                  display: "flex", alignItems: "baseline", gap: 6, padding: "8px 12px", borderRadius: 2,
                  border: `1px solid ${asosiy ? r.urgu + "88" : r.xira + "44"}`,
                  background: asosiy ? `${r.urgu}14` : "transparent",
                }}
              >
                <span style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, lineHeight: 1 }}>{x.soni}</span>
                <span style={{ fontSize: 9, letterSpacing: ".16em", color: asosiy ? r.urgu : r.xira, fontWeight: asosiy ? 700 : 500, textTransform: "uppercase" }}>
                  {x.turi}
                </span>
              </div>
            );
          })}
        </div>
      )}

      {joriyNamoz && (
        <div style={{ marginBottom: 20, display: "flex", justifyContent: "center" }}>
          <button
            onClick={ochQoida}
            style={{ fontFamily: UTIL, fontSize: 10.5, color: r.xira, background: "none", border: "none", cursor: "pointer", borderBottom: `1px dotted ${r.xira}88` }}
          >
            qanday o'qiladi?
          </button>
        </div>
      )}

      {tavsiyaSura && (
        <button
          onClick={() => ochSura(tavsiyaSura)}
          style={{ marginBottom: 10, display: "flex", width: "100%", alignItems: "center", justifyContent: "space-between", padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`, border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left" }}
        >
          <div>
            <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5, textTransform: "uppercase" }}>Tavsiya etilgan zam sura</p>
            <p style={{ fontFamily: DISPLAY, fontSize: 20, color: r.matn, margin: 0 }}>{tavsiyaSura.nom_uz}</p>
          </div>
          <span style={{ fontSize: 14, color: r.xira }}>›</span>
        </button>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        <button
          onClick={ochRoyxat}
          style={{ padding: "14px 16px", borderRadius: 3, background: `${r.urgu}12`, border: `1px solid ${r.urgu}4D`, cursor: "pointer", textAlign: "left" }}
        >
          <p style={{ fontFamily: DISPLAY, fontSize: 15, color: r.matn, marginBottom: 3 }}>Qisqa suralar</p>
          <p style={{ fontSize: 11, color: r.xira, margin: 0 }}>{suralar.length} ta · oflayn</p>
        </button>
        {["Qazo namozlar", "Qibla"].map((nom) => (
          <div key={nom} style={{ padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`, border: `1px solid ${r.xira}2E` }}>
            <p style={{ fontFamily: DISPLAY, fontSize: 15, color: r.matn, marginBottom: 3 }}>{nom}</p>
            <p style={{ fontSize: 11, color: r.xira, margin: 0 }}>Tez orada</p>
          </div>
        ))}
      </div>

      <p style={{ marginTop: 20, textAlign: "center", fontSize: 9.5, lineHeight: 1.6, color: r.xira, opacity: 0.7 }}>
        Namoz vaqtlari manbasi: namozvaqti.uz
        <br />
        «Book Media Nashr» taqvim kitobi asosida
      </p>
    </div>
  );
}
