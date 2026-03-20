import { useQuery } from "@apollo/client/react";
import { GET_RECENT_INSIGHTS } from "../api/graphql/queries";
import { InsightsResponse } from "../types/insight";

export const useInsights = (limit = 50) => {
  const query = useQuery<InsightsResponse>(GET_RECENT_INSIGHTS, {
    variables: { limit },
    errorPolicy: "all",
    fetchPolicy: "cache-and-network", // ✅ upgrade
  });

  const insights = query.data?.recentInsights ?? [];

  const error = query.error
    ? {
        message: "Failed to load insights",
        details: [query.error.message],
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