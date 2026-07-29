import { DARAJA_NOM } from "../data.js";
import { ARAB, DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

export default function SuraRoyxati({ r, suralar, ochish, yop }) {
  const guruh = (d) => suralar.filter((s) => s.daraja === d);

  return (
    <Oyna
      r={r}
      sarlavha="Qisqa suralar"
      ost={`${suralar.length} ta sura`}
      yop={yop}
      bolalar={
        <>
          {Object.keys(DARAJA_NOM).map((d) => (
            <div key={d} style={{ marginBottom: 20 }}>
              <p style={{ marginBottom: 10, fontFamily: UTIL, fontSize: 9, letterSpacing: ".18em", color: r.xira, textTransform: "uppercase" }}>
                {DARAJA_NOM[d]}
              </p>
              <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
                {guruh(d).map((s) => (
                  <button
                    key={s.raqam}
                    onClick={() => ochish(s)}
                    style={{
                      display: "flex", alignItems: "center", justifyContent: "space-between",
                      padding: "12px 16px", borderRadius: 3, background: `${r.matn}0A`,
                      border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
                    }}
                  >
                    <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
                      <span style={{ flexShrink: 0, minWidth: 22, fontFamily: UTIL, fontSize: 10.5, color: r.xira }}>{s.raqam}</span>
                      <div>
                        <p style={{ fontFamily: DISPLAY, fontSize: 16, color: r.matn, margin: 0 }}>{s.nom_uz}</p>
                        <p style={{ fontFamily: UTIL, fontSize: 10.5, color: r.xira, margin: 0 }}>{s.oyat_soni} oyat</p>
                      </div>
                    </div>
                    <span style={{ fontFamily: ARAB, fontSize: 17, color: r.urgu }}>{s.nom_ar}</span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </>
      }
    />
  );
}
