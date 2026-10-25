# 🤝 Consumer-Driven Contract Testing (Pact & TypeScript) — 7-Day Sprint

Welcome to the official reference codebase for the **Consumer-Driven Contract Testing** course track on [letustransform.com](https://www.letustransform.com) ([All QE Roadmaps](https://www.letustransform.com/roadmaps) · [QE Strategy Docs](https://www.letustransform.com/docs)).

This standalone repository contains verified `@pact-foundation/pact` V3 consumer tests, Express provider verification suites, provider state handlers, Docker Compose Pact Broker configurations, `can-i-deploy` CI quality gates, webhook templates, multi-consumer evolution scenarios, and GitHub Actions pipelines across all 7 days of the hands-on sprint.

---

## 🗺️ 7-Day Curriculum & Learning Matrix

| Day | Topic & Focus Area | Directory | Key Concepts & Tools | Interactive Playbook |
| :---: | :--- | :--- | :--- | :---: |
| **Day 1** | Consumer Pact Writing Basics | [`day-1-consumer-pact`](./day-1-consumer-pact/) | `@pact-foundation/pact` V3, `MatchersV3`, consumer interaction generation | [Day 1 Playbook](https://www.letustransform.com/episodes/contract-day-1) |
| **Day 2** | Provider Verification | [`day-2-provider-verification`](./day-2-provider-verification/) | Express Order Service provider, `Verifier`, `stateHandlers` | [Day 2 Playbook](https://www.letustransform.com/episodes/contract-day-2) |
| **Day 3** | Pact Broker Setup & Publish | [`day-3-broker-setup-publish`](./day-3-broker-setup-publish/) | Self-hosted Pact Broker (`docker-compose.yml`), contract publishing & versioning | [Day 3 Playbook](https://www.letustransform.com/episodes/contract-day-3) |
| **Day 4** | Can-I-Deploy Gate | [`day-4-can-i-deploy`](./day-4-can-i-deploy/) | `pact-broker can-i-deploy` CLI, matrix verification gating before release | [Day 4 Playbook](https://www.letustransform.com/episodes/contract-day-4) |
| **Day 5** | Webhooks & Provider State Teardown | [`day-5-webhooks-provider-states`](./day-5-webhooks-provider-states/) | Broker webhooks (`contract_content_changed`), isolated provider state setup/teardown | [Day 5 Playbook](https://www.letustransform.com/episodes/contract-day-5) |
| **Day 6** | Multi-Consumer Scenarios | [`day-6-multi-consumer`](./day-6-multi-consumer/) | Web, Mobile & Analytics consumers against one provider, additive schema evolution | [Day 6 Playbook](https://www.letustransform.com/episodes/contract-day-6) |
| **Day 7** | GitHub Actions CI Pipeline | [`day-7-github-actions-ci`](./day-7-github-actions-ci/) | End-to-end CI/CD contract pipeline: consumer test → publish → verify → `can-i-deploy` | [Day 7 Playbook](https://www.letustransform.com/episodes/contract-day-7) |

---

## 🧰 Prerequisites
- **Node.js**: `v18.0.0+`
- **Docker Desktop** (optional, for running the self-hosted Pact Broker in Days 3–5)
- **npm**

---

## 🚀 Quick Start

```bash
git clone https://github.com/letstrnsfrm-ai/contract-testing-roadmap.git
cd contract-testing-roadmap
npm install
npm test
```

To spin up the local Pact Broker + PostgreSQL stack:
```bash
docker-compose up -d
```

---

## 🔗 Explore More on Let's Transform QE Portal
- **[Hands-On QE Career Roadmaps](https://www.letustransform.com/roadmaps)**
- **[QE Strategy & Architecture Blueprints](https://www.letustransform.com/docs)**
- **[Executive Quality Engineering Hub](https://www.letustransform.com/lead-hub)**
