import React from 'react'
import { LineChart as RechartsLineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

function LineChart({ data }) {
  return (
    <div className="chart-wrapper">
      <ResponsiveContainer width="100%" height={300}>
        <RechartsLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#3498db" strokeWidth={2} />
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default LineChart