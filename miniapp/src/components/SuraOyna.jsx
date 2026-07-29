import { ARAB, DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

export default function SuraOyna({ r, sura, yop, orqaga }) {
  if (!sura) return null;
  const yuklanmoqda = !sura.matn;

  return (
    <Oyna
      r={r}
      sarlavha={`${sura.nom_uz} surasi`}
      ost={`${sura.raqam}-sura · ${sura.oyat_soni} oyat`}
      yop={yop}
      bolalar={
        <>
          <button
            onClick={orqaga}
            style={{
              marginBottom: 16, fontFamily: UTIL, fontSize: 11.5, color: r.xira,
              background: "none", border: "none", cursor: "pointer", padding: 0,
            }}
          >
            ← Ro'yxat
          </button>

          {yuklanmoqda && (
            <p style={{ fontFamily: UTIL, fontSize: 13, color: r.xira, textAlign: "center", padding: "24px 0" }}>
              Yuklanmoqda...
            </p>
          )}

          {!yuklanmoqda && sura.raqam !== 9 && (
            <p style={{ marginBottom: 20, textAlign: "center", fontFamily: ARAB, fontSize: 19, color: r.xira, direction: "rtl" }}>
              بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
            </p>
          )}

          {!yuklanmoqda &&
            sura.matn.map((o) => (
              <div key={o.oyat} style={{ marginBottom: 16, paddingBottom: 16, borderBottom: `1px solid ${r.xira}1F` }}>
                <div style={{ display: "flex", alignItems: "flex-start", gap: 12, direction: "rtl" }}>
                  <span
                    style={{
                      flexShrink: 0, fontFamily: UTIL, fontSize: 10, color: r.urgu,
                      border: `1px solid ${r.urgu}55`, borderRadius: 99, width: 20, height: 20,
                      display: "flex", alignItems: "center", justifyContent: "center", marginTop: 6,
                    }}
                  >
                    {o.oyat}
                  </span>
                  <p style={{ fontFamily: ARAB, fontSize: 23, lineHeight: 2, color: r.matn, margin: 0 }}>{o.arab}</p>
                </div>
              </div>
            ))}

          {!yuklanmoqda && (
            <p style={{ fontFamily: UTIL, fontSize: 10.5, lineHeight: 1.6, color: r.xira, opacity: 0.75 }}>
              Matn manbasi: Usmoniy mushaf (alquran.cloud). To'g'ri o'qilishini ustozdan o'rganing.
            </p>
          )}
        </>
      }
    />
  );
}
