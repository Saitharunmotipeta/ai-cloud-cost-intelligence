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


// ✅ GraphQL Response Types
type InsightsResponse = {
  recentInsights: Insight[];
};

type SeverityResponse = {
  severityBreakdown: Severity[];
};

type DailyResponse = {
  dailyInsights: DailyInsight[];
};


export const useDashboard = (timeRange: string = "7d") => {

  const commonOptions = {
    errorPolicy: "all" as const,

    // 🔥 optimized polling (not too aggressive)
    pollInterval: 30000,

    // 🔥 caching strategy
    fetchPolicy: "cache-and-network" as const,
    nextFetchPolicy: "cache-first" as const,
  };


  // 🔹 Insights Query
  const insightsQuery = useQuery<InsightsResponse>(
    GET_RECENT_INSIGHTS,
    {
      ...commonOptions,
      variables: { limit: 10, timeRange },
    }
  );


  // 🔹 Severity Breakdown Query
  const severityQuery = useQuery<SeverityResponse>(
    GET_SEVERITY_BREAKDOWN,
    {
      ...commonOptions,
      variables: { timeRange },
    }
  );


  // 🔹 Daily Insights Query
  const dailyQuery = useQuery<DailyResponse>(
    GET_DAILY_INSIGHTS,
    {
      ...commonOptions,
      variables: { timeRange },
    }
  );


  // ✅ Safe Data Extraction
  const insights = insightsQuery.data?.recentInsights ?? [];
  const severity = severityQuery.data?.severityBreakdown ?? [];
  const daily = dailyQuery.data?.dailyInsights ?? [];


  // ✅ Combined Loading State
  const loading =
    insightsQuery.loading ||
    severityQuery.loading ||
    dailyQuery.loading;


  // ✅ Combined Error Handling
  const errors = [
    insightsQuery.error,
    severityQuery.error,
    dailyQuery.error,
  ].filter(Boolean);


  const error = errors.length
    ? {
        message: "Some dashboard data failed to load",
        details: errors.map((e) => e?.message ?? "Unknown error"),
      }
    : null;


  return {
    insights,
    severity,
    daily,
    loading,
    error,

    // 🔥 Partial failure detection
    isPartial:
      (!insights.length || !severity.length || !daily.length) &&
      !loading,
  };
};