import client from "./client";
import {
  GET_RECENT_INSIGHTS,
  GET_ANOMALIES
} from "./queries";

import { InsightsResponse } from "../../types/insight";
import { GetAnomaliesResponse } from "../../types/anomaly";

// ✅ Insights
export const fetchInsights = async (limit = 50) => {
  const { data } = await client.query<InsightsResponse>({
    query: GET_RECENT_INSIGHTS,
    variables: { limit },
  });

  if (!data) {
    throw new Error("No data received from insights query");
  }

  return data.recentInsights; // ✅ aligned with GraphQL
};

// ✅ Anomalies (kept here based on your structure)
export const fetchAnomalies = async () => {
  const { data } = await client.query<GetAnomaliesResponse>({
    query: GET_ANOMALIES,
  });

  if (!data) {
    throw new Error("No data received from anomalies query");
  }

  return data.anomalies;
};