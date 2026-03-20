import { useQuery } from "@apollo/client/react";
import { GET_ANOMALIES } from "../api/graphql/queries";
import { GetAnomaliesResponse } from "../types/anomaly";

export const useAnomalies = (timeRange: string = "7d") => {
  const query = useQuery<GetAnomaliesResponse>(GET_ANOMALIES, {
    variables: { timeRange }, // 🔥 future ready
    errorPolicy: "all",
    fetchPolicy: "cache-and-network",
    pollInterval: 10000, // 🔥 live updates
  });

  const anomalies = query.data?.anomalies ?? [];

  const error = query.error
    ? {
        message: "Failed to load anomalies",
        details: [query.error?.message ?? "Unknown error"],
      }
    : null;

  const isEmpty = !query.loading && anomalies.length === 0;

  return {
    anomalies,
    loading: query.loading,
    error,
    isEmpty,
  };
};