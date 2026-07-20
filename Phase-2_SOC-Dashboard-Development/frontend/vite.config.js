import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, "..", "");
  const proxy = env.SOC_API_PROXY_TARGET ? { "/api": { target: env.SOC_API_PROXY_TARGET, changeOrigin: true } } : undefined;
  return {
    plugins: [react()],
    server: { port: 5173, proxy },
    test: { environment: "jsdom", setupFiles: "./src/test/setup.js", globals: true },
  };
});
