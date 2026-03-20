export type Anomaly = {
  service: string;
  expectedCost: number;
  actualCost: number;
  deviation: number;
  timestamp: string;
};

export type GetAnomaliesResponse = {
  anomalies: Anomaly[];
};