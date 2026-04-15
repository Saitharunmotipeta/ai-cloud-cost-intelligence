import client from "./client";
import {
  GET_INSIGHTS,
  GET_ANOMALIES
} from "./queries";

import { InsightsResponse } from "../../types/insight";
import { GetAnomaliesResponse } from "../../types/anomaly";

// 🔥 Insights (UPDATED)
export const fetchInsights = async (
  accountId: string,
  limit = 50
) => {

  const { data } = await client.query<InsightsResponse>({
    query: GET_INSIGHTS,
    variables: {
      accountId,
      limit,
      offset: 0
    },
    fetchPolicy: "network-only",
  });

  if (!data) {
    throw new Error("No data received from insights query");
  }

  return data.insights; // ✅ FIXED
};


// 🔥 Anomalies (UPDATED)
export const fetchAnomalies = async (accountId: string) => {

  const { data } = await client.query<GetAnomaliesResponse>({
    query: GET_ANOMALIES,
    variables: {
      accountId   // 🔥 REQUIRED
    },
    fetchPolicy: "network-only",
  });

  if (!data) {
    throw new Error("No data received from anomalies query");
  }

  return data.anomalies;
};