import React from 'react'

function StatCard({ title, value, color = 'blue' }) {
  const colorClasses = {
    blue: 'stat-card-blue',
    red: 'stat-card-red',
    green: 'stat-card-green',
    yellow: 'stat-card-yellow'
  }

  return (
    <div className={`stat-card ${colorClasses[color]}`}>
      <h3>{title}</h3>
      <div className="stat-value">{value}</div>
    </div>
  )
}

export default StatCard