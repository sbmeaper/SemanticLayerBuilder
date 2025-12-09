# Builder Agent — Contract & Behavior (Optimized Spec)

This file defines the **contract** for the Builder Agent.  
It must stay aligned with `project_definition.md` and **not** describe GUI actions  
(those are in `builder_agent_runbook.md`).

---

## 1. Purpose

The Builder Agent converts **raw schema + sample data** from a client data source  
(XML or SQL) into a validated, standardized **semantic layer**:

- `dimensions.yaml`
- `metrics.yaml`

These outputs must strictly conform to the **generic semantic contract** used by the MCP server.

The Builder Agent runs at **design time**, not in the query path.

---

## 2. Position in the System

As defined in `project_definition.md`, the system has:

1. Web UI (select source → refine → generate)
2. FastAPI backend (validates input + calls the agent)
3. **Builder Agent (this spec)**
4. MCP Semantic Server (runtime)

The Builder Agent receives normalized input from the backend and emits  
YAML that the MCP server can load without modification.

---

## 3. Inputs

The Builder Agent receives a JSON payload from the backend containing:

### 3.1 Source Description
- `type`: `"xml"` or `"sql"`
- Connection or file details (already validated)
- Table/entity name(s) if SQL

### 3.2 Schema
A structured list of fields:
- `name`
- `type` (string, integer, float, date, datetime, boolean)
- `nullable` (boolean)
- Any backend-detected PII (boolean flag)

### 3.3 Sample Data
A small set of rows per table/entity.  
Used only for:
- type refinement  
- categorical detection  
- spotting metrics vs identifiers

### 3.4 User Hints
From the GUI:
- columns to exclude  
- required PII handling (exclude or mask)

The Builder Agent **never** connects to data sources itself.

---

## 4. Outputs

The agent returns:

1. `dimensions.yaml`  
2. `metrics.yaml`  
3. `validation_status` (pass/fail)  
4. `errors` (if validation fails)  
5. `notes` (modeling choices, ignored fields, ambiguity flags)

The backend writes the YAML files to disk and sends logs back to the UI.

---

## 5. Responsibilities (Strict Contract)

For each run, the Builder Agent must do the following **in order**:

### 5.1 Analyze Schema & Samples
- Validate types.
- Refine types where samples contradict schema.
- Identify PII with high confidence.
- Drop any excluded fields.

### 5.2 Generate Dimensions
For each eligible field:
- Create a dimension with:
  - `name`
  - `label`
  - `type` (categorical | time | numeric | boolean)
  - `source` mapping (table/entity + field or XML path)
  - `nullable`
  - `pii`
  - `tags` (optional)
- Ensure names follow:
  - snake_case for internal names  
  - Title Case for labels

### 5.3 Generate Metrics
Based on:
- numeric fields  
- counts on fact-like tables  
- common patterns (sum, avg, min, max)

Each metric must include:
- `name`
- `label`
- `aggregation`
- `expression` (or base field)
- `nullable`
- `tags` (optional)

### 5.4 Apply Generic Contract Rules
- Only allowed dimension types
- Only allowed metric aggregations
- All required keys must be present
- No PII unless explicitly allowed
- No raw SQL in expressions
- No client-specific tool names or shapes
- No references to columns that were excluded

### 5.5 Emit YAML (Deterministic)
- Stable ordering:
  - dimensions alphabetical
  - metrics alphabetical
- Consistent indentation + quoting
- No extra whitespace
- No missing keys

### 5.6 Validate
Run schema validation against the generic MCP contract.  
Return actionable errors if invalid.

---

## 6. Error Behavior

On any violation:
- Stop YAML generation  
- Return:
  - `validation_status: fail`
  - A list of errors
  - Specific fields / lines that are invalid

The agent must **never** emit partially valid YAML.

---

## 7. Notes for Future Prompting

When we later create the actual runtime system prompt:

- It will be distilled from this file.
- It will include:
  - Allowed dimension types
  - Allowed metric types
  - YAML shape expectations
- It should be ≤ 500–1000 tokens to keep runtime costs low.

---

## 8. Non-Goals

- No SQL execution  
- No large dataset scanning  
- No warehouse or ETL work  
- No free-form LLM guessing outside schema + samples  
- No client-specific MCP surface (must remain generic)

---

## 9. Versioning

Any change to:
- allowed types  
- YAML structure  
- naming conventions  
- required keys  

**must** be mirrored in the MCP server’s schema and reflected in `project_definition.md`.