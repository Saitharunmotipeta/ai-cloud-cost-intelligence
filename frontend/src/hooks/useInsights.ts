import { useEffect, useState } from "react";
import { fetchInsights } from "../api/graphql/insights";

export const useInsights = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetchInsights();
        setData(res);
      } catch (err) {
        setError(err.message || "Error fetching insights");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return { data, loading, error };
};