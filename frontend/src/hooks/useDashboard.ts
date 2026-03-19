import { useQuery } from "@apollo/client/react";
import {
  GET_RECENT_INSIGHTS,
  GET_SEVERITY_BREAKDOWN,
  GET_DAILY_INSIGHTS,
} from "../api/graphql/queries";

export const useDashboard = () => {
  const insightsQuery = useQuery(GET_RECENT_INSIGHTS, {
    variables: { limit: 10 },
    errorPolicy: "all", // ✅ allow partial success
  });

  const severityQuery = useQuery(GET_SEVERITY_BREAKDOWN, {
    errorPolicy: "all",
  });

  const dailyQuery = useQuery(GET_DAILY_INSIGHTS, {
    errorPolicy: "all",
  });

  // ✅ Safe data extraction
  const insights = insightsQuery.data?.recentInsights ?? [];
  const severity = severityQuery.data?.severityBreakdown ?? [];
  const daily = dailyQuery.data?.dailyInsights ?? [];

  // ✅ Granular loading
  const loading =
    insightsQuery.loading ||
    severityQuery.loading ||
    dailyQuery.loading;

  // ✅ Graceful error handling
  const errors = [
    insightsQuery.error,
    severityQuery.error,
    dailyQuery.error,
  ].filter(Boolean);

  const hasError = errors.length > 0;

  // ✅ Structured error (not raw Apollo error)
  const error = hasError
    ? {
        message: "Some dashboard data failed to load",
        details: errors.map((e) => e.message),
      }
    : null;

  return {
    insights,
    severity,
    daily,
    loading,
    error,

    // 🔥 optional advanced flags
    isPartial:
      (!insights.length || !severity.length || !daily.length) &&
      !loading,
  };
};