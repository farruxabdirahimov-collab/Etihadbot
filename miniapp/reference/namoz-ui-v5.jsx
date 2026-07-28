import { useState, useEffect, useRef } from "react";

/* ══════════════════════════════════════════════
   NAMOZ — UI PROTOTIP v5
   + Qisqa suralar  + Namoz qoidasi
   ══════════════════════════════════════════════ */

const DISPLAY =
  "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif";
const UTIL = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif";
const ARAB =
  "'SF Arabic', 'Geeza Pro', 'Traditional Arabic', 'Scheherazade New', serif";

const PALETTE = {
  yashil: { yuqori: "#16311B", past: "#0A1A0D", matn: "#F2EDE0", xira: "#93A38C", nozik: "#7E9478", holat: "Vaqt yetarli" },
  sariq:  { yuqori: "#3E2A0C", past: "#241704", matn: "#F7EEDC", xira: "#B69C72", nozik: "#C4A46F", holat: "Tayyorlanish vaqti" },
  qizil:  { yuqori: "#3B1216", past: "#220709", matn: "#F7E9E5", xira: "#B08D85", nozik: "#C08876", holat: "Vaqt kam qoldi" },
  ado:    { yuqori: "#1C3A24", past: "#0D2011", matn: "#EFF3E6", xira: "#9BB093", nozik: "#8CA882", holat: "Ado etildi" },
  kutish: { yuqori: "#1E2E33", past: "#0C1618", matn: "#EDF1F0", xira: "#8FA0A2", nozik: "#7F9294", holat: "Roʻza davom etmoqda" },
  yaqin:  { yuqori: "#33291B", past: "#17110A", matn: "#F6F0E2", xira: "#B0A184", nozik: "#C0AC84", holat: "Iftor yaqin" },
};

const REJIMLAR = {
  oddiy: { nom: null, urgu: "#C9A961", nur: null },
  juma: { nom: "Juma", urgu: "#DFCB90", nur: "rgba(223,203,144,0.09)" },
  ramazon: { nom: "Ramazon", urgu: "#D5CDB4", nur: "rgba(213,205,180,0.07)" },
  royzaHayit: { nom: "Roʻza hayiti", urgu: "#F0C64E", nur: "rgba(240,198,78,0.13)" },
  qurbonHayit: { nom: "Qurbon hayiti", urgu: "#EFB84E", nur: "rgba(239,184,78,0.13)" },
};

const NAMOZLAR = [
  { nom: "Bomdod", arab: "الفجر", rakat: [{ turi: "sunnat", soni: 2, safar: 2 }, { turi: "farz", soni: 2, safar: 2 }], sura: { boshl: "Ixlos", orta: "Kavsar", murak: "Qadr" } },
  { nom: "Peshin", arab: "الظهر", rakat: [{ turi: "sunnat", soni: 4, safar: 0 }, { turi: "farz", soni: 4, safar: 2 }, { turi: "sunnat", soni: 2, safar: 0 }], sura: { boshl: "Falaq", orta: "Nasr", murak: "Fil" } },
  { nom: "Asr", arab: "العصر", rakat: [{ turi: "sunnat", soni: 4, safar: 0 }, { turi: "farz", soni: 4, safar: 2 }], sura: { boshl: "Nas", orta: "Moʻun", murak: "Quraysh" } },
  { nom: "Shom", arab: "المغرب", rakat: [{ turi: "farz", soni: 3, safar: 3 }, { turi: "sunnat", soni: 2, safar: 0 }], sura: { boshl: "Ixlos", orta: "Asr", murak: "Humaza" } },
  { nom: "Xufton", arab: "العشاء", rakat: [{ turi: "sunnat", soni: 4, safar: 0 }, { turi: "farz", soni: 4, safar: 2 }, { turi: "sunnat", soni: 2, safar: 0 }, { turi: "vitr", soni: 3, safar: 3 }], sura: { boshl: "Kavsar", orta: "Takosur", murak: "Qoria" } },
];

/* ── Qisqa suralar ──
   Matn alquran.cloud Usmoniy mushafidan. Bosma mushaf bilan
   solishtirilgandan soʻng tasdiqlangan deb belgilanadi. */
const SURALAR = [
  {
    raqam: 112, nom: "Ixlos", arab: "الإخلاص", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "قُلْ هُوَ ٱللَّهُ أَحَدٌ", tl: "Qul huwallohu ahad" },
      { n: 2, ar: "ٱللَّهُ ٱلصَّمَدُ", tl: "Allohus-samad" },
      { n: 3, ar: "لَمْ يَلِدْ وَلَمْ يُولَدْ", tl: "Lam yalid va lam yulad" },
      { n: 4, ar: "وَلَمْ يَكُن لَّهُۥ كُفُوًا أَحَدٌۢ", tl: "Va lam yakul lahu kufuvan ahad" },
    ],
  },
  {
    raqam: 108, nom: "Kavsar", arab: "الكوثر", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "إِنَّآ أَعْطَيْنَٰكَ ٱلْكَوْثَرَ", tl: "Inna aʼtoynakal-kavsar" },
      { n: 2, ar: "فَصَلِّ لِرَبِّكَ وَٱنْحَرْ", tl: "Fasalli lirobbika vanhar" },
      { n: 3, ar: "إِنَّ شَانِئَكَ هُوَ ٱلْأَبْتَرُ", tl: "Inna shaniaka huval-abtar" },
    ],
  },
  {
    raqam: 103, nom: "Asr", arab: "العصر", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "وَٱلْعَصْرِ", tl: "Val-asr" },
      { n: 2, ar: "إِنَّ ٱلْإِنسَٰنَ لَفِى خُسْرٍ", tl: "Innal-insana lafiy xusr" },
      { n: 3, ar: "إِلَّا ٱلَّذِينَ ءَامَنُوا۟ وَعَمِلُوا۟ ٱلصَّٰلِحَٰتِ وَتَوَاصَوْا۟ بِٱلْحَقِّ وَتَوَاصَوْا۟ بِٱلصَّبْرِ", tl: "Illallaziyna amanu va amilus-solihati va tavasav bil-haqqi va tavasav bis-sabr" },
    ],
  },
  {
    raqam: 110, nom: "Nasr", arab: "النصر", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "إِذَا جَآءَ نَصْرُ ٱللَّهِ وَٱلْفَتْحُ", tl: "Iza jaa nasrullohi val-fath" },
      { n: 2, ar: "وَرَأَيْتَ ٱلنَّاسَ يَدْخُلُونَ فِى دِينِ ٱللَّهِ أَفْوَاجًا", tl: "Va roaytan-nasa yadxuluna fiy diynillahi afvaja" },
      { n: 3, ar: "فَسَبِّحْ بِحَمْدِ رَبِّكَ وَٱسْتَغْفِرْهُ ۚ إِنَّهُۥ كَانَ تَوَّابًۢا", tl: "Fasabbih bihamdi robbika vastagʻfirh, innahu kana tavvaba" },
    ],
  },
  {
    raqam: 113, nom: "Falaq", arab: "الفلق", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "قُلْ أَعُوذُ بِرَبِّ ٱلْفَلَقِ", tl: "Qul aʼuzu birobbil-falaq" },
      { n: 2, ar: "مِن شَرِّ مَا خَلَقَ", tl: "Min sharri ma xolaq" },
      { n: 3, ar: "وَمِن شَرِّ غَاسِقٍ إِذَا وَقَبَ", tl: "Va min sharri gʻosiqin iza vaqob" },
      { n: 4, ar: "وَمِن شَرِّ ٱلنَّفَّٰثَٰتِ فِى ٱلْعُقَدِ", tl: "Va min sharrin-naffasati fil-uqod" },
      { n: 5, ar: "وَمِن شَرِّ حَاسِدٍ إِذَا حَسَدَ", tl: "Va min sharri hasidin iza hasad" },
    ],
  },
  {
    raqam: 114, nom: "Nas", arab: "الناس", daraja: "boshl", tasdiq: true,
    oyatlar: [
      { n: 1, ar: "قُلْ أَعُوذُ بِرَبِّ ٱلنَّاسِ", tl: "Qul aʼuzu birobbin-nas" },
      { n: 2, ar: "مَلِكِ ٱلنَّاسِ", tl: "Malikin-nas" },
      { n: 3, ar: "إِلَٰهِ ٱلنَّاسِ", tl: "Ilahin-nas" },
      { n: 4, ar: "مِن شَرِّ ٱلْوَسْوَاسِ ٱلْخَنَّاسِ", tl: "Min sharril-vasvasil-xonnas" },
      { n: 5, ar: "ٱلَّذِى يُوَسْوِسُ فِى صُدُورِ ٱلنَّاسِ", tl: "Allaziy yuvasvisu fiy suduurin-nas" },
      { n: 6, ar: "مِنَ ٱلْجِنَّةِ وَٱلنَّاسِ", tl: "Minal-jinnati van-nas" },
    ],
  },
  /* Bazadan keladigan qolgan suralar */
  { raqam: 106, nom: "Quraysh", arab: "قريش", daraja: "boshl", oyatSoni: 4 },
  { raqam: 111, nom: "Masad", arab: "المسد", daraja: "boshl", oyatSoni: 5 },
  { raqam: 105, nom: "Fil", arab: "الفيل", daraja: "orta", oyatSoni: 5 },
  { raqam: 109, nom: "Kofirun", arab: "الكافرون", daraja: "orta", oyatSoni: 6 },
  { raqam: 107, nom: "Moʻun", arab: "الماعون", daraja: "orta", oyatSoni: 7 },
  { raqam: 97, nom: "Qadr", arab: "القدر", daraja: "orta", oyatSoni: 5 },
  { raqam: 102, nom: "Takosur", arab: "التكاثر", daraja: "orta", oyatSoni: 8 },
  { raqam: 104, nom: "Humaza", arab: "الهمزة", daraja: "orta", oyatSoni: 9 },
  { raqam: 99, nom: "Zalzala", arab: "الزلزلة", daraja: "orta", oyatSoni: 8 },
  { raqam: 101, nom: "Qoriʼa", arab: "القارعة", daraja: "murak", oyatSoni: 11 },
  { raqam: 100, nom: "Odiyot", arab: "العاديات", daraja: "murak", oyatSoni: 11 },
  { raqam: 95, nom: "Tiyn", arab: "التين", daraja: "murak", oyatSoni: 8 },
  { raqam: 94, nom: "Sharh", arab: "الشرح", daraja: "murak", oyatSoni: 8 },
  { raqam: 93, nom: "Zuho", arab: "الضحى", daraja: "murak", oyatSoni: 11 },
];

/* ── Namoz qoidasi: qisqa, keyin kengaytiriladi ── */
const QOIDA = [
  { n: 1, nom: "Niyat", izoh: "Qaysi namozni oʻqiyotganingizni koʻngildan oʻtkazasiz." },
  { n: 2, nom: "Takbiratul ihrom", izoh: "Qoʻlni quloq barobariga koʻtarib «Allohu akbar» deysiz. Shundan soʻng namoz boshlandi — gapirmaysiz, oʻgirilmaysiz." },
  { n: 3, nom: "Qiyom", izoh: "Tik turib Fotiha surasini, soʻng zam surani oʻqiysiz." },
  { n: 4, nom: "Rukuʼ", izoh: "Belni egib «Subhana Robbiyal Aziym» — uch marta." },
  { n: 5, nom: "Qavma", izoh: "Tik turasiz: «Samiʼallohu liman hamidah — Robbana lakal hamd»." },
  { n: 6, nom: "Sajda", izoh: "Peshona yerga tegadi: «Subhana Robbiyal Aʼla» — uch marta." },
  { n: 7, nom: "Jalsa", izoh: "Bir lahza oʻtirasiz, soʻng ikkinchi sajdani qilasiz." },
  { n: 8, nom: "Ikkinchi rakat", izoh: "Turib 3–7-qadamlarni takrorlaysiz." },
  { n: 9, nom: "Qaʼda", izoh: "Oʻtirib Attahiyot, salovot va duoni oʻqiysiz." },
  { n: 10, nom: "Salom", izoh: "Oʻngga, soʻng chapga qarab «Assalomu alaykum va rohmatulloh»." },
];

const DARAJA_NOM = { boshl: "Boshlangʻich", orta: "Oʻrta", murak: "Murakkab" };
const ikki = (n) => String(n).padStart(2, "0");

function asosRang({ soniya, ado, ramazon, faza }) {
  if (ado) return PALETTE.ado;
  const d = soniya / 60;
  if (ramazon && faza === "kunduz") return d > 20 ? PALETTE.kutish : PALETTE.yaqin;
  if (d > 20) return PALETTE.yashil;
  if (d > 10) return PALETTE.sariq;
  return PALETTE.qizil;
}

/* ─────────── Modal qobiq ─────────── */
function Oyna({ r, sarlavha, ost, yop, bolalar }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center sm:items-center"
      style={{ background: "rgba(0,0,0,.62)", backdropFilter: "blur(3px)" }}
      onClick={yop}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="w-full max-w-md"
        style={{
          background: r.yuqori,
          borderTop: `1px solid ${r.urgu}55`,
          borderRadius: "6px 6px 0 0",
          maxHeight: "86vh",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div
          className="flex shrink-0 items-center justify-between px-5 py-4"
          style={{ borderBottom: `1px solid ${r.xira}2E` }}
        >
          <div>
            <p style={{ fontFamily: DISPLAY, fontSize: 19, color: r.matn }}>
              {sarlavha}
            </p>
            {ost && (
              <p style={{ fontFamily: UTIL, fontSize: 11, color: r.xira, marginTop: 2 }}>
                {ost}
              </p>
            )}
          </div>
          <button
            onClick={yop}
            style={{
              width: 30, height: 30, borderRadius: 2,
              border: `1px solid ${r.xira}44`, background: "transparent",
              color: r.matn, fontSize: 16, lineHeight: 1, cursor: "pointer",
            }}
          >
            ×
          </button>
        </div>
        <div className="overflow-y-auto px-5 py-4">{bolalar}</div>
      </div>
    </div>
  );
}

/* ─────────── Sura oʻquvchi ─────────── */
function SuraOyna({ r, sura, yop, orqaga }) {
  const [talaffuz, setTalaffuz] = useState(true);
  const bor = Array.isArray(sura.oyatlar);

  return (
    <Oyna
      r={r}
      sarlavha={`${sura.nom} surasi`}
      ost={`${sura.raqam}-sura · ${bor ? sura.oyatlar.length : sura.oyatSoni} oyat`}
      yop={yop}
      bolalar={
        <>
          <div className="mb-4 flex items-center justify-between">
            <button
              onClick={orqaga}
              style={{
                fontFamily: UTIL, fontSize: 11.5, color: r.xira,
                background: "none", border: "none", cursor: "pointer", padding: 0,
              }}
            >
              ← Roʻyxat
            </button>
            <button
              onClick={() => setTalaffuz(!talaffuz)}
              style={{
                fontFamily: UTIL, fontSize: 10.5, color: talaffuz ? r.urgu : r.xira,
                border: `1px solid ${talaffuz ? r.urgu + "77" : r.xira + "44"}`,
                background: talaffuz ? `${r.urgu}14` : "transparent",
                borderRadius: 2, padding: "5px 10px", cursor: "pointer",
              }}
            >
              Talaffuz
            </button>
          </div>

          {bor ? (
            <>
              {sura.raqam !== 9 && (
                <p
                  className="mb-5 text-center"
                  style={{ fontFamily: ARAB, fontSize: 19, color: r.xira, direction: "rtl" }}
                >
                  بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ
                </p>
              )}
              {sura.oyatlar.map((o) => (
                <div
                  key={o.n}
                  className="mb-4 pb-4"
                  style={{ borderBottom: `1px solid ${r.xira}1F` }}
                >
                  <div className="mb-2 flex items-start gap-3" style={{ direction: "rtl" }}>
                    <span
                      className="shrink-0 tabular-nums"
                      style={{
                        fontFamily: UTIL, fontSize: 10, color: r.urgu,
                        border: `1px solid ${r.urgu}55`, borderRadius: 99,
                        width: 20, height: 20, display: "flex",
                        alignItems: "center", justifyContent: "center", marginTop: 6,
                      }}
                    >
                      {o.n}
                    </span>
                    <p style={{ fontFamily: ARAB, fontSize: 23, lineHeight: 2, color: r.matn }}>
                      {o.ar}
                    </p>
                  </div>
                  {talaffuz && (
                    <p style={{ fontFamily: UTIL, fontSize: 12.5, lineHeight: 1.7, color: r.xira, paddingRight: 32 }}>
                      {o.tl}
                    </p>
                  )}
                </div>
              ))}
              <p style={{ fontFamily: UTIL, fontSize: 10.5, lineHeight: 1.6, color: r.xira, opacity: 0.75 }}>
                Matn manbasi: Usmoniy mushaf. Talaffuz yozuvi faqat yordam
                uchun — asl oʻqilishni ustozdan oʻrganing.
              </p>
            </>
          ) : (
            <div className="py-10 text-center">
              <p style={{ fontFamily: UTIL, fontSize: 13, color: r.xira, lineHeight: 1.7 }}>
                Bu suraning matni bazadan yuklanadi.
                <br />
                Ilova birinchi ishga tushganda barcha 20 sura
                <br />
                qurilmaga saqlanadi va internetsiz ishlaydi.
              </p>
            </div>
          )}
        </>
      }
    />
  );
}

/* ─────────── Sura roʻyxati ─────────── */
function SuraRoyxati({ r, ochish, yop }) {
  const guruh = (d) => SURALAR.filter((s) => s.daraja === d);
  return (
    <Oyna
      r={r}
      sarlavha="Qisqa suralar"
      ost="20 ta sura · internetsiz ishlaydi"
      yop={yop}
      bolalar={
        <>
          {["boshl", "orta", "murak"].map((d) => (
            <div key={d} className="mb-5">
              <p
                className="mb-2.5 uppercase"
                style={{ fontFamily: UTIL, fontSize: 9, letterSpacing: ".18em", color: r.xira }}
              >
                {DARAJA_NOM[d]}
              </p>
              <div className="flex flex-col gap-1.5">
                {guruh(d).map((s) => (
                  <button
                    key={s.raqam}
                    onClick={() => ochish(s)}
                    className="flex items-center justify-between px-4 py-3"
                    style={{
                      borderRadius: 3, background: `${r.matn}0A`,
                      border: `1px solid ${r.xira}2E`, cursor: "pointer",
                      textAlign: "left",
                    }}
                  >
                    <div className="flex items-baseline gap-3">
                      <span
                        className="tabular-nums shrink-0"
                        style={{ fontFamily: UTIL, fontSize: 10.5, color: r.xira, minWidth: 22 }}
                      >
                        {s.raqam}
                      </span>
                      <div>
                        <p style={{ fontFamily: DISPLAY, fontSize: 16, color: r.matn }}>
                          {s.nom}
                        </p>
                        <p style={{ fontFamily: UTIL, fontSize: 10.5, color: r.xira }}>
                          {(s.oyatlar ? s.oyatlar.length : s.oyatSoni)} oyat
                        </p>
                      </div>
                    </div>
                    <span style={{ fontFamily: ARAB, fontSize: 17, color: r.urgu }}>
                      {s.arab}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </>
      }
    />
  );
}

/* ─────────── Namoz qoidasi ─────────── */
function QoidaOyna({ r, yop }) {
  return (
    <Oyna
      r={r}
      sarlavha="Namoz qanday oʻqiladi"
      ost="Ikki rakatli namoz misolida"
      yop={yop}
      bolalar={
        <>
          {QOIDA.map((q) => (
            <div key={q.n} className="mb-3.5 flex gap-3">
              <span
                className="shrink-0 tabular-nums"
                style={{
                  fontFamily: UTIL, fontSize: 10, color: r.urgu,
                  border: `1px solid ${r.urgu}55`, borderRadius: 2,
                  width: 22, height: 22, display: "flex",
                  alignItems: "center", justifyContent: "center", marginTop: 2,
                }}
              >
                {q.n}
              </span>
              <div>
                <p style={{ fontFamily: DISPLAY, fontSize: 15.5, color: r.matn, marginBottom: 2 }}>
                  {q.nom}
                </p>
                <p style={{ fontFamily: UTIL, fontSize: 12, lineHeight: 1.65, color: r.xira }}>
                  {q.izoh}
                </p>
              </div>
            </div>
          ))}
          <div
            className="mt-4 px-4 py-3.5"
            style={{ borderRadius: 3, background: `${r.urgu}12`, border: `1px solid ${r.urgu}44` }}
          >
            <p style={{ fontFamily: UTIL, fontSize: 11.5, lineHeight: 1.65, color: r.xira }}>
              Bu qisqacha tartib. Toʻrt rakatli namozlarda 3–7-qadamlar toʻrt
              marta takrorlanadi. Batafsil oʻrgatish, ovozli hamrohlik va
              tahorat qoidasi keyingi versiyada qoʻshiladi.
            </p>
          </div>
        </>
      }
    />
  );
}

/* ═══════════ ASOSIY ═══════════ */
export default function NamozUI() {
  const [hozir, setHozir] = useState(new Date());
  const [qolgan, setQolgan] = useState(17 * 60 + 31);
  const [oyna] = useState(40 * 60);
  const [namozIdx, setNamozIdx] = useState(0);
  const [rejim, setRejim] = useState("oddiy");
  const [faza, setFaza] = useState("kunduz");
  const [ramazonKun, setRamazonKun] = useState(14);
  const [holat, setHolat] = useState("hisob");
  const [daraja, setDaraja] = useState("boshl");
  const [adoEtilgan, setAdoEtilgan] = useState([]);
  const [modal, setModal] = useState(null); // null | 'royxat' | 'qoida'
  const [suraTanlangan, setSuraTanlangan] = useState(null);
  const [demoOchiq, setDemoOchiq] = useState(true);
  const tick = useRef();

  useEffect(() => {
    tick.current = setInterval(() => {
      setHozir(new Date());
      setQolgan((q) => (q > 0 ? q - 1 : 0));
    }, 1000);
    return () => clearInterval(tick.current);
  }, []);

  useEffect(() => {
    if (qolgan <= 0 && holat === "hisob") setHolat("soroq");
    if (qolgan > 0 && (holat === "soroq" || holat === "kutmoqda")) setHolat("hisob");
  }, [qolgan]);

  const rj = REJIMLAR[rejim];
  const ramazon = rejim === "ramazon";
  const oxirgiOn = ramazon && ramazonKun >= 21;
  const ado = holat === "ado";
  const asos = asosRang({ soniya: qolgan, ado, ramazon, faza });
  const r = { ...asos, urgu: oxirgiOn ? "#E8DCA8" : rj.urgu };

  const namoz = NAMOZLAR[namozIdx];
  const vaqtKirdi = qolgan <= 0;
  const daq = Math.floor(qolgan / 60);
  const son = qolgan % 60;

  const tavsiyaSura = SURALAR.find((s) => s.nom === namoz.sura[daraja]);
  const R = 108;
  const C = 2 * Math.PI * R;
  const ulush = Math.max(0, Math.min(1, qolgan / oyna));

  const tasmaNom = ramazon
    ? `Ramazon · ${ramazonKun}-kun${oxirgiOn ? " · oxirgi oʻn kecha" : ""}`
    : rj.nom;

  return (
    <div
      className="min-h-screen w-full"
      style={{
        background: rj.nur
          ? `radial-gradient(110% 55% at 50% 0%, ${rj.nur} 0%, transparent 60%), radial-gradient(120% 80% at 50% 0%, ${asos.yuqori} 0%, ${asos.past} 72%)`
          : `radial-gradient(120% 80% at 50% 0%, ${asos.yuqori} 0%, ${asos.past} 72%)`,
        transition: "background .9s ease",
        fontFamily: UTIL,
      }}
    >
      {tasmaNom && (
        <div
          className="flex items-center justify-center gap-2.5 py-2"
          style={{ background: `${r.urgu}16`, borderBottom: `1px solid ${r.urgu}3D` }}
        >
          <span style={{ width: 4, height: 4, borderRadius: 99, background: r.urgu, display: "inline-block" }} />
          <span className="uppercase" style={{ fontSize: 9.5, letterSpacing: ".24em", color: r.urgu, fontWeight: 600 }}>
            {tasmaNom}
          </span>
          <span style={{ width: 4, height: 4, borderRadius: 99, background: r.urgu, display: "inline-block" }} />
        </div>
      )}

      <div className="mx-auto max-w-md px-5 pb-10 pt-5">
        <div className="mb-1 flex items-center justify-between">
          <p style={{ fontFamily: DISPLAY, fontSize: 16, color: r.matn }}>Urganch</p>
          <p className="tabular-nums" style={{ fontFamily: DISPLAY, fontSize: 22, color: r.matn }}>
            {ikki(hozir.getHours())}
            <span style={{ color: r.xira }}>:</span>
            {ikki(hozir.getMinutes())}
            <span style={{ color: r.xira, fontSize: 15 }}>:{ikki(hozir.getSeconds())}</span>
          </p>
        </div>
        <div className="mb-6 flex items-center justify-between pb-3" style={{ borderBottom: `1px solid ${r.xira}22` }}>
          <p style={{ fontSize: 11, color: r.xira }}>12 Safar 1448</p>
          <p style={{ fontSize: 11, color: r.xira }}>28 iyul, seshanba</p>
        </div>

        {/* Halqa */}
        <div className="mb-5 flex justify-center">
          <div className="relative flex items-center justify-center">
            <svg width="248" height="248" style={{ transform: "rotate(-90deg)" }}>
              <circle cx="124" cy="124" r={R} fill="none" stroke={r.xira} strokeWidth="1" opacity="0.22" />
              <circle
                cx="124" cy="124" r={R} fill="none" stroke={r.urgu}
                strokeWidth="2.5" strokeLinecap="round"
                strokeDasharray={C} strokeDashoffset={C * (1 - ulush)}
                style={{ transition: "stroke-dashoffset .9s linear, stroke .7s" }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <p style={{ fontFamily: ARAB, fontSize: 19, color: r.xira, marginBottom: 2 }}>
                {namoz.arab}
              </p>
              <p style={{ fontFamily: DISPLAY, fontSize: 25, color: r.matn, marginBottom: 8 }}>
                {namoz.nom}
              </p>
              {!vaqtKirdi ? (
                <>
                  <p className="tabular-nums" style={{ fontFamily: DISPLAY, fontSize: 50, color: r.urgu, lineHeight: 1 }}>
                    {ikki(daq)}<span style={{ opacity: 0.55 }}>:</span>{ikki(son)}
                  </p>
                  <p className="uppercase" style={{ fontSize: 8.5, letterSpacing: ".2em", color: r.xira, marginTop: 8 }}>
                    qoldi
                  </p>
                </>
              ) : (
                <p style={{ fontFamily: DISPLAY, fontSize: 24, color: r.urgu }}>
                  {ado ? "Ado etildi" : "Vaqt kirdi"}
                </p>
              )}
            </div>
          </div>
        </div>

        <p className="mb-5 text-center uppercase" style={{ fontSize: 9.5, letterSpacing: ".22em", color: r.nozik }}>
          {asos.holat}
        </p>

        {/* Rakat + kichik qoida tugmasi */}
        <div className="mb-1.5 flex flex-wrap items-center justify-center gap-1.5">
          {namoz.rakat.map((x, i) => {
            const asosiy = x.turi === "farz" || x.turi === "vitr";
            return (
              <div
                key={i}
                className="flex items-baseline gap-1.5 px-3 py-2"
                style={{
                  borderRadius: 2,
                  border: `1px solid ${asosiy ? r.urgu + "88" : r.xira + "44"}`,
                  background: asosiy ? `${r.urgu}14` : "transparent",
                }}
              >
                <span className="tabular-nums" style={{ fontFamily: DISPLAY, fontSize: 18, color: r.matn, lineHeight: 1 }}>
                  {x.soni}
                </span>
                <span className="uppercase" style={{ fontSize: 9, letterSpacing: ".16em", color: asosiy ? r.urgu : r.xira, fontWeight: asosiy ? 700 : 500 }}>
                  {x.turi}
                </span>
              </div>
            );
          })}
        </div>

        {/* ← kichik tugma */}
        <div className="mb-5 flex justify-center">
          <button
            onClick={() => setModal("qoida")}
            style={{
              fontFamily: UTIL, fontSize: 10.5, color: r.xira,
              background: "none", border: "none", cursor: "pointer",
              borderBottom: `1px dotted ${r.xira}88`,
              padding: "2px 0", letterSpacing: ".02em",
            }}
          >
            qanday oʻqiladi?
          </button>
        </div>

        {/* Zam sura — bosiladi */}
        <button
          onClick={() => {
            if (tavsiyaSura) {
              setSuraTanlangan(tavsiyaSura);
              setModal("sura");
            }
          }}
          className="mb-2.5 flex w-full items-center justify-between px-4 py-3.5"
          style={{
            borderRadius: 3, background: `${r.matn}0A`,
            border: `1px solid ${r.xira}2E`, cursor: "pointer", textAlign: "left",
          }}
        >
          <div>
            <p className="uppercase" style={{ fontSize: 9, letterSpacing: ".18em", color: r.xira, marginBottom: 5 }}>
              Tavsiya etilgan zam sura
            </p>
            <p style={{ fontFamily: DISPLAY, fontSize: 20, color: r.matn }}>
              {namoz.sura[daraja]}
            </p>
          </div>
          <div className="flex items-center gap-2.5">
            <span style={{ fontSize: 10, color: r.urgu, border: `1px solid ${r.urgu}55`, borderRadius: 2, padding: "4px 9px" }}>
              {DARAJA_NOM[daraja]}
            </span>
            <span style={{ fontSize: 14, color: r.xira }}>›</span>
          </div>
        </button>

        {holat === "soroq" && (
          <div className="mb-2.5 px-4 py-4" style={{ borderRadius: 3, background: `${r.urgu}14`, border: `1px solid ${r.urgu}55` }}>
            <p style={{ fontFamily: DISPLAY, fontSize: 17, color: r.matn, marginBottom: 13 }}>
              {namoz.nom} namozini oʻqidingizmi?
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => { setHolat("ado"); setAdoEtilgan((p) => [...new Set([...p, namozIdx])]); }}
                className="flex-1 py-2.5"
                style={{ borderRadius: 2, background: r.urgu, color: asos.past, fontSize: 13.5, fontWeight: 700, border: "none", cursor: "pointer" }}
              >
                Ha
              </button>
              <button
                onClick={() => setHolat("kutmoqda")}
                className="flex-1 py-2.5"
                style={{ borderRadius: 2, background: "transparent", color: r.matn, fontSize: 13.5, border: `1px solid ${r.xira}66`, cursor: "pointer" }}
              >
                Endi oʻqiyman
              </button>
            </div>
          </div>
        )}

        {/* Pastki kartalar */}
        <div className="grid grid-cols-2 gap-2.5">
          <button
            onClick={() => setModal("royxat")}
            className="px-4 py-3.5"
            style={{ borderRadius: 3, background: `${r.urgu}12`, border: `1px solid ${r.urgu}4D`, cursor: "pointer", textAlign: "left" }}
          >
            <p style={{ fontFamily: DISPLAY, fontSize: 15, color: r.matn, marginBottom: 3 }}>
              Qisqa suralar
            </p>
            <p style={{ fontSize: 11, color: r.xira }}>20 ta · oflayn</p>
          </button>

          {[
            { nom: "Qurʼon", izoh: "18-juz · 62%", p: 0.62 },
            { nom: "Qazo namozlar", izoh: "6 ta qoldirilgan", p: null },
            { nom: "Qibla", izoh: "241° janubi-gʻarb", p: null },
          ].map((f) => (
            <div key={f.nom} className="px-4 py-3.5" style={{ borderRadius: 3, background: `${r.matn}0A`, border: `1px solid ${r.xira}2E` }}>
              <p style={{ fontFamily: DISPLAY, fontSize: 15, color: r.matn, marginBottom: 3 }}>
                {f.nom}
              </p>
              <p style={{ fontSize: 11, color: r.xira, marginBottom: f.p !== null ? 9 : 0 }}>
                {f.izoh}
              </p>
              {f.p !== null && (
                <div style={{ height: 2.5, background: `${r.xira}33`, borderRadius: 99, overflow: "hidden" }}>
                  <div style={{ width: `${f.p * 100}%`, height: "100%", background: r.urgu }} />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Manba — shart boʻyicha doim koʻrinadi */}
        <p
          className="mt-5 text-center"
          style={{ fontSize: 9.5, lineHeight: 1.6, color: r.xira, opacity: 0.7 }}
        >
          Namoz vaqtlari manbasi: namozvaqti.uz
          <br />
          «Book Media Nashr» taqvim kitobi asosida
        </p>
      </div>

      {/* ══ DEMO ══ */}
      <div className="mx-auto max-w-md px-5 pb-12" style={{ borderTop: `1px solid ${r.xira}1F`, paddingTop: 16 }}>
        <button
          onClick={() => setDemoOchiq(!demoOchiq)}
          className="mb-3 flex w-full items-center justify-between"
          style={{ background: "none", border: "none", cursor: "pointer" }}
        >
          <span className="uppercase" style={{ fontSize: 9, letterSpacing: ".2em", color: r.xira }}>
            Demo boshqaruv
          </span>
          <span style={{ fontSize: 10, color: r.xira, transform: demoOchiq ? "rotate(180deg)" : "none", transition: "transform .3s" }}>
            ▾
          </span>
        </button>

        {demoOchiq && (
          <>
            <div className="mb-4">
              <div className="mb-1.5 flex justify-between">
                <span style={{ fontSize: 11, color: r.xira }}>Qolgan vaqt</span>
                <span className="tabular-nums" style={{ fontSize: 11, color: r.matn }}>
                  {ikki(daq)}:{ikki(son)}
                </span>
              </div>
              <input
                type="range" min="0" max="2400" step="15" value={qolgan}
                onChange={(e) => setQolgan(Number(e.target.value))}
                className="w-full" style={{ accentColor: r.urgu }}
              />
            </div>

            <div className="mb-2.5 grid grid-cols-5 gap-1.5">
              {NAMOZLAR.map((n, i) => (
                <button
                  key={n.nom}
                  onClick={() => { setNamozIdx(i); setHolat(qolgan <= 0 ? "soroq" : "hisob"); }}
                  className="py-2"
                  style={{
                    borderRadius: 2, fontSize: 10.5,
                    border: `1px solid ${namozIdx === i ? r.urgu : r.xira + "3D"}`,
                    background: namozIdx === i ? `${r.urgu}1F` : "transparent",
                    color: namozIdx === i ? r.matn : r.xira, cursor: "pointer",
                  }}
                >
                  {n.nom}
                </button>
              ))}
            </div>

            <div className="grid grid-cols-3 gap-1.5">
              {Object.keys(DARAJA_NOM).map((d) => (
                <button
                  key={d}
                  onClick={() => setDaraja(d)}
                  className="py-2"
                  style={{
                    borderRadius: 2, fontSize: 10.5,
                    border: `1px solid ${daraja === d ? r.urgu : r.xira + "3D"}`,
                    background: daraja === d ? `${r.urgu}1F` : "transparent",
                    color: daraja === d ? r.matn : r.xira, cursor: "pointer",
                  }}
                >
                  {DARAJA_NOM[d]}
                </button>
              ))}
            </div>
          </>
        )}
      </div>

      {/* ══ Modallar ══ */}
      {modal === "royxat" && (
        <SuraRoyxati
          r={r}
          yop={() => setModal(null)}
          ochish={(s) => { setSuraTanlangan(s); setModal("sura"); }}
        />
      )}
      {modal === "sura" && suraTanlangan && (
        <SuraOyna
          r={r}
          sura={suraTanlangan}
          yop={() => setModal(null)}
          orqaga={() => setModal("royxat")}
        />
      )}
      {modal === "qoida" && <QoidaOyna r={r} yop={() => setModal(null)} />}
    </div>
  );
}
