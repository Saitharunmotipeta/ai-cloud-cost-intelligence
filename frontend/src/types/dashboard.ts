export type Insight = {
  id: string;
  service: string;
  severity: string;
  anomalyType: string;
  impact: string;
  explanation: string;
  rootCause: string;
  action: string;
  confidence: string;
  generatedAt: string;
};

export type Severity = {
  severity: string;
  count: number;
};

export type DailyInsight = {
  date: string;
  count: number;
};

export type DashboardResponse = {
  insights: Insight[];
  severityBreakdown: Severity[];
  dailyInsights: DailyInsight[];
};