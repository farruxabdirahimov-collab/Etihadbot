import { NAMOZ_TARTIBI, NOM_KORSATISH } from "../data.js";
import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

const DAQIQA_VARIANTLARI = [5, 10, 15, 20, 30];

function Katak({ r, belgilangan, onClick, matn }) {
  return (
    <button
      onClick={onClick}
      style={{
        display: "flex", alignItems: "center", gap: 10, width: "100%", padding: "10px 14px",
        borderRadius: 3, background: `${r.matn}0A`, border: `1px solid ${r.xira}2E`,
        cursor: "pointer", textAlign: "left", fontFamily: DISPLAY, fontSize: 15, color: r.matn,
      }}
    >
      <span>{belgilangan ? "✅" : "⬜️"}</span>
      {matn}
    </button>
  );
}

function DaqiqaTanlash({ r, tanlangan, onTanlash }) {
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
      {DAQIQA_VARIANTLARI.map((d) => (
        <button
          key={d}
          onClick={() => onTanlash(d)}
          style={{
            padding: "8px 12px", borderRadius: 2, fontFamily: UTIL, fontSize: 12,
            border: `1px solid ${tanlangan === d ? r.urgu : r.xira + "44"}`,
            background: tanlangan === d ? `${r.urgu}1F` : "transparent",
            color: tanlangan === d ? r.matn : r.xira, cursor: "pointer",
          }}
        >
          {d} daqiqa
        </button>
      ))}
    </div>
  );
}

export default function BildirishnomaOyna({ r, sozlamalar, yop, onYangilash }) {
  const tanlanganNamozlar = new Set(sozlamalar.eslatma_namozlar);

  function namozniAlmashtir(nom) {
    const yangi = new Set(tanlanganNamozlar);
    if (yangi.has(nom)) yangi.delete(nom);
    else yangi.add(nom);
    onYangilash({ eslatma_namozlar: Array.from(yangi) });
  }

  return (
    <Oyna
      r={r}
      sarlavha="Bildirishnoma sozlamalari"
      yop={yop}
      bolalar={
        <>
          <Katak
            r={r}
            belgilangan={sozlamalar.eslatma_yoqilgan}
            onClick={() => onYangilash({ eslatma_yoqilgan: !sozlamalar.eslatma_yoqilgan })}
            matn="Bildirishnoma yoqilgan"
          />

          <p style={{ margin: "18px 0 8px", fontSize: 9, letterSpacing: ".18em", color: r.xira, textTransform: "uppercase" }}>
            Qaysi namozlar uchun
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {NAMOZ_TARTIBI.map((nom) => (
              <Katak
                key={nom}
                r={r}
                belgilangan={tanlanganNamozlar.has(nom)}
                onClick={() => namozniAlmashtir(nom)}
                matn={NOM_KORSATISH[nom]}
              />
            ))}
          </div>

          <p style={{ margin: "18px 0 8px", fontSize: 9, letterSpacing: ".18em", color: r.xira, textTransform: "uppercase" }}>
            Necha daqiqa oldin
          </p>
          <DaqiqaTanlash
            r={r}
            tanlangan={sozlamalar.eslatma_daqiqa}
            onTanlash={(d) => onYangilash({ eslatma_daqiqa: d })}
          />

          <p style={{ margin: "18px 0 8px", fontSize: 9, letterSpacing: ".18em", color: r.xira, textTransform: "uppercase" }}>
            Vaqt tugash ogohlantirishi
          </p>
          <Katak
            r={r}
            belgilangan={sozlamalar.eslatma_tugash_yoqilgan}
            onClick={() => onYangilash({ eslatma_tugash_yoqilgan: !sozlamalar.eslatma_tugash_yoqilgan })}
            matn="Vaqt tugashidan oldin ham ogohlantirilsin"
          />
          {sozlamalar.eslatma_tugash_yoqilgan && (
            <div style={{ marginTop: 8 }}>
              <DaqiqaTanlash
                r={r}
                tanlangan={sozlamalar.eslatma_tugash_daqiqa}
                onTanlash={(d) => onYangilash({ eslatma_tugash_daqiqa: d })}
              />
            </div>
          )}
        </>
      }
    />
  );
}
