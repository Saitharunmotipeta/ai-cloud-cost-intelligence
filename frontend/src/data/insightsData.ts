import { Insight } from "../types/insight";

export const demoInsights: Insight[] = [
  {
    id: "demo-insight-001",
    accountId: "123456789012",
    service: "EC2",
    anomalyType: "COST_SPIKE",
    severity: "HIGH",
    impact:
      "Monthly compute expenditure may increase by approximately 32% if the current usage pattern continues.",
    explanation:
      "EC2 compute spending increased significantly compared with the established historical cost baseline.",
    rootCause:
      "Multiple compute instances remained active during extended low-traffic periods.",
    action:
      "Review instance utilization, apply scheduled shutdown policies, and evaluate rightsizing opportunities.",
    confidence: "94%",
    generatedAt: "2026-07-05T09:30:00Z",
  },
  {
    id: "demo-insight-002",
    accountId: "123456789012",
    service: "RDS",
    anomalyType: "UNDERUTILIZED_RESOURCE",
    severity: "MEDIUM",
    impact:
      "The current database configuration is producing avoidable infrastructure expenditure.",
    explanation:
      "Average RDS utilization remained consistently below the expected operational capacity.",
    rootCause:
      "The provisioned database instance class exceeds the requirements of the current workload.",
    action:
      "Evaluate recent CPU and memory utilization and consider migrating to a smaller RDS instance class.",
    confidence: "89%",
    generatedAt: "2026-07-04T14:15:00Z",
  },
  {
    id: "demo-insight-003",
    accountId: "123456789012",
    service: "Lambda",
    anomalyType: "EXECUTION_INCREASE",
    severity: "HIGH",
    impact:
      "Repeated serverless executions may increase invocation and compute charges.",
    explanation:
      "Lambda invocation volume increased unexpectedly during recent event-processing windows.",
    rootCause:
      "Duplicate monitoring events triggered repeated function executions.",
    action:
      "Introduce idempotency validation and review event retry behavior before processing Lambda workloads.",
    confidence: "92%",
    generatedAt: "2026-07-04T08:40:00Z",
  },
  {
    id: "demo-insight-004",
    accountId: "123456789012",
    service: "S3",
    anomalyType: "STORAGE_GROWTH",
    severity: "MEDIUM",
    impact:
      "Persistent storage growth may gradually increase monthly cloud expenditure.",
    explanation:
      "S3 storage consumption has increased continuously across recent monitoring periods.",
    rootCause:
      "Historical monitoring exports and processed reports are retained without lifecycle expiration policies.",
    action:
      "Configure lifecycle policies to transition historical objects to lower-cost storage tiers or expire unnecessary data.",
    confidence: "91%",
    generatedAt: "2026-07-03T18:20:00Z",
  },
  {
    id: "demo-insight-005",
    accountId: "123456789012",
    service: "EC2",
    anomalyType: "IDLE_RESOURCE",
    severity: "HIGH",
    impact:
      "An idle compute resource is contributing directly to unnecessary cloud spend.",
    explanation:
      "An EC2 instance remained continuously active while maintaining CPU utilization below 5%.",
    rootCause:
      "A development workload completed, but the associated compute instance was not stopped.",
    action:
      "Stop the idle instance and introduce automated scheduling for non-production compute resources.",
    confidence: "96%",
    generatedAt: "2026-07-03T11:10:00Z",
  },
  {
    id: "demo-insight-006",
    accountId: "123456789012",
    service: "CloudWatch",
    anomalyType: "LOG_INGESTION_GROWTH",
    severity: "MEDIUM",
    impact:
      "Higher log ingestion volume may increase monitoring and storage costs.",
    explanation:
      "CloudWatch log ingestion increased significantly compared with the previous observation window.",
    rootCause:
      "Verbose application logging generated a high volume of repetitive informational events.",
    action:
      "Review production logging levels and reduce repetitive non-critical log events.",
    confidence: "87%",
    generatedAt: "2026-07-02T20:45:00Z",
  },
  {
    id: "demo-insight-007",
    accountId: "123456789012",
    service: "API Gateway",
    anomalyType: "TRAFFIC_BURST",
    severity: "HIGH",
    impact:
      "Sustained request growth may increase API processing costs and backend workload.",
    explanation:
      "API request volume exceeded the recent traffic baseline by approximately 47%.",
    rootCause:
      "A sudden burst of dashboard polling requests created additional API traffic.",
    action:
      "Review frontend polling intervals and introduce caching for frequently requested dashboard data.",
    confidence: "93%",
    generatedAt: "2026-07-02T14:30:00Z",
  },
  {
    id: "demo-insight-008",
    accountId: "123456789012",
    service: "RDS",
    anomalyType: "CAPACITY_MISMATCH",
    severity: "LOW",
    impact:
      "Provisioned database capacity is not being fully utilized.",
    explanation:
      "Database connection activity decreased while the allocated infrastructure capacity remained unchanged.",
    rootCause:
      "The application workload reduced without a corresponding database capacity adjustment.",
    action:
      "Monitor workload trends and evaluate database rightsizing if low utilization continues.",
    confidence: "84%",
    generatedAt: "2026-07-01T17:25:00Z",
  },
];