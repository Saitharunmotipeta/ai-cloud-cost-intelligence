import React, { useState } from "react";

import {
  ChevronDown,
  ChevronUp,
  BrainCircuit,
  Network,
  Sparkles,
  Cpu,
  BarChart3,
  Activity,
  Globe,
  ServerCog
} from "lucide-react";

import {
  SiDocker,
  SiRedis,
  SiGraphql,
  SiFastapi,
  SiPostgresql,
  SiPython
} from "react-icons/si";

import {
  TbBrandOpenai
} from "react-icons/tb";

/* =========================================================
   PRINCIPLES
========================================================= */

const principles = [
  {
    title: "Event-Driven Architecture",
    icon: "⚡",
    description:
      "Real-time asynchronous communication across distributed cloud services."
  },
  {
    title: "Microservices Design",
    icon: "🧩",
    description:
      "Independent deployable services built for scalability and resilience."
  },
  {
    title: "AI Intelligence Layer",
    icon: "🧠",
    description:
      "LangChain, LangGraph, and RAG pipelines generate optimization insights."
  },
  {
    title: "Cloud-Native Infrastructure",
    icon: "☁️",
    description:
      "AWS-native deployment optimized for distributed event workflows."
  }
];

/* =========================================================
   SERVICES
========================================================= */

const services = [
  {
    name: "Ingestion Service",
    icon: <Cpu size={28} />,
    className: "aws-service",
    description:
      "Collects cloud billing, usage, and infrastructure telemetry."
  },
  {
    name: "Analytics Engine",
    icon: <SiPython size={28} />,
    className: "python-service",
    description:
      "Processes anomalies and executes intelligence workflows."
  },
  {
    name: "Storage Service",
    icon: <SiPostgresql size={28} />,
    className: "postgres-service",
    description:
      "Stores insights, anomalies, metrics, and historical datasets."
  },
  {
    name: "GraphQL Gateway",
    icon: <SiGraphql size={28} />,
    className: "graphql-service",
    description:
      "Unified API aggregation layer powering the frontend dashboard."
  },
  {
    name: "AI Intelligence Layer",
    icon: <TbBrandOpenai size={28} />,
    className: "ai-service",
    description:
      "Generates AI-driven optimization recommendations and root-cause analysis."
  },
  {
    name: "Container Platform",
    icon: <SiDocker size={28} />,
    className: "docker-service",
    description:
      "Containerized services deployed independently across environments."
  }
];

/* =========================================================
   AI STACK
========================================================= */

const aiStack = [
  {
    name: "LangChain",
    icon: <BrainCircuit size={18} />
  },
  {
    name: "LangGraph",
    icon: <Network size={18} />
  },
  {
    name: "RAG Pipelines",
    icon: <Sparkles size={18} />
  },
  {
    name: "Prompt Engineering",
    icon: <Cpu size={18} />
  },
  {
    name: "Optimization Intelligence",
    icon: <BarChart3 size={18} />
  }
];

/* =========================================================
   AWS STACK
========================================================= */

const cloudServices = [
  {
    name: "Lambda",
    icon: <Cpu size={18} />
  },
  {
    name: "SQS",
    icon: <Network size={18} />
  },
  {
    name: "CloudWatch",
    icon: <Activity size={18} />
  },
  {
    name: "EC2",
    icon: <ServerCog size={18} />
  },
  {
    name: "API Gateway",
    icon: <Globe size={18} />
  },
  {
    name: "Docker",
    icon: <SiDocker size={18} />
  },
  {
    name: "Redis",
    icon: <SiRedis size={18} />
  },
  {
    name: "PostgreSQL",
    icon: <SiPostgresql size={18} />
  },
  {
    name: "FastAPI",
    icon: <SiFastapi size={18} />
  },
  {
    name: "GraphQL",
    icon: <SiGraphql size={18} />
  }
];

/* =========================================================
   PHASES
========================================================= */

const phases = [
  {
    title: "Phase 1 — Event Backbone",
    content:
      "Built broker abstraction supporting Redis Streams and AWS SQS for asynchronous event-driven communication."
  },
  {
    title: "Phase 2 — Anomaly Detection",
    content:
      "Developed analytics workflows capable of detecting cloud cost spikes and infrastructure anomalies."
  },
  {
    title: "Phase 3 — AI Intelligence Layer",
    content:
      "Integrated LangChain, LangGraph, and RAG workflows for intelligent optimization recommendations."
  },
  {
    title: "Phase 4 — GraphQL Aggregation",
    content:
      "Unified microservices through a centralized GraphQL gateway architecture."
  },
  {
    title: "Phase 5 — Interactive Dashboard",
    content:
      "Designed enterprise-grade monitoring dashboards with live AI insights and anomaly workflows."
  },
  {
    title: "Phase 6 — AWS Deployment",
    content:
      "Containerized infrastructure deployed on AWS cloud-native architecture."
  }
];

/* =========================================================
   COMPONENT
========================================================= */

export default function Architecture() {

  const [openIndex, setOpenIndex] =
    useState(null);

  return (

    <div className="architecture-page">

      {/* HERO */}

      <section className="architecture-hero">

        <div className="hero-glow"></div>

        <div className="hero-content">


          <p className="about-badge">
            LIVE CLOUD ARCHITECTURE
          </p>

          <h1 className="about-title">
            AI Cloud Cost Intelligence Engine
          </h1>

          <p className="about-subtitle">
            Distributed event-driven intelligence platform
            powered by anomaly detection, AI workflows,
            GraphQL aggregation, and AWS-native infrastructure.
          </p>

          

        </div>

      </section>

      {/* PRINCIPLES */}

      <section className="about-section">

        <h2 className="section-title">
          Architecture Principles
        </h2>

        <div className="card-grid four-columns">

          {principles.map((item) => (

            <div
              key={item.title}
              className="about-card neon-card"
            >

              <div className="about-card-icon">
                {item.icon}
              </div>

              <h3>{item.title}</h3>

              <p>{item.description}</p>

            </div>

          ))}

        </div>

      </section>

      {/* EVENT PIPELINE */}

      <section className="about-section">

        <h2 className="section-title">
          Live Event Pipeline
        </h2>

        <div className="pipeline-container">

          <div className="pipeline-node">
            Cost Data Ingested
          </div>

          <div className="pipeline-line"></div>

          <div className="pipeline-node">
            Ready For Analysis
          </div>

          <div className="pipeline-line"></div>

          <div className="pipeline-node">
            Anomaly Detected
          </div>

          <div className="pipeline-line"></div>

          <div className="pipeline-node">
            Insight Generated
          </div>

        </div>

      </section>

      {/* SERVICES */}

      <section className="about-section">

        <h2 className="section-title">
          Distributed Microservices
        </h2>

        <div className="card-grid three-columns">

          {services.map((service) => (

            <div
              key={service.name}
              className="about-card service-card"
            >

              <div
                className={`service-icon ${service.className}`}
              >
                {service.icon}
              </div>

              <h3>{service.name}</h3>

              <p>{service.description}</p>

            </div>

          ))}

        </div>

      </section>

      {/* AI STACK */}

      <section className="about-section">

        <h2 className="section-title">
          AI Intelligence Stack
        </h2>

        <div className="tag-container">

          {aiStack.map((item) => (

            <div
              key={item.name}
              className="logo-tag"
            >

              {item.icon}

              <span>{item.name}</span>

            </div>

          ))}

        </div>

      </section>

      {/* AWS STACK */}

      <section className="about-section">

        <h2 className="section-title">
          AWS Infrastructure Stack
        </h2>

        <div className="tag-container">

          {cloudServices.map((service) => (

            <div
              key={service.name}
              className="logo-tag aws-logo-tag"
            >

              {service.icon}

              <span>{service.name}</span>

            </div>

          ))}

        </div>

      </section>

      {/* ROADMAP */}

      <section className="about-section">

        <h2 className="section-title">
          Engineering Evolution
        </h2>

        <div className="accordion-container">

          {phases.map((phase, index) => (

            <div
              key={phase.title}
              className="accordion-item"
            >

              <button
                className="accordion-header"
                onClick={() =>
                  setOpenIndex(
                    openIndex === index
                      ? null
                      : index
                  )
                }
              >

                <span>{phase.title}</span>

                {openIndex === index
                  ? <ChevronUp size={18} />
                  : <ChevronDown size={18} />
                }

              </button>

              {openIndex === index && (

                <div className="accordion-content">

                  {phase.content}

                </div>

              )}

            </div>

          ))}

        </div>

      </section>

    </div>

  );

}