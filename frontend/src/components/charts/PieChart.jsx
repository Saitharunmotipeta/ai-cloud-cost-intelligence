import React from "react";

import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip
} from "recharts";

const COLORS = [
  "#ff4d6d",
  "#f59e0b",
  "#3b82f6",
  "#22c55e"
];

function PieChart({ data }) {

  return (

    <div className="modern-chart-wrapper">

      <ResponsiveContainer width="100%" height={340}>

        <RechartsPieChart>

          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={75}
            outerRadius={105}
            paddingAngle={4}
            dataKey="count"
            stroke="none"
          >

            {data.map((entry, index) => (

              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />

            ))}

          </Pie>

          <Tooltip
            contentStyle={{
              background: "#0b1120",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: "14px",
              color: "white"
            }}
          />

        </RechartsPieChart>

      </ResponsiveContainer>

      {/* LEGEND */}

      <div className="custom-legend">

        {data.map((item, index) => (

          <div
            className="legend-item"
            key={item.severity}
          >

            <div
              className="legend-color"
              style={{
                background:
                  COLORS[index % COLORS.length]
              }}
            />

            <span>
              {item.severity}
            </span>

          </div>

        ))}

      </div>

    </div>

  );
}

export default PieChart;