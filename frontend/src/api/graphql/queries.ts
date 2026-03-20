import { gql } from "@apollo/client";

export const GET_RECENT_INSIGHTS = gql`
  query GetRecentInsights($limit: Int!) {
    recentInsights(limit: $limit) {
      service
      message
      recommendation
      severity
      generatedAt
    }
  }
`;

export const GET_SEVERITY_BREAKDOWN = gql`
  query GetSeverityBreakdown {
    severityBreakdown {
      severity
      count
    }
  }
`;

export const GET_DAILY_INSIGHTS = gql`
  query GetDailyInsights {
    dailyInsights {
      date
      count
    }
  }
`;

export const GET_ANOMALIES = gql`
  query GetAnomalies {
    anomalies {
      service
      expectedCost
      actualCost
      deviation
      timestamp
    }
  }
`;

export const GET_INSIGHTS = gql`
  query GetInsights {
    insights {
      service
      message
      recommendation
      severity
      generatedAt
    }
  }
`;