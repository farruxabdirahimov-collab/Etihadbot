import { useEffect, useState } from "react";
import { api } from "./api.js";
import BildirishnomaOyna from "./components/BildirishnomaOyna.jsx";
import BoshEkran from "./components/BoshEkran.jsx";
import FikrOyna from "./components/FikrOyna.jsx";
import IlkTanlov from "./components/IlkTanlov.jsx";
import QiblaOyna from "./components/QiblaOyna.jsx";
import QoidaOyna from "./components/QoidaOyna.jsx";
import ShaharTanlashOyna from "./components/ShaharTanlashOyna.jsx";
import SozlamaOyna from "./components/SozlamaOyna.jsx";
import SuraOyna from "./components/SuraOyna.jsx";
import SuraRoyxati from "./components/SuraRoyxati.jsx";
import { joriyHolatniHisobla, rangniAniqla } from "./hisoblash.js";
import * as saqlash from "./saqlash.js";
import { telegramdami, telegramniTayyorla, ulashishniOch } from "./telegram.js";
import { PALETTE, UTIL } from "./theme.js";

const TAVSIYA_MATNI =
  "Namoz vaqtlari va namozni o'rganish uchun «Etihat — E'tiqod» ilovasini tavsiya qilaman.";

// Mehmon rejimida bildirishnoma yo'q — u faqat Telegram orqali beriladi.
const MEHMON_SOZLAMALARI = {
  eslatma_yoqilgan: false,
  eslatma_namozlar: [],
  eslatma_daqiqa: 10,
  eslatma_tugash_yoqilgan: false,
  eslatma_tugash_daqiqa: 15,
};

export default function App() {
  const [holat, setHolat] = useState("yuklanmoqda"); // yuklanmoqda | ilk_tanlov | tayyor | xato
  const [mehmon, setMehmon] = useState(false);
  const [shaharId, setShaharId] = useState(null);
  const [daraja, setDaraja] = useState("boshlangich");
  const [vaqtlar, setVaqtlar] = useState(null);
  const [suralar, setSuralar] = useState([]);
  const [sozlamalar, setSozlamalar] = useState(null);
  const [viloyatlar, setViloyatlar] = useState([]);
  const [qibla, setQibla] = useState(null);
  const [botUsername, setBotUsername] = useState("");
  const [hozir, setHozir] = useState(new Date());
  const [modal, setModal] = useState(null);
  const [suraTanlangan, setSuraTanlangan] = useState(null);

  useEffect(() => {
    telegramniTayyorla();
    (async () => {
      const tgda = telegramdami();
      setMehmon(!tgda);
      try {
        let boshlangichShahar = null;
        if (tgda) {
          const f = await api.foydalanuvchi();
          boshlangichShahar = f.shahar_id ?? null;
          setDaraja(f.daraja ?? "boshlangich");
          setSozlamalar(f.royxatdan_otganmi ? await api.sozlamalar() : null);
        } else {
          const mahalliy = saqlash.ol();
          boshlangichShahar = mahalliy.shahar_id;
          setDaraja(mahalliy.daraja);
          setSozlamalar({ ...MEHMON_SOZLAMALARI });
        }

        const [vil, ilova] = await Promise.all([api.viloyatlar(), api.ilova()]);
        setViloyatlar(vil);
        setBotUsername(ilova.bot_username);

        if (!boshlangichShahar) {
          setHolat("ilk_tanlov");
          return;
        }
        await shaharMalumotlariniYukla(boshlangichShahar);
      } catch {
        setHolat("xato");
      }
    })();
  }, []);

  useEffect(() => {
    const t = setInterval(() => setHozir(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  async function shaharMalumotlariniYukla(id) {
    const [v, s, q] = await Promise.all([api.vaqtlar(id), api.suralar(), api.qibla(id)]);
    setShaharId(id);
    setVaqtlar(v);
    setSuralar(s);
    setQibla(q);
    setHolat(v.topildi ? "tayyor" : "xato");
  }

  async function ochSura(qisqaMalumot) {
    setSuraTanlangan(qisqaMalumot);
    setModal("sura");
    const toliq = await api.sura(qisqaMalumot.raqam);
    setSuraTanlangan(toliq);
  }

  async function sozlamaniYangila(patch) {
    setSozlamalar((oldi) => ({ ...oldi, ...patch }));
    if (!mehmon) await api.sozlamalarniYangila(patch);
  }

  async function shaharniTanlash(sh) {
    if (mehmon) {
      saqlash.yoz({ shahar_id: sh.id });
    } else {
      await api.sozlamalarniYangila({ shahar_id: sh.id });
      setSozlamalar((oldi) => ({ ...(oldi ?? MEHMON_SOZLAMALARI), shahar_id: sh.id }));
    }
    await shaharMalumotlariniYukla(sh.id);
    setModal(holat === "ilk_tanlov" ? null : "sozlama");
  }

  function ulash() {
    const havola = botUsername ? `https://t.me/${botUsername}` : window.location.origin;
    ulashishniOch(havola, TAVSIYA_MATNI);
  }

  function botniOch() {
    if (!botUsername) return;
    window.open(`https://t.me/${botUsername}`, "_blank");
  }

  const svetoforHolati = vaqtlar ? joriyHolatniHisobla(vaqtlar, hozir) : null;
  const qolganSoniya = svetoforHolati?.chegaraVaqt
    ? Math.max(0, Math.round((svetoforHolati.chegaraVaqt - hozir) / 1000))
    : null;
  // Vaqtlar hali yuklanmagan ekranlarda (yuklanish, ilk tanlov) svetofor
  // rangi ma'nosiz — tinch yashil fon ishlatiladi.
  const r = vaqtlar ? rangniAniqla(qolganSoniya) : PALETTE.yashil;

  return (
    <div
      style={{
        position: "relative", minHeight: "100vh", width: "100%", fontFamily: UTIL,
        background: `radial-gradient(120% 80% at 50% 0%, ${r.yuqori} 0%, ${r.past} 72%)`,
        transition: "background .9s ease",
      }}
    >
      {holat === "yuklanmoqda" && <XabarEkrani r={r} matn="Yuklanmoqda..." />}
      {holat === "xato" && (
        <XabarEkrani r={r} matn="Ma'lumot yuklanmadi. Internetni tekshirib, sahifani yangilang." />
      )}
      {holat === "ilk_tanlov" && (
        <IlkTanlov r={r} viloyatlar={viloyatlar} tanlash={shaharniTanlash} />
      )}

      {holat === "tayyor" && vaqtlar && (
        <BoshEkran
          vaqtlar={vaqtlar}
          hozir={hozir}
          daraja={daraja}
          suralar={suralar}
          qibla={qibla}
          ochRoyxat={() => setModal("royxat")}
          ochQoida={() => setModal("qoida")}
          ochSura={ochSura}
          ochQibla={() => setModal("qibla")}
          ulash={ulash}
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
      {modal === "qibla" && qibla?.topildi && (
        <QiblaOyna r={r} qibla={qibla} yop={() => setModal(null)} />
      )}

      {modal === "sozlama" && (
        <SozlamaOyna
          r={r}
          shaharNomi={vaqtlar?.shahar ?? "—"}
          sozlamalar={sozlamalar}
          mehmon={mehmon}
          yop={() => setModal(null)}
          ochShahar={() => setModal("shahar")}
          ochBildirishnoma={() => setModal("bildirishnoma")}
          ochFikr={() => setModal("fikr")}
          botniOch={botniOch}
        />
      )}
      {modal === "fikr" && <FikrOyna r={r} yop={() => setModal("sozlama")} />}
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
