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

## 2. Core Components

1. **Frontend UI (single-screen web app)**
   - User chooses data source (XML file / SQL database)
   - Controls sampling (first N rows vs random sample)
   - Provides config hints (e.g., columns to exclude)
   - Shows run status & logs
   - Shows discovered dimensions (and later metrics) live

2. **FastAPI Backend (Orchestrator)**
   - Exposes:
     - `GET /` → serves the one-screen UI
     - `POST /run_scan` → triggers a semantic scan
   - Validates and normalizes UI inputs
   - Calls the **Builder Agent** with a well-defined payload
   - Returns logs + discovered semantic objects (dims/metrics) to the UI

3. **Builder Agent (LLM-native Worker)**
   - Inspects schema and sample rows from a data source
   - Infers candidate **dimensions** (and later **metrics**)
   - Maps findings into a **generic semantic contract** schema
   - Emits:
     - `dimensions.yaml`
     - `metrics.yaml`
   - Produces human-readable logs and suggestions for the UI

4. **MCP Server (Semantic Layer Runtime)**
   - Loads `dimensions.yaml` + `metrics.yaml`
   - Validates them against the generic contract
   - Exposes tools to:
     - list dimensions and metrics
     - run queries against the underlying data
   - Acts as a standard endpoint that chatbots / agents can call

## 3. Generic Semantic Contract (Shared Across Clients)

The MCP server uses a **generic config schema** that is the same for all
clients. The content of each file is client-specific, but the **shape** is
consistent.

### 3.1 Dimensions Schema (conceptual)

```yaml
version: 1
dimensions:
  - name: customer_city
    label: Customer City
    description: City of the customer’s primary address

    type: categorical            # categorical | time | numeric | boolean

    source:
      kind: sql                  # sql | xml | other
      entity: customers          # table name or logical entity
      field: city                # column or field name
      path: null                 # optional XPath / JSONPath for XML/JSON

    pii: false
    nullable: true
    tags: [ geo, customer ]ut Generation:** Validate and save the `metrics.yaml` and `dimensions.yaml` files.