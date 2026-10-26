import { createContext, useCallback, useContext, useState } from "react";

const Ctx = createContext(null);
export const useToast = () => useContext(Ctx);

export function ToastProvider({ children }) {
  const [items, setItems] = useState([]);
  const toast = useCallback((text, type = "success") => {
    const id = Math.random().toString(36).slice(2);
    setItems((l) => [...l, { id, text, type }]);
    setTimeout(() => setItems((l) => l.filter((x) => x.id !== id)), 3800);
  }, []);
  return (
    <Ctx.Provider value={toast}>
      {children}
      <div className="toasts" aria-live="polite">{items.map((t) => <div key={t.id} className={"toast " + t.type}>{t.text}</div>)}</div>
    </Ctx.Provider>
  );
}
