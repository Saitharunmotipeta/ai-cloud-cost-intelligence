export type Insight = {
  id: string;

  accountId: string;
  service: string;

  anomalyType: string;
  severity: string;
  impact: string;

  explanation: string;
  rootCause: string;
  action: string;
  confidence: string;

  generatedAt: string;
};

export type InsightsResponse = {
  insights: Insight[]; // 🔥 MUST match GraphQL query
};