import { useQuery } from "@apollo/client/react";
import {
  GET_RECENT_INSIGHTS,
  GET_SEVERITY_BREAKDOWN,
  GET_DAILY_INSIGHTS,
} from "../api/graphql/queries";

import {
  Insight,
  Severity,
  DailyInsight,
} from "../types/dashboard";

export const useDashboard = (timeRange: string = "7d") => {
  const commonOptions = {
    errorPolicy: "all" as const,
    pollInterval: 10000,
  };

  const insightsQuery = useQuery<{ recentInsights: Insight[] }>(
    GET_RECENT_INSIGHTS,
    {
      ...commonOptions,
      variables: { limit: 10, timeRange },
    }
  );

  const severityQuery = useQuery<{ severityBreakdown: Severity[] }>(
    GET_SEVERITY_BREAKDOWN,
    {
      ...commonOptions,
      variables: { timeRange },
    }
  );

  const dailyQuery = useQuery<{ dailyInsights: DailyInsight[] }>(
    GET_DAILY_INSIGHTS,
    {
      ...commonOptions,
      variables: { timeRange },
    }
  );

  const insights = insightsQuery.data?.recentInsights ?? [];
  const severity = severityQuery.data?.severityBreakdown ?? [];
  const daily = dailyQuery.data?.dailyInsights ?? [];

  const loading =
    insightsQuery.loading ||
    severityQuery.loading ||
    dailyQuery.loading;

  const errors = [
    insightsQuery.error,
    severityQuery.error,
    dailyQuery.error,
  ].filter(Boolean);

  const error = errors.length
    ? {
        message: "Some dashboard data failed to load",
        details: errors.map((e) => e?.message ?? "Unknown error")
      }
    : null;

  return {
    insights,
    severity,
    daily,
    loading,
    error,
    isPartial:
      (!insights.length || !severity.length || !daily.length) &&
      !loading,
  };
};