export function formatTimestamp(value) {
  if (!value) return "Awaiting response";
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "medium",
  }).format(new Date(value));
}

export function statusLabel(status) {
  return status === "healthy" ? "Operational" : "Unavailable";
}
