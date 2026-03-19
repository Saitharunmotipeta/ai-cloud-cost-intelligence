import { useEffect, useState } from "react";
import { fetchAnomalies } from "../api/graphql/insights";

export const useAnomalies = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchAnomalies();
        setData(res);
      } catch (err) {
        setError(err.message || "Error fetching anomalies");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { data, loading, error };
};