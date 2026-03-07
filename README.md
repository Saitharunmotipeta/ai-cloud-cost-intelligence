# AI Cloud Cost Intelligence Engine

Event-driven, serverless-ready AI Cloud Cost Intelligence platform designed to detect cloud cost anomalies and generate intelligent optimization insights using machine learning and LLM reasoning.

Built with:

* FastAPI (microservices architecture)
* Redis Streams (local messaging)
* AWS SQS (cloud phase)
* PostgreSQL
* scikit-learn (anomaly detection)
* LangChain + LangGraph (AI reasoning)
* Docker (local orchestration)
* Serverless-ready design (Lambda-compatible)

---

## Architecture Overview

This system follows a strict event-driven microservices architecture.

Core domain event flow:

cost_data_ingested_v1
↓
cost_data_ready_for_analysis_v1
↓
cost_anomaly_detected_v1
↓
cost_insight_generated_v1

All services communicate exclusively through events.
No service-to-service REST calls are allowed.

Delivery model:

* At-least-once delivery
* Idempotent consumers
* Dead-letter ready
* 15-minute SLA window for AI insights

---

## Services

### ingestion-service

Receives or simulates cloud usage data and emits initial cost events.

### analytics-service

Processes normalized metrics and detects anomalies using ML models.

### intelligence-service (Phase 3)

Generates AI-powered explanations and optimization recommendations.

### notification-service (Phase 4)

Reacts to insight events and logs notification delivery.

### api-gateway (Phase 5)

Provides REST and GraphQL access for querying anomalies and insights.

---

## Repository Structure

services/
shared/
infrastructure/
scripts/

Shared contains:

* Event contracts
* Broker abstraction
* Database base configuration
* Observability utilities

Each service:

* Runs independently
* Has its own Dockerfile
* Is serverless-migration ready

---

## Phase 1 – Event Backbone

Current focus:

* Redis Streams broker
* Base event contract
* Ingestion publishes dummy event
* Analytics consumes and republishes
* Dockerized local environment

Goal: Validate event-driven spine before adding ML or LLM complexity.

---

## Design Principles

* Event-first architecture
* Strict service boundaries
* Broker abstraction for Redis → SQS migration
* No overengineering
* Production-style structured logging
* Cloud-native discipline
* Stateless service design

---

## Local Development

Requirements:

* Docker
* Docker Compose

Run:

docker-compose up --build

This will start:

* Redis
* ingestion-service
* analytics-service

You should observe event flow in service logs.

---

## Roadmap

Phase 1 – Event plumbing
Phase 2 – Database + anomaly detection
Phase 3 – LLM intelligence layer
Phase 4 – Notification service
Phase 5 – GraphQL gateway
Phase 6 – Cloud readiness (SQS, Lambda, Terraform)

---

## Delivery Guarantees

* At-least-once event delivery
* Idempotent event consumers
* Configurable SLA window (default 15 minutes)
* Dead-letter support in cloud phase

---

## Status

Under active development.
Phase 1: Event backbone implementation. (Completed)
Phase 2: AI orchestration layer for reasoning.

---
