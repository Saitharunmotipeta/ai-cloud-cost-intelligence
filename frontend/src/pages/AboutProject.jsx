import React from "react";

import {
  BrainCircuit,
  ShieldAlert,
  TrendingUp,
  Activity,
  ArrowRight
} from "lucide-react";

const problems = [

  {
    title: "Rising Cloud Costs",
    icon: <TrendingUp size={28} />,
    description:
      "Modern cloud infrastructure scales rapidly, making it difficult to track unnecessary spending across services."
  },

  {
    title: "Hidden Usage Spikes",
    icon: <Activity size={28} />,
    description:
      "Unexpected traffic surges and inefficient workloads can silently increase operational expenses."
  },

  {
    title: "Manual Monitoring",
    icon: <ShieldAlert size={28} />,
    description:
      "Traditional monitoring requires teams to manually investigate logs, metrics, and billing anomalies."
  },

  {
    title: "Delayed Optimization",
    icon: <BrainCircuit size={28} />,
    description:
      "Without intelligent automation, optimization opportunities are often discovered too late."
  }

];

const workflow = [
  "Collect Cloud Metrics",
  "Detect Spending Anomalies",
  "Analyze Usage Patterns",
  "Generate AI Insights",
  "Recommend Optimizations"
];

export default function About() {

  return (

    <div className="about-page">

      {/* =========================
          HERO
      ========================= */}

      <section className="about-main-hero">

        <div className="about-main-glow"></div>

        <div className="about-main-content">

          <div className="about-chip">
            WHY THIS PLATFORM EXISTS
          </div>

          <h1>
            Intelligent cloud monitoring
            for modern infrastructure
          </h1>

          <p>
            AI Cloud Cost Intelligence Engine helps organizations
            detect abnormal cloud spending, identify operational
            inefficiencies, and generate intelligent optimization
            recommendations before infrastructure costs escalate.
          </p>

        </div>

      </section>

      {/* =========================
          PROBLEM SECTION
      ========================= */}

      <section className="about-section">

        <div className="section-heading">

          <h2>
            The problem with cloud cost management
          </h2>

          <p>
            Cloud environments grow rapidly.
            Monitoring them manually becomes increasingly difficult.
          </p>

        </div>

        <div className="about-grid">

          {problems.map((item) => (

            <div
              key={item.title}
              className="about-problem-card"
            >

              <div className="problem-icon">
                {item.icon}
              </div>

              <h3>
                {item.title}
              </h3>

              <p>
                {item.description}
              </p>

            </div>

          ))}

        </div>

      </section>

      {/* =========================
          WORKFLOW
      ========================= */}

      <section className="about-section">

        <div className="section-heading">

          <h2>
            How the platform works
          </h2>

          <p>
            The system continuously monitors cloud activity
            and transforms raw infrastructure data into
            intelligent optimization insights.
          </p>

        </div>

        <div className="workflow-container">

          {workflow.map((step, index) => (

            <React.Fragment key={step}>

              <div className="workflow-step">

                <div className="workflow-number">
                  {index + 1}
                </div>

                <span>
                  {step}
                </span>

              </div>

              {index !== workflow.length - 1 && (
                <ArrowRight
                  className="workflow-arrow"
                  size={20}
                />
              )}

            </React.Fragment>

          ))}

        </div>

      </section>

      {/* =========================
          REAL WORLD EXAMPLE
      ========================= */}

      <section className="about-section">

        <div className="use-case-card">

          <div className="use-case-badge">
            REAL WORLD USE CASE
          </div>

          <h2>
            Example scenario
          </h2>

          <p>
            A company deploys a new product update.
            Traffic unexpectedly spikes overnight,
            causing cloud infrastructure costs to increase by 70%.
          </p>

          <p>
            The AI engine immediately detects abnormal spending patterns,
            identifies the affected services, analyzes the possible root cause,
            and recommends optimization actions before the costs continue rising.
          </p>

        </div>

      </section>

      {/* =========================
          WHY AI
      ========================= */}

      <section className="about-section">

        <div className="why-ai-container">

          <div className="why-ai-left">

            <div className="about-chip">
              AI INTELLIGENCE LAYER
            </div>

            <h2>
              Why artificial intelligence matters
            </h2>

            <p>
              Modern cloud environments generate massive amounts of
              operational data every second.
            </p>

            <p>
              AI helps detect hidden patterns,
              identify cost anomalies faster,
              and automate optimization workflows
              that would otherwise require manual investigation.
            </p>

          </div>

          <div className="why-ai-right">

            <div className="ai-feature">
              Real-time anomaly detection
            </div>

            <div className="ai-feature">
              Intelligent cost optimization
            </div>

            <div className="ai-feature">
              Predictive infrastructure monitoring
            </div>

            <div className="ai-feature">
              Automated insight generation
            </div>

          </div>

        </div>

      </section>

    </div>

  );
}