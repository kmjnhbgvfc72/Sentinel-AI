import { useCallback, useEffect, useRef, useState } from "react";

export function useApi(loader, dependencies = [], { pollMs = 0 } = {}) {
  const [state, setState] = useState({ data: null, loading: true, error: null, updatedAt: null });
  const mounted = useRef(true);
  const load = useCallback(async () => {
    setState((current) => ({ ...current, loading: current.data === null, error: null }));
    try {
      const response = await loader();
      if (mounted.current) setState({ data: response, loading: false, error: null, updatedAt: new Date() });
    } catch (error) {
      if (mounted.current) setState((current) => ({ ...current, loading: false, error, updatedAt: current.updatedAt }));
    }
  }, dependencies); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    mounted.current = true;
    load();
    let timer;
    const schedule = () => { clearInterval(timer); if (pollMs && !document.hidden) timer = setInterval(load, pollMs); };
    schedule();
    document.addEventListener("visibilitychange", schedule);
    return () => { mounted.current = false; clearInterval(timer); document.removeEventListener("visibilitychange", schedule); };
  }, [load, pollMs]);
  return { ...state, retry: load };
}
