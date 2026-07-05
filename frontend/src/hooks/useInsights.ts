import { useQuery } from "@apollo/client/react";
import { useEffect } from "react";
import { GET_INSIGHTS } from "../api/graphql/queries";
import { InsightsResponse } from "../types/insight";

import { demoInsights } from "../data/insightsData";

type UseInsightsParams = {
  accountId: string;
  service?: string | null;
  severity?: string | null;
  limit?: number;
};

export const useInsights = ({
  accountId,
  service = null,
  severity = null,
  limit = 50,
}: UseInsightsParams) => {
  const query = useQuery<InsightsResponse>(GET_INSIGHTS, {
    variables: {
      accountId,
      service,
      severity,
      limit,
      offset: 0,
    },
    errorPolicy: "all",
    fetchPolicy: "network-only",
    pollInterval: 60000,
  });

  const isDemoMode = Boolean(query.error);

  const liveInsights = query.data?.insights ?? [];

  const filteredDemoInsights = demoInsights
    .filter((insight) => {
      const serviceMatches =
        !service || insight.service === service;

      const severityMatches =
        !severity || insight.severity === severity;

      return serviceMatches && severityMatches;
    })
    .slice(0, limit);

  const insights = isDemoMode
    ? filteredDemoInsights
    : liveInsights;

  const loading = isDemoMode
    ? false
    : query.loading;

  useEffect(() => {
  window.dispatchEvent(
    new CustomEvent("data-source-change", {
      detail: isDemoMode ? "DEMO" : "LIVE",
    })
  );
}, [isDemoMode]);

  const error =
    query.error && !isDemoMode
      ? {
          message: "Failed to load insights",
          details: [
            query.error?.message ?? "Unknown error",
          ],
        }
      : null;

  const isEmpty =
    !loading && insights.length === 0;

  return {
    insights,
    loading,
    error,
    isEmpty,
    isDemoMode,
    dataSource: isDemoMode ? "DEMO" : "LIVE",
  };
};