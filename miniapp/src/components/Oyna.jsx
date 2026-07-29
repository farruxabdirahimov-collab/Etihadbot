import { DISPLAY, UTIL } from "../theme.js";

export default function Oyna({ r, sarlavha, ost, yop, bolalar }) {
  return (
    <div
      onClick={yop}
      style={{
        position: "fixed", inset: 0, zIndex: 50,
        display: "flex", alignItems: "flex-end", justifyContent: "center",
        background: "rgba(0,0,0,.62)", backdropFilter: "blur(3px)",
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: "100%", maxWidth: 480, background: r.yuqori,
          borderTop: `1px solid ${r.urgu}55`, borderRadius: "6px 6px 0 0",
          maxHeight: "86vh", display: "flex", flexDirection: "column",
        }}
      >
        <div
          style={{
            display: "flex", flexShrink: 0, alignItems: "center", justifyContent: "space-between",
            padding: "16px 20px", borderBottom: `1px solid ${r.xira}2E`,
          }}
        >
          <div>
            <p style={{ fontFamily: DISPLAY, fontSize: 19, color: r.matn, margin: 0 }}>{sarlavha}</p>
            {ost && (
              <p style={{ fontFamily: UTIL, fontSize: 11, color: r.xira, marginTop: 2 }}>{ost}</p>
            )}
          </div>
          <button
            onClick={yop}
            style={{
              width: 30, height: 30, borderRadius: 2, border: `1px solid ${r.xira}44`,
              background: "transparent", color: r.matn, fontSize: 16, lineHeight: 1, cursor: "pointer",
            }}
          >
            ×
          </button>
        </div>
        <div style={{ overflowY: "auto", padding: "16px 20px" }}>{bolalar}</div>
      </div>
    </div>
  );
}
