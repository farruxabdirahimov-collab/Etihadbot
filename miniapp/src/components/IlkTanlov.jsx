import { useState } from "react";
import { DISPLAY, UTIL } from "../theme.js";

export default function IlkTanlov({ r, viloyatlar, tanlash }) {
  const [viloyat, setViloyat] = useState(null);
  const royxat = viloyat ? viloyat.shaharlar : viloyatlar;

  return (
    <div style={{ maxWidth: 480, margin: "0 auto", padding: "36px 20px 40px" }}>
      <p style={{ textAlign: "center", fontSize: 34, margin: "0 0 10px" }}>🌙</p>
      <h1 style={{ fontFamily: DISPLAY, fontSize: 24, color: r.matn, textAlign: "center", margin: "0 0 8px" }}>
        Etihat — E'tiqod
      </h1>
      <p style={{ fontFamily: UTIL, fontSize: 13, lineHeight: 1.65, color: r.xira, textAlign: "center", marginBottom: 28 }}>
        Namoz vaqtlari va namozni o'rganish uchun ilova.
        <br />
        Boshlash uchun shahringizni tanlang.
      </p>

      {viloyat && (
        <button
          onClick={() => setViloyat(null)}
          style={{
            marginBottom: 14, fontFamily: UTIL, fontSize: 12, color: r.xira,
            background: "none", border: "none", cursor: "pointer", padding: 0,
          }}
        >
          ← Viloyatlar
        </button>
      )}

      <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 10, textTransform: "uppercase" }}>
        {viloyat ? viloyat.nom : "Viloyatingiz"}
      </p>

      <div style={{ display: "grid", gridTemplateColumns: viloyat ? "1fr" : "1fr 1fr", gap: 8 }}>
        {royxat.map((element) =>
          viloyat ? (
            <button
              key={element.id}
              onClick={() => tanlash(element)}
              style={{
                padding: "13px 16px", borderRadius: 3, background: `${r.matn}0A`,
                border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
                fontFamily: DISPLAY, fontSize: 16, color: r.matn,
              }}
            >
              {element.nom}
            </button>
          ) : (
            <button
              key={element.nom}
              onClick={() => (element.shaharlar.length === 1 ? tanlash(element.shaharlar[0]) : setViloyat(element))}
              style={{
                padding: "12px 14px", borderRadius: 3, background: `${r.matn}0A`,
                border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
                fontFamily: UTIL, fontSize: 12.5, color: r.matn,
              }}
            >
              {element.nom}
            </button>
          )
        )}
      </div>

      {viloyatlar.length === 0 && (
        <p style={{ fontFamily: UTIL, fontSize: 13, color: r.xira, textAlign: "center", padding: "20px 0" }}>
          Shaharlar ro'yxati yuklanmadi. Internetni tekshirib, sahifani yangilang.
        </p>
      )}

      <p style={{ marginTop: 28, textAlign: "center", fontSize: 9.5, lineHeight: 1.6, color: r.xira, opacity: 0.7 }}>
        Namoz vaqtlari manbasi: namozvaqti.uz
        <br />
        «Book Media Nashr» taqvim kitobi asosida
      </p>
    </div>
  );
}
