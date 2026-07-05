import { useQuery } from "@apollo/client/react";
import { useEffect } from "react";

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

import {
  demoDashboardInsights,
  demoSeverityBreakdown,
  demoDailyInsights,
} from "../data/dashboardData";

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
  const shouldSkip = !accountId;

  const commonOptions = {
    errorPolicy: "all" as const,
    fetchPolicy: "network-only" as const,
    pollInterval: 1500000,
    skip: shouldSkip,
  };

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

  const severityQuery = useQuery<SeverityResponse>(
    GET_SEVERITY_BREAKDOWN,
    {
      ...commonOptions,
      variables: { accountId },
    }
  );

  const dailyQuery = useQuery<DailyResponse>(
    GET_DAILY_INSIGHTS,
    {
      ...commonOptions,
      variables: { accountId },
    }
  );

  const hasQueryError =
    Boolean(insightsQuery.error) ||
    Boolean(severityQuery.error) ||
    Boolean(dailyQuery.error);

  const isDemoMode = !shouldSkip && hasQueryError;

  const liveInsights = insightsQuery.data?.insights ?? [];
  const liveSeverity =
    severityQuery.data?.severityBreakdown ?? [];
  const liveDaily = dailyQuery.data?.dailyInsights ?? [];

  const filteredDemoInsights = demoDashboardInsights.filter(
    (insight) => {
      const serviceMatches =
        !service || insight.service === service;

      const severityMatches =
        !severity || insight.severity === severity;

      return serviceMatches && severityMatches;
    }
  );

  const insights = isDemoMode
    ? filteredDemoInsights
    : liveInsights;

  const severityData = isDemoMode
    ? demoSeverityBreakdown
    : liveSeverity;

  const daily = isDemoMode
    ? demoDailyInsights
    : liveDaily;

  const loading = isDemoMode
    ? false
    : insightsQuery.loading ||
      severityQuery.loading ||
      dailyQuery.loading;

  useEffect(() => {
    window.dispatchEvent(
      new CustomEvent("data-source-change", {
        detail: isDemoMode ? "DEMO" : "LIVE",
      })
    );
  }, [isDemoMode]);

  const errors = [
    insightsQuery.error,
    severityQuery.error,
    dailyQuery.error,
  ].filter(Boolean);

  const error =
    errors.length && !isDemoMode
      ? {
          message: "Some dashboard data failed to load",
          details: errors.map(
            (e) => e?.message ?? "Unknown error"
          ),
        }
      : null;

  return {
    insights,
    severity: severityData,
    daily,
    loading,
    error,
    isDemoMode,
    dataSource: isDemoMode ? "DEMO" : "LIVE",
    isPartial:
      (!insights.length ||
        !severityData.length ||
        !daily.length) &&
      !loading,
  };
};