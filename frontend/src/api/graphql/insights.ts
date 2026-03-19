import client from "./client";
import { GET_INSIGHTS, GET_ANOMALIES } from "./queries";

export const fetchInsights = async () => {
  const { data } = await client.query({
    query: GET_INSIGHTS,
  });
  return data.insights;
};

export const fetchAnomalies = async () => {
  const { data } = await client.query({
    query: GET_ANOMALIES,
  });
  return data.anomalies;
};