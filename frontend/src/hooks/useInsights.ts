import { useQuery } from "@apollo/client/react";
import { GET_INSIGHTS } from "../api/graphql/queries";
import { InsightsResponse } from "../types/insight";

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

  const insights = query.data?.insights ?? [];

  const error = query.error
    ? {
        message: "Failed to load insights",
        details: [query.error?.message ?? "Unknown error"],
      }
    : null;

  const isEmpty = !query.loading && insights.length === 0;

  return {
    insights,
    loading: query.loading,
    error,
    isEmpty,
  };
};