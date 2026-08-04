import { useEffect, useState } from "react";
import { api } from "./api.js";
import BildirishnomaOyna from "./components/BildirishnomaOyna.jsx";
import BoshEkran from "./components/BoshEkran.jsx";
import QoidaOyna from "./components/QoidaOyna.jsx";
import ShaharTanlashOyna from "./components/ShaharTanlashOyna.jsx";
import SozlamaOyna from "./components/SozlamaOyna.jsx";
import SuraOyna from "./components/SuraOyna.jsx";
import SuraRoyxati from "./components/SuraRoyxati.jsx";
import { joriyHolatniHisobla, rangniAniqla } from "./hisoblash.js";
import { telegramniTayyorla } from "./telegram.js";
import { UTIL } from "./theme.js";

export default function App() {
  const [holat, setHolat] = useState("yuklanmoqda"); // yuklanmoqda | royxatsiz | tayyor | xato
  const [foydalanuvchi, setFoydalanuvchi] = useState(null);
  const [vaqtlar, setVaqtlar] = useState(null);
  const [suralar, setSuralar] = useState([]);
  const [sozlamalar, setSozlamalar] = useState(null);
  const [viloyatlar, setViloyatlar] = useState([]);
  const [hozir, setHozir] = useState(new Date());
  // null | 'royxat' | 'sura' | 'qoida' | 'sozlama' | 'shahar' | 'bildirishnoma'
  const [modal, setModal] = useState(null);
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
        const [v, s, soz, vil] = await Promise.all([
          api.vaqtlar(f.shahar_id), api.suralar(), api.sozlamalar(), api.viloyatlar(),
        ]);
        setVaqtlar(v);
        setSuralar(s);
        setSozlamalar(soz);
        setViloyatlar(vil);
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

  async function sozlamaniYangila(patch) {
    setSozlamalar((oldi) => ({ ...oldi, ...patch }));
    await api.sozlamalarniYangila(patch);
  }

  async function shaharniTanlash(sh) {
    await sozlamaniYangila({ shahar_id: sh.id });
    const yangiVaqtlar = await api.vaqtlar(sh.id);
    setVaqtlar(yangiVaqtlar);
    setModal("sozlama");
  }

  const svetoforHolati = vaqtlar ? joriyHolatniHisobla(vaqtlar, hozir) : null;
  const qolganSoniya = svetoforHolati?.chegaraVaqt
    ? Math.max(0, Math.round((svetoforHolati.chegaraVaqt - hozir) / 1000))
    : null;
  const r = rangniAniqla(qolganSoniya);

  return (
    <div
      style={{
        position: "relative", minHeight: "100vh", width: "100%", fontFamily: UTIL,
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

      {holat === "tayyor" && (
        <button
          onClick={() => setModal("sozlama")}
          aria-label="Sozlamalar"
          style={{
            position: "fixed", right: 18, bottom: 18, width: 48, height: 48, borderRadius: "50%",
            background: r.yuqori, border: `1px solid ${r.urgu}66`, color: r.urgu, fontSize: 20,
            display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer",
            boxShadow: "0 4px 14px rgba(0,0,0,.35)", zIndex: 40,
          }}
        >
          ⚙️
        </button>
      )}

      {modal === "royxat" && (
        <SuraRoyxati r={r} suralar={suralar} yop={() => setModal(null)} ochish={ochSura} />
      )}
      {modal === "sura" && (
        <SuraOyna r={r} sura={suraTanlangan} yop={() => setModal(null)} orqaga={() => setModal("royxat")} />
      )}
      {modal === "qoida" && <QoidaOyna r={r} yop={() => setModal(null)} />}

      {modal === "sozlama" && sozlamalar && (
        <SozlamaOyna
          r={r}
          shaharNomi={vaqtlar?.shahar ?? "—"}
          sozlamalar={sozlamalar}
          yop={() => setModal(null)}
          ochShahar={() => setModal("shahar")}
          ochBildirishnoma={() => setModal("bildirishnoma")}
        />
      )}
      {modal === "shahar" && (
        <ShaharTanlashOyna
          r={r}
          viloyatlar={viloyatlar}
          yop={() => setModal("sozlama")}
          tanlash={shaharniTanlash}
        />
      )}
      {modal === "bildirishnoma" && sozlamalar && (
        <BildirishnomaOyna
          r={r}
          sozlamalar={sozlamalar}
          yop={() => setModal("sozlama")}
          onYangilash={sozlamaniYangila}
        />
      )}
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
