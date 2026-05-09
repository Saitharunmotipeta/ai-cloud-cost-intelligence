import React from 'react';

const principles = [
  {
    title: 'Event-Driven Architecture',
    icon: '⚡',
    description:
      'All services communicate asynchronously through events for loose coupling and scalability.',
  },
  {
    title: 'Microservices',
    icon: '🧩',
    description:
      'Each service has a single responsibility and can be deployed independently.',
  },
  {
    title: 'AI Intelligence Layer',
    icon: '🧠',
    description:
      'LangChain, LangGraph, and RAG generate context-aware optimization insights.',
  },
  {
    title: 'Cloud-Native Design',
    icon: '☁️',
    description:
      'Built for containers, serverless computing, and production-grade AWS deployment.',
  },
];

const services = [
  {
    name: 'Ingestion Service',
    description: 'Collects and normalizes cloud cost and usage data.',
  },
  {
    name: 'Analytics Service',
    description: 'Detects anomalies using machine learning models.',
  },
  {
    name: 'Storage Service',
    description: 'Stores anomalies, insights, and aggregated metrics.',
  },
  {
    name: 'GraphQL Gateway',
    description: 'Unified API endpoint for the React dashboard.',
  },
  {
    name: 'Intelligence Service',
    description:
      'Uses LangChain, LangGraph, and RAG to generate recommendations.',
  },
];

const aiStack = [
  'LangChain',
  'LangGraph',
  'RAG',
  'Prompt Engineering',
  'Historical Retrieval',
  'Optimization Recommendations',
];

const cloudServices = [
  'CloudFront',
  'S3',
  'API Gateway',
  'EC2',
  'ECR',
  'Lambda',
  'SQS',
  'IAM',
  'CloudWatch',
  'Supabase / PostgreSQL',
];

const phases = [
  'Phase 1 – Event Backbone',
  'Phase 2 – Anomaly Detection',
  'Phase 3 – AI Intelligence Layer',
  'Phase 4 – Storage & GraphQL',
  'Phase 5 – Frontend Dashboard',
  'Phase 6 – AWS Deployment',
  'Phase 7 – Production Polish',
];

export default function AboutProject() {
  return (
    <div className="page-container">
      <section className="about-hero">
        <p className="about-badge">Architecture Showcase</p>
        <h1 className="about-title">AI Cloud Cost Intelligence Engine</h1>
        <p className="about-subtitle">
          An end-to-end event-driven platform that detects cloud cost anomalies
          and generates AI-powered optimization insights using machine learning,
          LangChain, LangGraph, and RAG.
        </p>
      </section>

      <section className="about-section">
        <h2 className="section-title">Architecture Principles</h2>
        <div className="card-grid four-columns">
          {principles.map((item) => (
            <div key={item.title} className="about-card">
              <div className="about-card-icon">{item.icon}</div>
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h2 className="section-title">Event Pipeline</h2>
        <div className="pipeline-flow">
          <span>Cost Data Ingested</span>
          <span>→</span>
          <span>Ready for Analysis</span>
          <span>→</span>
          <span>Anomaly Detected</span>
          <span>→</span>
          <span>Insight Generated</span>
        </div>
      </section>

      <section className="about-section">
        <h2 className="section-title">Microservices</h2>
        <div className="card-grid three-columns">
          {services.map((service) => (
            <div key={service.name} className="about-card">
              <h3>{service.name}</h3>
              <p>{service.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h2 className="section-title">AI Intelligence Layer</h2>
        <div className="about-highlight">
          <p>
            The intelligence engine combines retrieval and reasoning to explain
            anomalies and generate optimization recommendations.
          </p>
          <div className="tag-container">
            {aiStack.map((item) => (
              <span key={item} className="tech-tag">
                {item}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2 className="section-title">AWS Deployment Services</h2>
        <div className="tag-container">
          {cloudServices.map((service) => (
            <span key={service} className="tech-tag aws-tag">
              {service}
            </span>
          ))}
        </div>
      </section>

      <section className="about-section">
        <h2 className="section-title">Project Evolution</h2>
        <div className="roadmap-list">
          {phases.map((phase) => (
            <div key={phase} className="roadmap-item">
              {phase}
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}