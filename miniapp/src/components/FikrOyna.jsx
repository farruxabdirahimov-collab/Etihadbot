import { useState } from "react";
import { api } from "../api.js";
import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

const CHEGARA = 1000;

export default function FikrOyna({ r, yop }) {
  const [matn, setMatn] = useState("");
  const [holat, setHolat] = useState("yozilmoqda"); // yozilmoqda | yuborilmoqda | yuborildi
  const [xato, setXato] = useState("");

  async function yubor() {
    if (matn.trim().length < 3) return;
    setHolat("yuborilmoqda");
    setXato("");
    try {
      await api.fikrYubor(matn.trim());
      setHolat("yuborildi");
    } catch (e) {
      setXato(e.message);
      setHolat("yozilmoqda");
    }
  }

  if (holat === "yuborildi") {
    return (
      <Oyna
        r={r}
        sarlavha="Rahmat!"
        yop={yop}
        bolalar={
          <div style={{ padding: "20px 0", textAlign: "center" }}>
            <p style={{ fontSize: 40, margin: "0 0 12px" }}>✅</p>
            <p style={{ fontFamily: DISPLAY, fontSize: 17, color: r.matn, marginBottom: 8 }}>
              Fikringiz yuborildi
            </p>
            <p style={{ fontFamily: UTIL, fontSize: 12.5, lineHeight: 1.65, color: r.xira }}>
              Har bir taklif ilovani yaxshilashga yordam beradi. Vaqt
              ajratganingiz uchun rahmat.
            </p>
          </div>
        }
      />
    );
  }

  const yuborilmoqda = holat === "yuborilmoqda";
  const tayyor = matn.trim().length >= 3 && !yuborilmoqda;

  return (
    <Oyna
      r={r}
      sarlavha="Fikr va takliflar"
      ost="To'g'ridan-to'g'ri ishlab chiquvchiga yetadi"
      yop={yop}
      bolalar={
        <>
          <p style={{ fontFamily: UTIL, fontSize: 12.5, lineHeight: 1.65, color: r.xira, marginBottom: 12 }}>
            Xatolik topdingizmi yoki taklifingiz bormi? Yozing — ilovani
            birgalikda yaxshilaymiz.
          </p>

          <textarea
            value={matn}
            onChange={(e) => setMatn(e.target.value.slice(0, CHEGARA))}
            placeholder="Masalan: Namoz vaqti shahrimda 2 daqiqa farq qilyapti..."
            rows={6}
            style={{
              width: "100%", boxSizing: "border-box", padding: "12px 14px",
              borderRadius: 3, background: `${r.matn}0A`, border: `1px solid ${r.xira}44`,
              color: r.matn, fontFamily: UTIL, fontSize: 14, lineHeight: 1.6,
              resize: "vertical", outline: "none",
            }}
          />

          <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 4, marginBottom: 12 }}>
            <span style={{ fontFamily: UTIL, fontSize: 10.5, color: r.xira }}>
              {matn.length} / {CHEGARA}
            </span>
          </div>

          {xato && (
            <p style={{ fontFamily: UTIL, fontSize: 12, lineHeight: 1.6, color: r.matn, background: `${r.urgu}18`, border: `1px solid ${r.urgu}55`, borderRadius: 3, padding: "10px 12px", marginBottom: 12 }}>
              {xato}
            </p>
          )}

          <button
            onClick={yubor}
            disabled={!tayyor}
            style={{
              width: "100%", padding: "13px 16px", borderRadius: 3,
              background: tayyor ? r.urgu : `${r.xira}22`,
              border: "none", color: tayyor ? r.past : r.xira,
              fontFamily: UTIL, fontSize: 14, fontWeight: 700,
              cursor: tayyor ? "pointer" : "default",
            }}
          >
            {yuborilmoqda ? "Yuborilmoqda..." : "Yuborish"}
          </button>
        </>
      }
    />
  );
}
