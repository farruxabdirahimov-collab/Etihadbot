import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

function Band({ r, sarlavha, qiymat, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "14px 16px", borderRadius: 3, background: `${r.matn}0A`,
        border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
      }}
    >
      <div>
        <p style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5, textTransform: "uppercase" }}>
          {sarlavha}
        </p>
        <p style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, margin: 0 }}>{qiymat}</p>
      </div>
      <span style={{ fontSize: 14, color: r.xira }}>›</span>
    </button>
  );
}

export default function SozlamaOyna({
  r, shaharNomi, sozlamalar, mehmon, yop, ochShahar, ochBildirishnoma, ochFikr, botniOch,
}) {
  const eslatmaMatni = sozlamalar?.eslatma_yoqilgan
    ? `${sozlamalar.eslatma_namozlar.length} ta namoz uchun yoqilgan`
    : "o'chirilgan";

  return (
    <Oyna
      r={r}
      sarlavha="Sozlamalar"
      yop={yop}
      bolalar={
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <Band r={r} sarlavha="Shahar" qiymat={shaharNomi} onClick={ochShahar} />

          {mehmon ? (
            <>
              <Band
                r={r}
                sarlavha="Bildirishnoma"
                qiymat="Telegram orqali yoqiladi"
                onClick={botniOch}
              />
              <p style={{ fontFamily: UTIL, fontSize: 11, lineHeight: 1.65, color: r.xira, margin: "2px 2px 8px" }}>
                Namoz vaqti eslatmalari Telegram bot orqali yuboriladi. Botni
                bir marta ochsangiz, eslatmalarni o'zingizga moslab
                sozlashingiz mumkin.
              </p>
            </>
          ) : (
            <Band r={r} sarlavha="Bildirishnoma" qiymat={eslatmaMatni} onClick={ochBildirishnoma} />
          )}

          <Band
            r={r}
            sarlavha="Fikr va takliflar"
            qiymat="xato yoki taklif yuborish"
            onClick={ochFikr}
          />

          <p style={{ marginTop: 12, fontFamily: UTIL, fontSize: 10.5, lineHeight: 1.6, color: r.xira, opacity: 0.75 }}>
            {mehmon
              ? "Tanlovingiz shu qurilmada saqlanadi. Telegram orqali kirsangiz, sozlamalar barcha qurilmalaringizda bir xil bo'ladi."
              : "Sozlamalar Telegram botdagi /sozlama va /bildirishnoma buyruqlari bilan bir xil — qaysi biridan foydalansangiz ham darhol saqlanadi."}
          </p>
        </div>
      }
    />
  );
}
