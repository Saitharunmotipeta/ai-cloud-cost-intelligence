export type Insight = {
  insight_id: string;
  service: string;
  severity: string;
  message: string;
  recommendation: string;
  generated_at: string;
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
  recentInsights: Insight[];
  severityBreakdown: Severity[];
  dailyInsights: DailyInsight[];
};