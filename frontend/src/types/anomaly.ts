export type Anomaly = {
  service: string;
  expectedCost: number;
  actualCost: number;
  deviation: number;
  severity: string;        // 🔥 ADD THIS
  timestamp: string;
};

export type GetAnomaliesResponse = {
  anomalies: Anomaly[];
};