# SemanticLayerBuilder — Project Definition

## 1. Purpose

SemanticLayerBuilder is a system for automatically generating a *semantic layer*
(dimensions + metrics) for arbitrary client datasets using:

- sample data inspection (XML or SQL)
- schema inference
- LLM-native reasoning
- standardized YAML config files
- a **generic** contract for an MCP server

The goal is to let consultants onboard new clients quickly, with minimal
hand-crafted semantic modeling, while still producing **clean, explainable**
metrics and dimensions that can be used by downstream tools and chatbots.

---

## 2. Core Components

### 2.1 Frontend UI (single-screen web app)

- User selects a data source (XML file or SQL database)
- Controls sampling (first N rows or random sample)
- Provides config hints (e.g., columns to exclude)
- Shows run status & logs
- Shows discovered dimensions and metrics live
- Provides a “Generate YAML” button once refinement is complete

### 2.2 FastAPI Backend (Orchestrator)

- Routes:
  - `GET /` → serves the one-screen UI
  - `POST /run_scan` → triggers a semantic scan
- Validates and normalizes UI inputs
- Connects to XML/SQL sources to produce:
  - structured schema
  - sample rows
- Calls the **Builder Agent** with a well-defined payload
- Returns logs + semantic objects (dimensions + metrics) to the UI

### 2.3 Builder Agent (LLM-native Worker)

- Analyzes schema + sample data provided by the backend
- Infers candidate **dimensions** and **metrics**
- Maps them into the **generic semantic contract**
- Emits:
  - `dimensions.yaml`
  - `metrics.yaml`
- Produces logs and modeling notes for the UI
- Runs strictly at **design time**, never in the runtime query path

### 2.4 MCP Server (Semantic Layer Runtime)

- Loads `dimensions.yaml` + `metrics.yaml`
- Validates them against the generic contract
- Exposes a **stable, generic tool surface** to downstream agents:
  - list dimensions
  - list metrics
  - get metric definition
  - run metric queries
  - explain metrics
- Provides the interface downstream agents/chatbots call using the same API for all clients

---

## 3. Design Goals

- **Multi-client support**  
  Each client has its own semantic definitions but all conform to the same contract.

- **LLM-native**  
  Simple, predictable YAML shapes that LLMs can reliably generate and consume.

- **Strict validation**  
  MCP server enforces schema correctness to guarantee agent reliability.

- **Small contract**  
  Minimizes LLM tokens needed for Builder Agent, MCP server, and downstream querying agents.

- **Scalable onboarding**  
  Consultants can onboard new clients with minimal friction and reproducible results.

---

## 4. Generic Semantic Contract (Optimized, Strict, Stable)

This contract defines the **universal shapes** for dimensions, metrics, and MCP tool behavior.  
All clients must conform.  
The Builder Agent must generate YAML that validates against it.  
The MCP Server must enforce it strictly.

The contract intentionally stays **small and rigid** so:

- LLM agents can learn it easily  
- It is cheap to include in prompts  
- It generalizes across industries  
- It remains stable across clients  
- Validation is simple and deterministic

---

### 4.1 Allowed Dimension Types

A dimension MUST have one of:

- `categorical`
- `time`
- `numeric`
- `boolean`

No other types are permitted.

---

### 4.2 Dimension YAML Shape

```yaml
- name: string (snake_case)
  label: string (Title Case)
  description: string (optional)

  type: one of [categorical, time, numeric, boolean]

  source:
    kind: "sql" | "xml"
    entity: string     # table or logical XML group
    field: string      # column name or XML field/path

  nullable: boolean
  pii: boolean
  tags: [string, ...] (optional)