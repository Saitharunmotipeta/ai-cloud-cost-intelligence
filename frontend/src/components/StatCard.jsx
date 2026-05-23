import React from 'react'
import SkeletonCard from './skeletons/SkeletonCard'

function StatCard({
  title,
  value,
  color = 'blue',
  loading = false
}) {

  const colorClasses = {
    blue: 'stat-card-blue',
    red: 'stat-card-red',
    green: 'stat-card-green',
    yellow: 'stat-card-yellow'
  }

  // ✅ Keep skeleton loading
  if (loading) {
    return <SkeletonCard />
  }

  return (

    <div className={`modern-stat-card ${colorClasses[color]}`}>

      <div className="card-top">
        <span>{title}</span>
      </div>

      <div className="card-value">
        {value ?? 0}
      </div>

    </div>

  )
}

export default StatCard