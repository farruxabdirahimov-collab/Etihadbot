import { QOIDA } from "../data.js";
import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

export default function QoidaOyna({ r, yop }) {
  return (
    <Oyna
      r={r}
      sarlavha="Namoz qanday o'qiladi"
      ost="Ikki rakatli namoz misolida"
      yop={yop}
      bolalar={
        <>
          {QOIDA.map((q) => (
            <div key={q.n} style={{ marginBottom: 14, display: "flex", gap: 12 }}>
              <span
                style={{
                  flexShrink: 0, fontFamily: UTIL, fontSize: 10, color: r.urgu,
                  border: `1px solid ${r.urgu}55`, borderRadius: 2, width: 22, height: 22,
                  display: "flex", alignItems: "center", justifyContent: "center", marginTop: 2,
                }}
              >
                {q.n}
              </span>
              <div>
                <p style={{ fontFamily: DISPLAY, fontSize: 15.5, color: r.matn, marginBottom: 2 }}>{q.nom}</p>
                <p style={{ fontFamily: UTIL, fontSize: 12, lineHeight: 1.65, color: r.xira, margin: 0 }}>{q.izoh}</p>
              </div>
            </div>
          ))}
          <div style={{ marginTop: 16, padding: "14px 16px", borderRadius: 3, background: `${r.urgu}12`, border: `1px solid ${r.urgu}44` }}>
            <p style={{ fontFamily: UTIL, fontSize: 11.5, lineHeight: 1.65, color: r.xira, margin: 0 }}>
              Bu qisqacha tartib. To'rt rakatli namozlarda 3–7-qadamlar to'rt marta
              takrorlanadi. Fiqhiy tafsilotlar mazhabga qarab farq qilishi mumkin —
              aniq qoidani ustozingizdan so'rang.
            </p>
          </div>
        </>
      }
    />
  );
}
