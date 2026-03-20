import React from 'react'
import SkeletonCard from './skeletons/SkeletonCard'

function StatCard({ title, value, color = 'blue', loading = false }) {
  const colorClasses = {
    blue: 'stat-card-blue',
    red: 'stat-card-red',
    green: 'stat-card-green',
    yellow: 'stat-card-yellow'
  }

  // ✅ NEW: loading support
  if (loading) {
    return <SkeletonCard />
  }

  return (
    <div className={`stat-card ${colorClasses[color]}`}>
      <h3>{title}</h3>
      <div className="stat-value">
        {value ?? 0}
      </div>
    </div>
  )
}

export default StatCard