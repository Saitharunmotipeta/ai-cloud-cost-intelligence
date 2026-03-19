import { gql } from '@apollo/client'

export const GET_RECENT_INSIGHTS = gql`
  query GetRecentInsights($limit: Int) {
    recent_insights(limit: $limit) {
      id
      account_id
      service
      severity
      message
      recommendation
      generated_at
    }
  }
`

export const GET_SEVERITY_BREAKDOWN = gql`
  query GetSeverityBreakdown {
    severity_breakdown {
      severity
      count
    }
  }
`

export const GET_DAILY_INSIGHTS = gql`
  query GetDailyInsights {
    daily_insights {
      date
      count
    }
  }
`

export const GET_SERVICE_SUMMARY = gql`
  query GetServiceSummary($account_id: String!) {
    service_summary(account_id: $account_id) {
      service
      total_count
    }
  }
`