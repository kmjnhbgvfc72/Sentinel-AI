const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function getHealth(signal) {
  const response = await fetch(`${API_BASE_URL}/health`, {
    headers: { Accept: "application/json" },
    signal,
  });

  if (!response.ok) {
    throw new Error(`Health API returned ${response.status}`);
  }

  return response.json();
}
