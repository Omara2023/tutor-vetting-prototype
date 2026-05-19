# Agentic Profile Screener & Interview Architect

A lightweight, high-velocity python prototype built to automate unstructured applicant vetting and dynamically generate tailored interview frameworks. Designed and executed as a time-boxed 3-hour rapid engineering sprint, the system bridges the gap between raw business requirements and structured LLM execution.

## System Architecture

The core engineering objective was to generate sample applicant data  and transform it into actionable scoring metrics based on fluid administrator constraints, entirely bypassing brittle heuristic parsing.

1. **Value Mapping & Ideation (Hour 1):** Scoped business value mechanics. Developed a dual-engine protocol: an automated metric classification loop and a context-aware interview question generator that isolates resume inconsistencies or technical gaps.
2. **Technical Implementation (Hours 2-3):** Built the end-to-end Python harness executing API calls via OpenRouter to execute business logic.

## Technical Stack

- **Language:** Python 3.11+
- **Orchestration / LLM Interface:** OpenRouter API 
- **Environment Management:** Python-Dotenv

## Key Features

- **Dynamic Evaluation Matrices:** Allows administrative clerks to input arbitrary strings of criteria and scoring rules. The orchestration layer injects these constraints into the model prompt context.
- **Automated Resume Profiling:** Standardises profile information into a standardised scoring system.
- **Targeted Interview Generation:** Evaluates candidate credentials, flags explicit logical gaps or missing operational milestones, and engineers interview question suggestions.

## Roadmap & Upcoming Extensions

- [ ] **PDF Ingestion Layer:** Integrate a robust text extraction pipeline (using `pypdf`/`pdfplumber`) to ingest raw binary resume files directly.
- [ ] **Persistence Layer Refactor:** Migrate from .sqplite backend to a local Postgres/pgvector.
- [ ] **Graph Mapping:** Integrate a lightweight graph structure to visualise candidate relational competencies across team structures.