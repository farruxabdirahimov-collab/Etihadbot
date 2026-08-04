import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

export default function SozlamaOyna({ r, shaharNomi, sozlamalar, yop, ochShahar, ochBildirishnoma, ochFikr }) {
  const eslatmaMatni = sozlamalar.eslatma_yoqilgan
    ? `${sozlamalar.eslatma_namozlar.length} ta namoz uchun yoqilgan`
    : "o'chirilgan";

  return (
    <Oyna
      r={r}
      sarlavha="Sozlamalar"
      yop={yop}
      bolalar={
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <button
            onClick={ochShahar}
            style={{
              display: "flex", alignItems: "center", justifyContent: "space-between",
              padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`,
              border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
            }}
          >
            <div>
              <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5, textTransform: "uppercase" }}>Shahar</p>
              <p style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, margin: 0 }}>{shaharNomi}</p>
            </div>
            <span style={{ fontSize: 14, color: r.xira }}>›</span>
          </button>

          <button
            onClick={ochBildirishnoma}
            style={{
              display: "flex", alignItems: "center", justifyContent: "space-between",
              padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`,
              border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
            }}
          >
            <div>
              <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5, textTransform: "uppercase" }}>Bildirishnoma</p>
              <p style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, margin: 0 }}>{eslatmaMatni}</p>
            </div>
            <span style={{ fontSize: 14, color: r.xira }}>›</span>
          </button>

          <button
            onClick={ochFikr}
            style={{
              display: "flex", alignItems: "center", justifyContent: "space-between",
              padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`,
              border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
            }}
          >
            <div>
              <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5, textTransform: "uppercase" }}>Fikr va takliflar</p>
              <p style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, margin: 0 }}>xato yoki taklif yuborish</p>
            </div>
            <span style={{ fontSize: 14, color: r.xira }}>›</span>
          </button>

          <p style={{ marginTop: 12, fontFamily: UTIL, fontSize: 10.5, lineHeight: 1.6, color: r.xira, opacity: 0.75 }}>
            Sozlamalar Telegram botdagi /sozlama va /bildirishnoma buyruqlari
            bilan bir xil — qaysi biridan foydalansangiz ham darhol saqlanadi.
          </p>
        </div>
      }
    />
  );
}
