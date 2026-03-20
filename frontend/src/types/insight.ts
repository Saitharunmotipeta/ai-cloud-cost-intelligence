export type Insight = {
  insight_id: string;
  account_id: string;
  service: string;
  severity: string;
  message: string;
  recommendation: string;
  generated_at: string;
};

export type InsightsResponse = {
  recentInsights: Insight[]; // ✅ MUST match GraphQL response
};