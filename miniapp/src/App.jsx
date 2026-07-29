import { useEffect, useState } from "react";
import { api } from "./api.js";
import BoshEkran from "./components/BoshEkran.jsx";
import QoidaOyna from "./components/QoidaOyna.jsx";
import SuraOyna from "./components/SuraOyna.jsx";
import SuraRoyxati from "./components/SuraRoyxati.jsx";
import { keyingiNamozniHisobla, rangniAniqla } from "./hisoblash.js";
import { telegramniTayyorla } from "./telegram.js";
import { UTIL } from "./theme.js";

export default function App() {
  const [holat, setHolat] = useState("yuklanmoqda"); // yuklanmoqda | royxatsiz | tayyor | xato
  const [foydalanuvchi, setFoydalanuvchi] = useState(null);
  const [vaqtlar, setVaqtlar] = useState(null);
  const [suralar, setSuralar] = useState([]);
  const [hozir, setHozir] = useState(new Date());
  const [modal, setModal] = useState(null); // null | 'royxat' | 'sura' | 'qoida'
  const [suraTanlangan, setSuraTanlangan] = useState(null);

  useEffect(() => {
    telegramniTayyorla();
    (async () => {
      try {
        const f = await api.foydalanuvchi();
        if (!f.royxatdan_otganmi || !f.shahar_id) {
          setHolat("royxatsiz");
          return;
        }
        setFoydalanuvchi(f);
        const [v, s] = await Promise.all([api.vaqtlar(f.shahar_id), api.suralar()]);
        setVaqtlar(v);
        setSuralar(s);
        setHolat(v.topildi ? "tayyor" : "xato");
      } catch {
        setHolat("xato");
      }
    })();
  }, []);

  useEffect(() => {
    const t = setInterval(() => setHozir(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  async function ochSura(qisqaMalumot) {
    setSuraTanlangan(qisqaMalumot);
    setModal("sura");
    const toliq = await api.sura(qisqaMalumot.raqam);
    setSuraTanlangan(toliq);
  }

  const keyingiNamoz = vaqtlar ? keyingiNamozniHisobla(vaqtlar, hozir) : null;
  const qolganSoniya = keyingiNamoz ? Math.max(0, Math.round((keyingiNamoz.vaqt - hozir) / 1000)) : null;
  const r = rangniAniqla(qolganSoniya);

  return (
    <div
      style={{
        minHeight: "100vh", width: "100%", fontFamily: UTIL,
        background: `radial-gradient(120% 80% at 50% 0%, ${r.yuqori} 0%, ${r.past} 72%)`,
        transition: "background .9s ease",
      }}
    >
      {holat === "yuklanmoqda" && <XabarEkrani r={r} matn="Yuklanmoqda..." />}
      {holat === "xato" && <XabarEkrani r={r} matn="Ma'lumot yuklanmadi. Iltimos, keyinroq qayta urinib ko'ring." />}
      {holat === "royxatsiz" && (
        <XabarEkrani r={r} matn={"Avval Telegram botda /start buyrug'i orqali ro'yxatdan o'ting, so'ng shahringizni tanlang."} />
      )}

      {holat === "tayyor" && vaqtlar && (
        <BoshEkran
          vaqtlar={vaqtlar}
          hozir={hozir}
          daraja={foydalanuvchi?.daraja ?? "boshlangich"}
          suralar={suralar}
          ochRoyxat={() => setModal("royxat")}
          ochQoida={() => setModal("qoida")}
          ochSura={ochSura}
        />
      )}

      {modal === "royxat" && (
        <SuraRoyxati r={r} suralar={suralar} yop={() => setModal(null)} ochish={ochSura} />
      )}
      {modal === "sura" && (
        <SuraOyna r={r} sura={suraTanlangan} yop={() => setModal(null)} orqaga={() => setModal("royxat")} />
      )}
      {modal === "qoida" && <QoidaOyna r={r} yop={() => setModal(null)} />}
    </div>
  );
}

function XabarEkrani({ r, matn }) {
  return (
    <div style={{ display: "flex", minHeight: "100vh", alignItems: "center", justifyContent: "center", padding: 32 }}>
      <p style={{ fontFamily: UTIL, fontSize: 14, lineHeight: 1.7, color: r.matn, textAlign: "center" }}>{matn}</p>
    </div>
  );
}
