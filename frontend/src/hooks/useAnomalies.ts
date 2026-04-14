import { useQuery } from "@apollo/client/react";
import { GET_ANOMALIES } from "../api/graphql/queries";
import { GetAnomaliesResponse } from "../types/anomaly";

type UseAnomaliesParams = {
  accountId: string | null;
};

export const useAnomalies = ({ accountId }: UseAnomaliesParams) => {

  // 🚨 prevent invalid GraphQL call
  const shouldSkip = !accountId;

  const query = useQuery<GetAnomaliesResponse>(GET_ANOMALIES, {
    variables: {
      accountId,
    },
    errorPolicy: "all",
    fetchPolicy: "network-only",
    pollInterval: 120000,   // 🔥 2 min (lighter than dashboard)
    skip: shouldSkip,       // 🔥 CRITICAL FIX
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