import { useQuery } from "@apollo/client/react";
import { useEffect } from "react";
import { GET_ANOMALIES } from "../api/graphql/queries";
import { GetAnomaliesResponse } from "../types/anomaly";

import { demoAnomalies } from "../data/anomaliesData";

type UseAnomaliesParams = {
  accountId: string | null;
};

export const useAnomalies = ({
  accountId,
}: UseAnomaliesParams) => {
  // Prevent invalid GraphQL call
  const shouldSkip = !accountId;

  const query = useQuery<GetAnomaliesResponse>(
    GET_ANOMALIES,
    {
      variables: {
        accountId,
      },
      errorPolicy: "all",
      fetchPolicy: "network-only",
      pollInterval: 120000,
      skip: shouldSkip,
    }
  );

  const isDemoMode =
    !shouldSkip && Boolean(query.error);

  useEffect(() => {
  window.dispatchEvent(
    new CustomEvent("data-source-change", {
      detail: isDemoMode ? "DEMO" : "LIVE",
    })
  );
}, [isDemoMode]);

  const liveAnomalies =
    query.data?.anomalies ?? [];

  const anomalies = isDemoMode
    ? demoAnomalies
    : liveAnomalies;

  const loading = isDemoMode
    ? false
    : query.loading;

  const error =
    query.error && !isDemoMode
      ? {
          message: "Failed to load anomalies",
          details: [
            query.error?.message ?? "Unknown error",
          ],
        }
      : null;

  const isEmpty =
    !loading && anomalies.length === 0;

  return {
    anomalies,
    loading,
    error,
    isEmpty,
    isDemoMode,
    dataSource: isDemoMode ? "DEMO" : "LIVE",
  };
};