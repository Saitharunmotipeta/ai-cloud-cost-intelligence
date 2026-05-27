import React from "react";

import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart
} from "recharts";

function LineChart({ data }) {

  return (

    <div className="modern-chart-wrapper">

      <ResponsiveContainer width="100%" height={340}>

        <AreaChart data={data}>

          <defs>

            <linearGradient
              id="colorInsights"
              x1="0"
              y1="0"
              x2="0"
              y2="1"
            >

              <stop
                offset="0%"
                stopColor="#6d5dfc"
                stopOpacity={0.45}
              />

              <stop
                offset="100%"
                stopColor="#6d5dfc"
                stopOpacity={0}
              />

            </linearGradient>

          </defs>

          <CartesianGrid
            stroke="rgba(255,255,255,0.05)"
            vertical={false}
          />

          <XAxis
            dataKey="date"
            tick={{
              fill: "rgba(255,255,255,0.55)",
              fontSize: 12
            }}
            axisLine={false}
            tickLine={false}
          />

          <YAxis
            tick={{
              fill: "rgba(255,255,255,0.55)",
              fontSize: 12
            }}
            axisLine={false}
            tickLine={false}
          />

          <Tooltip
            contentStyle={{
              background: "#0b1120",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: "14px",
              color: "white"
            }}
          />

          <Area
            type="monotone"
            dataKey="count"
            stroke="none"
            fill="url(#colorInsights)"
          />

          <Line
            type="monotone"
            dataKey="count"
            stroke="#6d5dfc"
            strokeWidth={3}
            dot={false}
            activeDot={{
              r: 6,
              fill: "#ffffff",
              stroke: "#6d5dfc",
              strokeWidth: 3
            }}
          />

        </AreaChart>

      </ResponsiveContainer>

    </div>

  );
}

export default LineChart;