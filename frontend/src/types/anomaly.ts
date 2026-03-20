export type Anomaly = {
  event_id: string;
  service: string;
  cost: number;
  deviation: number;
};

export type AnomaliesResponse = {
  anomalies: Anomaly[];
};