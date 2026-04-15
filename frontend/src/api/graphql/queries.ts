import { gql } from "@apollo/client";


// 🔥 MAIN INSIGHTS (FILTERABLE)
export const GET_INSIGHTS = gql`
  query GetInsights(
    $accountId: String!
    $service: String
    $severity: String
    $limit: Int
    $offset: Int
  ) {
    insights(
      accountId: $accountId
      service: $service
      severity: $severity
      limit: $limit
      offset: $offset
    ) {
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


// 🔥 SEVERITY BREAKDOWN (ACCOUNT SAFE)
export const GET_SEVERITY_BREAKDOWN = gql`
  query GetSeverityBreakdown($accountId: String!) {
    severityBreakdown(accountId: $accountId) {
      severity
      count
    }
  }
`;


// 🔥 DAILY INSIGHTS (ACCOUNT SAFE)
export const GET_DAILY_INSIGHTS = gql`
  query GetDailyInsights($accountId: String!) {
    dailyInsights(accountId: $accountId) {
      date
      count
    }
  }
`;


export const GET_ANOMALIES = gql`
  query GetAnomalies($accountId: String!) {
    anomalies(accountId: $accountId) {
      id
      service
      severity
      explanation
      timestamp
    }
  }
`;