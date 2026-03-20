export const formatDate = (dateString: string) => {
  if (!dateString) return "-";

  try {
    const date = new Date(dateString);

    // Invalid date safety
    if (isNaN(date.getTime())) return "-";

    return date.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (err) {
    return "-";
  }
};