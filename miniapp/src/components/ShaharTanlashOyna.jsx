import { useState } from "react";
import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

export default function ShaharTanlashOyna({ r, viloyatlar, yop, tanlash }) {
  const [tanlanganViloyat, setTanlanganViloyat] = useState(null);

  if (tanlanganViloyat) {
    return (
      <Oyna
        r={r}
        sarlavha={tanlanganViloyat.nom}
        ost="Shahringizni tanlang"
        yop={yop}
        bolalar={
          <>
            <button
              onClick={() => setTanlanganViloyat(null)}
              style={{ marginBottom: 16, fontFamily: UTIL, fontSize: 11.5, color: r.xira, background: "none", border: "none", cursor: "pointer", padding: 0 }}
            >
              ← Viloyatlar
            </button>
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              {tanlanganViloyat.shaharlar.map((sh) => (
                <button
                  key={sh.id}
                  onClick={() => tanlash(sh)}
                  style={{
                    padding: "12px 16px", borderRadius: 3, background: `${r.matn}0A`,
                    border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
                    fontFamily: DISPLAY, fontSize: 16, color: r.matn,
                  }}
                >
                  {sh.nom}
                </button>
              ))}
            </div>
          </>
        }
      />
    );
  }

  return (
    <Oyna
      r={r}
      sarlavha="Viloyatni tanlang"
      yop={yop}
      bolalar={
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
          {viloyatlar.map((v) => (
            <button
              key={v.nom}
              onClick={() => (v.shaharlar.length === 1 ? tanlash(v.shaharlar[0]) : setTanlanganViloyat(v))}
              style={{
                padding: "12px 14px", borderRadius: 3, background: `${r.matn}0A`,
                border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
                fontFamily: UTIL, fontSize: 12.5, color: r.matn,
              }}
            >
              {v.nom}
            </button>
          ))}
        </div>
      }
    />
  );
}
