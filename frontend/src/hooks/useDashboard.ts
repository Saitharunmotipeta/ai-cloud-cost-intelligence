import { useQuery } from "@apollo/client/react";

import {
  GET_INSIGHTS,
  GET_SEVERITY_BREAKDOWN,
  GET_DAILY_INSIGHTS,
} from "../api/graphql/queries";

import {
  Insight,
  Severity,
  DailyInsight,
} from "../types/dashboard";

type InsightsResponse = {
  insights: Insight[];
};

type SeverityResponse = {
  severityBreakdown: Severity[];
};

type DailyResponse = {
  dailyInsights: DailyInsight[];
};

type UseDashboardParams = {
  accountId: string | null;
  service?: string | null;
  severity?: string | null;
};

export const useDashboard = ({
  accountId,
  service = null,
  severity = null,
}: UseDashboardParams) => {

  // 🚨 SAFETY: prevent invalid GraphQL call
  const shouldSkip = !accountId;

  const commonOptions = {
    errorPolicy: "all" as const,
    fetchPolicy: "network-only" as const,
    pollInterval: 60000, // 🔥 keep 1 min or increase later
    skip: shouldSkip,    // 🔥 CRITICAL FIX
  };

  // 🔥 Insights (FILTERED)
  const insightsQuery = useQuery<InsightsResponse>(
    GET_INSIGHTS,
    {
      ...commonOptions,
      variables: {
        accountId,
        service,
        severity,
        limit: 10,
        offset: 0,
      },
    }
  );

  // 🔥 Severity Breakdown
  const severityQuery = useQuery<SeverityResponse>(
    GET_SEVERITY_BREAKDOWN,
    {
      ...commonOptions,
      variables: { accountId },
    }
  );

  // 🔥 Daily Insights
  const dailyQuery = useQuery<DailyResponse>(
    GET_DAILY_INSIGHTS,
    {
      ...commonOptions,
      variables: { accountId },
    }
  );

  const insights = insightsQuery.data?.insights ?? [];
  const severityData = severityQuery.data?.severityBreakdown ?? [];
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
        details: errors.map((e) => e?.message ?? "Unknown error"),
      }
    : null;

  return {
    insights,
    severity: severityData,
    daily,
    loading,
    error,
    isPartial:
      (!insights.length || !severityData.length || !daily.length) &&
      !loading,
  };
};