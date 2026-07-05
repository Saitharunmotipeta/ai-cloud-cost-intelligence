import {
  Insight,
  Severity,
  DailyInsight,
} from "../types/dashboard";

export const demoDashboardInsights: Insight[] = [
  {
    id: "demo-insight-001",
    service: "EC2",
    severity: "HIGH",
    anomalyType: "COST_SPIKE",
    impact: "Monthly compute cost increased by approximately 32%.",
    explanation:
      "EC2 usage increased significantly compared with the previous usage pattern.",
    rootCause:
      "A compute instance remained active during low-traffic hours.",
    action:
      "Review instance utilization and consider scheduled shutdown or rightsizing.",
    confidence: "94%",
    generatedAt: "2026-07-05T09:30:00Z",
  },
  {
    id: "demo-insight-002",
    service: "RDS",
    severity: "MEDIUM",
    anomalyType: "UNDERUTILIZED_RESOURCE",
    impact: "Database infrastructure is generating avoidable operational cost.",
    explanation:
      "Average database utilization remained below expected capacity.",
    rootCause:
      "The provisioned database instance is larger than the current workload requires.",
    action:
      "Evaluate a smaller RDS instance class based on recent utilization metrics.",
    confidence: "89%",
    generatedAt: "2026-07-04T14:15:00Z",
  },
  {
    id: "demo-insight-003",
    service: "Lambda",
    severity: "LOW",
    anomalyType: "EXECUTION_INCREASE",
    impact: "Serverless execution cost may gradually increase.",
    explanation:
      "Lambda invocation volume increased during recent processing windows.",
    rootCause:
      "Repeated event processing caused additional function invocations.",
    action:
      "Review event triggers and validate idempotency in the processing workflow.",
    confidence: "86%",
    generatedAt: "2026-07-03T18:45:00Z",
  },
  {
    id: "demo-insight-004",
    service: "S3",
    severity: "MEDIUM",
    anomalyType: "STORAGE_GROWTH",
    impact: "Storage cost is trending upward due to retained historical objects.",
    explanation:
      "S3 storage consumption has steadily increased over the recent monitoring period.",
    rootCause:
      "Old monitoring exports and historical data are being retained indefinitely.",
    action:
      "Configure an S3 lifecycle policy to archive or expire older objects.",
    confidence: "91%",
    generatedAt: "2026-07-02T11:20:00Z",
  },
  {
    id: "demo-insight-005",
    service: "EC2",
    severity: "HIGH",
    anomalyType: "IDLE_RESOURCE",
    impact: "An idle compute resource is contributing to unnecessary cloud spend.",
    explanation:
      "The instance showed consistently low CPU activity while remaining continuously available.",
    rootCause:
      "A development instance was not stopped after the workload completed.",
    action:
      "Stop the instance during inactive periods and evaluate automated scheduling.",
    confidence: "96%",
    generatedAt: "2026-07-01T08:10:00Z",
  },
];

export const demoSeverityBreakdown: Severity[] = [
  {
    severity: "HIGH",
    count: 8,
  },
  {
    severity: "MEDIUM",
    count: 13,
  },
  {
    severity: "LOW",
    count: 6,
  },
];

export const demoDailyInsights: DailyInsight[] = [
  {
    date: "2026-06-29",
    count: 3,
  },
  {
    date: "2026-06-30",
    count: 5,
  },
  {
    date: "2026-07-01",
    count: 4,
  },
  {
    date: "2026-07-02",
    count: 7,
  },
  {
    date: "2026-07-03",
    count: 6,
  },
  {
    date: "2026-07-04",
    count: 8,
  },
  {
    date: "2026-07-05",
    count: 5,
  },
];