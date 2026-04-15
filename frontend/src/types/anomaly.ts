export type Anomaly = {
  id: string;
  service: string;
  severity: string;
  explanation: string;
  timestamp: string;
};

export type GetAnomaliesResponse = {
  anomalies: Anomaly[];
};