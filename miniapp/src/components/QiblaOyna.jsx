import { useEffect, useRef, useState } from "react";
import { kompasniYoq } from "../kompas.js";
import { DISPLAY, UTIL } from "../theme.js";
import Oyna from "./Oyna.jsx";

const OLCHAM = 230;
const M = OLCHAM / 2;
const RADIUS = M - 18;

// «Shimol» va «Sharq» bir harf bilan boshlangani uchun qisqartma o'rniga
// to'liq so'z yoziladi — chalkashlik bo'lmasin.
const RUMBLAR = [
  { belgi: "Shimol", burchak: 0 },
  { belgi: "Sharq", burchak: 90 },
  { belgi: "Janub", burchak: 180 },
  { belgi: "G'arb", burchak: 270 },
];

function nuqta(burchak, masofa) {
  const rad = ((burchak - 90) * Math.PI) / 180;
  return [M + masofa * Math.cos(rad), M + masofa * Math.sin(rad)];
}

export default function QiblaOyna({ r, qibla, yop }) {
  const [yonalish, setYonalish] = useState(null); // null = kompas o'chiq
  const [kompasXato, setKompasXato] = useState(false);
  const tozalash = useRef(null);

  useEffect(() => () => tozalash.current?.(), []);

  async function kompasniIshgaTushir() {
    const toxtat = await kompasniYoq((h) => setYonalish(h));
    if (toxtat) {
      tozalash.current = toxtat;
    } else {
      setKompasXato(true);
    }
  }

  const kompasFaol = yonalish !== null;
  // Kompas faol bo'lsa rozetkani teskari buramiz — shunda «SH» haqiqiy
  // shimolga qaraydi va qibla strelkasi o'z-o'zidan to'g'ri joyni ko'rsatadi.
  const rozetkaBurchagi = kompasFaol ? -yonalish : 0;
  const [uchX, uchY] = nuqta(qibla.gradus, RADIUS - 14);

  return (
    <Oyna
      r={r}
      sarlavha="Qibla yo'nalishi"
      ost={`${qibla.shahar} · ${qibla.gradus}° (${qibla.yonalish})`}
      yop={yop}
      bolalar={
        <>
          <div style={{ display: "flex", justifyContent: "center", marginBottom: 8 }}>
            <svg width={OLCHAM} height={OLCHAM}>
              {/* Telefon qaragan tomonni bildiruvchi qo'zg'almas ko'rsatkich */}
              <polygon
                points={`${M - 7},6 ${M + 7},6 ${M},18`}
                fill={r.matn}
                opacity="0.55"
              />
              <g style={{ transform: `rotate(${rozetkaBurchagi}deg)`, transformOrigin: `${M}px ${M}px`, transition: "transform .25s linear" }}>
                <circle cx={M} cy={M} r={RADIUS} fill="none" stroke={r.xira} strokeWidth="1" opacity="0.35" />
                {Array.from({ length: 72 }, (_, i) => {
                  const uzun = i % 6 === 0;
                  const [x1, y1] = nuqta(i * 5, RADIUS);
                  const [x2, y2] = nuqta(i * 5, RADIUS - (uzun ? 8 : 4));
                  return (
                    <line key={i} x1={x1} y1={y1} x2={x2} y2={y2}
                      stroke={r.xira} strokeWidth={uzun ? 1.2 : 0.6} opacity={uzun ? 0.6 : 0.3} />
                  );
                })}
                {RUMBLAR.map(({ belgi, burchak }) => {
                  const [x, y] = nuqta(burchak, RADIUS - 20);
                  return (
                    <text key={belgi} x={x} y={y} textAnchor="middle" dominantBaseline="middle"
                      style={{ fontFamily: UTIL, fontSize: 9.5, fill: burchak === 0 ? r.matn : r.xira }}>
                      {belgi}
                    </text>
                  );
                })}
                {/* Qibla strelkasi */}
                <line x1={M} y1={M} x2={uchX} y2={uchY} stroke={r.urgu} strokeWidth="2.5" strokeLinecap="round" />
                <text x={uchX} y={uchY} textAnchor="middle" dominantBaseline="middle" style={{ fontSize: 20 }}>
                  🕋
                </text>
              </g>
              <circle cx={M} cy={M} r="3.5" fill={r.urgu} />
            </svg>
          </div>

          <p style={{ textAlign: "center", fontFamily: DISPLAY, fontSize: 30, color: r.urgu, margin: "0 0 4px" }}>
            {qibla.gradus}°
          </p>
          <p style={{ textAlign: "center", fontFamily: UTIL, fontSize: 11.5, color: r.xira, marginBottom: 16 }}>
            shimoldan soat strelkasi bo'yicha
          </p>

          {!kompasFaol && !kompasXato && (
            <button
              onClick={kompasniIshgaTushir}
              style={{
                width: "100%", padding: "12px 16px", borderRadius: 3, marginBottom: 12,
                background: `${r.urgu}18`, border: `1px solid ${r.urgu}66`,
                color: r.matn, fontFamily: UTIL, fontSize: 13.5, cursor: "pointer",
              }}
            >
              🧭 Kompasni yoqish
            </button>
          )}

          <p style={{ fontFamily: UTIL, fontSize: 11.5, lineHeight: 1.65, color: r.xira }}>
            {kompasFaol
              ? "Kompas faol — telefonni tekis ushlang va 🕋 belgisi yuqoridagi ko'rsatkichga to'g'ri kelguncha buriling."
              : kompasXato
                ? "Qurilma kompasi mavjud emas yoki ruxsat berilmadi. Oddiy kompasdan shimolni toping va undan soat strelkasi bo'yicha yuqoridagi gradusga buriling."
                : "Kompassiz ham foydalanish mumkin: shimolni toping va undan soat strelkasi bo'yicha yuqoridagi gradusga buriling."}
          </p>

          <div style={{ marginTop: 14, padding: "12px 14px", borderRadius: 3, background: `${r.urgu}12`, border: `1px solid ${r.urgu}44` }}>
            <p style={{ fontFamily: UTIL, fontSize: 11, lineHeight: 1.65, color: r.xira, margin: 0 }}>
              Bu hisob shahar markazi koordinatalariga asoslangan taxminiy
              yo'nalish. Telefon kompasi ham magnit maydonidan xato berishi
              mumkin — aniq qibla uchun mahalliy masjid yoki mo'tabar
              manbaga murojaat qiling.
            </p>
          </div>
        </>
      }
    />
  );
}
