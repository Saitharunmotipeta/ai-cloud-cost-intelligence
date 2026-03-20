import client from "./client";
import { GET_INSIGHTS, GET_ANOMALIES } from "./queries";

import { InsightsResponse } from "../../types/insight";
import { AnomaliesResponse } from "../../types/anomaly";

export const fetchInsights = async () => {
  const { data } = await client.query<InsightsResponse>({
    query: GET_INSIGHTS,
  });
  if (!data) {
    throw new Error("No data received from query");
  }

  return data.insights;
};

export const fetchAnomalies = async () => {
  const { data } = await client.query<AnomaliesResponse>({
    query: GET_ANOMALIES,
  });
  if (!data) {
    throw new Error("No data received from query");
  }

  return data.anomalies;
};