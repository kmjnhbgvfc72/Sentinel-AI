export const formatDate = (value) => value ? new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value)) : "—";
export const formatNumber = (value) => new Intl.NumberFormat().format(value ?? 0);
export const titleCase = (value = "") => value.replaceAll("-", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
