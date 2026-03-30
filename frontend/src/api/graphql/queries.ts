import { gql } from "@apollo/client";

// 🔥 UPDATED INSIGHTS (FULL STRUCTURED)
export const GET_INSIGHTS = gql`
  query GetInsights {
    insights(accountId: "11111111-1111-1111-1111-111111111111") {
      id
      service
      anomalyType
      severity
      impact
      explanation
      rootCause
      action
      confidence
      generatedAt
    }
  }
`;

// 🔥 UPDATED RECENT INSIGHTS
export const GET_RECENT_INSIGHTS = gql`
  query GetRecentInsights($limit: Int!) {
    recentInsights(limit: $limit) {
      id
      service
      anomalyType
      severity
      impact
      explanation
      rootCause
      action
      confidence
      generatedAt
    }
  }
`;

// ✅ NO CHANGE NEEDED
export const GET_SEVERITY_BREAKDOWN = gql`
  query GetSeverityBreakdown {
    severityBreakdown {
      severity
      count
    }
  }
`;

// ✅ NO CHANGE NEEDED
export const GET_DAILY_INSIGHTS = gql`
  query GetDailyInsights {
    dailyInsights {
      date
      count
    }
  }
`;

// 🔥 OPTIONAL UPGRADE (better anomaly view later)
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