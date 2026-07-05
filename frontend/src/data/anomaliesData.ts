import { Anomaly } from "../types/anomaly";

export const demoAnomalies: Anomaly[] = [
  {
    id: "demo-anomaly-001",
    service: "EC2",
    severity: "HIGH",
    explanation:
      "EC2 compute cost increased by 34% compared with the previous monitoring period due to extended instance runtime.",
    timestamp: "2026-07-05T10:42:00Z",
  },
  {
    id: "demo-anomaly-002",
    service: "RDS",
    severity: "MEDIUM",
    explanation:
      "RDS utilization remained below 18% while the provisioned database capacity remained unchanged.",
    timestamp: "2026-07-05T08:15:00Z",
  },
  {
    id: "demo-anomaly-003",
    service: "Lambda",
    severity: "HIGH",
    explanation:
      "Lambda invocation volume increased unexpectedly after repeated processing of duplicate monitoring events.",
    timestamp: "2026-07-04T21:30:00Z",
  },
  {
    id: "demo-anomaly-004",
    service: "S3",
    severity: "MEDIUM",
    explanation:
      "S3 storage consumption increased continuously due to historical monitoring exports being retained without lifecycle expiration.",
    timestamp: "2026-07-04T16:20:00Z",
  },
  {
    id: "demo-anomaly-005",
    service: "EC2",
    severity: "LOW",
    explanation:
      "A development EC2 instance remained active for several hours with CPU utilization below 5%.",
    timestamp: "2026-07-04T12:05:00Z",
  },
  {
    id: "demo-anomaly-006",
    service: "CloudWatch",
    severity: "MEDIUM",
    explanation:
      "Monitoring log ingestion volume increased significantly during the latest observation window.",
    timestamp: "2026-07-03T19:45:00Z",
  },
  {
    id: "demo-anomaly-007",
    service: "API Gateway",
    severity: "HIGH",
    explanation:
      "API request traffic experienced a sudden burst that exceeded the recent baseline by 47%.",
    timestamp: "2026-07-03T14:10:00Z",
  },
  {
    id: "demo-anomaly-008",
    service: "RDS",
    severity: "LOW",
    explanation:
      "Database connection activity decreased while provisioned infrastructure capacity remained constant.",
    timestamp: "2026-07-02T22:35:00Z",
  },
  {
    id: "demo-anomaly-009",
    service: "S3",
    severity: "MEDIUM",
    explanation:
      "Frequent object retrieval operations produced an unusual increase in storage access activity.",
    timestamp: "2026-07-02T17:50:00Z",
  },
  {
    id: "demo-anomaly-010",
    service: "Lambda",
    severity: "LOW",
    explanation:
      "Average Lambda execution duration increased moderately compared with the established execution baseline.",
    timestamp: "2026-07-01T11:25:00Z",
  },
];