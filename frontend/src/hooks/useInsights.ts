import { useQuery } from "@apollo/client/react";
import { GET_RECENT_INSIGHTS } from "../api/graphql/queries";

export const useInsights = (limit = 50) => {
  const query = useQuery(GET_RECENT_INSIGHTS, {
    variables: { limit },
    errorPolicy: "all",
  });

  const insights = query.data?.recentInsights ?? [];

  const error = query.error
    ? {
        message: "Failed to load insights",
        details: [query.error.message],
      }
    : null;

  return {
    insights,
    loading: query.loading,
    error,
    isEmpty: !query.loading && insights.length === 0,
  };
};