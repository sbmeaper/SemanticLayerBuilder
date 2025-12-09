# 🤖 SemanticLayerBuilder Agent Specification

## 1. Overview and Goal

| Key Attribute | Description |
| :--- | :--- |
| **Agent Name** | `SemanticLayerBuilder` |
| **Primary Goal** | Automatically ingest and analyze raw data (XML or SQL tables) to generate a structured **semantic layer** definition. |
| **Value Proposition** | Accelerate the creation of data-querying infrastructure by automating the definition of **metrics** and **dimensions**. |

---

## 2. Input and Output Specification

### ➡️ Input

| Input Type | Format/Source | Description |
| :--- | :--- | :--- |
| **Single Source** | XML File | A single XML document containing hierarchical data. |
| **Multiple Sources** | SQL Database Tables | A set of connected tables (e.g., provided via connection credentials or a schema definition). |
| **Configuration** | JSON/YAML (Optional) | User-defined hints, exclusion lists, or specific naming conventions to enforce. |

### ⬅️ Output

The agent must produce two well-formed YAML files that conform to the required schema for the downstream **MCP Server** query constructor.

| Output File | Purpose | Example Contents |
| :--- | :--- | :--- |
| `metrics.yaml` | Defines calculable numerical fields (e.g., counts, sums, averages). | `metrics: - name: total_sales - type: sum - expression: 'price * quantity'` |
| `dimensions.yaml` | Defines categorical or descriptive fields used for filtering and grouping. | `dimensions: - name: product_category - type: string - source: 'product_table.category_name'` |

---

## 3. Processing and Core Logic

### 3.1. Data Ingestion and Normalization
* **XML Handling:** Traverse the XML tree to identify nodes and attributes, flattening the hierarchy where appropriate to suggest initial **dimensions**.
* **Table Handling:** Analyze table schemas to identify **primary keys**, **foreign keys**, and column data types. Use relationships to infer join paths.

### 3.2. Semantic Inference (LLM Core)
* **Candidate Identification:** Based on data types, identify fields for **Metrics** (numerical/temporal) and **Dimensions** (string/date/boolean/ID).
* **Intelligent Naming/Grouping:** Use an LLM to apply **contextual awareness** to raw column names (e.g., `cust_id` $\rightarrow$ `Customer ID`).
* **Aggregation Suggestion:** Suggest common metrics (e.g., `count`, `sum`, `avg`) for numerical fields.

---

## 4. Quality, Security, and Operational Considerations

### 🔒 Security
* **Input Sanitization:** Validate all configuration inputs (paths, credentials) to prevent **injection attacks**.
* **PII/Sensitive Data:** Flag columns that appear to contain **Personally Identifiable Information (PII)** and allow the user to exclude or mask them.

### ⚖️ Scale and Performance
* **Chunking/Streaming:** For large data sources, implement **data streaming** or **sampling** instead of loading the entire dataset into memory.
* **Caching:** Cache schema analysis results to improve run time on subsequent operations.

### 📈 Reliability and Operationalization
* **Input Validation:** Thoroughly check the generated YAML files against the expected MCP Server **schema** *before* saving them to disk.
* **Audit Logging:** Log the input source, configuration, and success/failure status of every run.

---

## 5. Interaction Interface (GUI-Focused)

The agent should operate in a step-by-step manner to facilitate learning and validation.

* **Step 1: Input Selection:** Specify data source (XML file path or DB connection).
* **Step 2: Schema Review & PII Flagging:** Review inferred fields, confirm PII flags, and exclude raw fields.
* **Step 3: Semantic Layer Refinement:** Edit inferred **dimension names** and adjust **aggregation types** and underlying expressions for **metrics**.
* **Step 4: Output Generation:** Validate and save the `metrics.yaml` and `dimensions.yaml` files.