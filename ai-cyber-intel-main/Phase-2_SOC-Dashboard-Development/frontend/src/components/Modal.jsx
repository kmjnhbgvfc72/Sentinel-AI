import { X } from "lucide-react";
import { useEffect, useRef } from "react";

export default function Modal({ title, children, onClose }) {
  const closeRef = useRef(null);
  useEffect(() => { closeRef.current?.focus(); const handler = (event) => event.key === "Escape" && onClose(); document.addEventListener("keydown", handler); return () => document.removeEventListener("keydown", handler); }, [onClose]);
  return <div className="modal-backdrop" role="presentation" onMouseDown={(event) => event.target === event.currentTarget && onClose()}><section className="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title"><header><h2 id="modal-title">{title}</h2><button ref={closeRef} className="icon-button" onClick={onClose} aria-label="Close details"><X/></button></header><div className="modal-content">{children}</div></section></div>;
}
