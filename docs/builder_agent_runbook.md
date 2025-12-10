# ⚙️ SemanticLayerBuilder Agent Run Instructions

## 1. Task Goal

The objective of this run is to create a complete and validated semantic layer definition (`metrics.yaml` and `dimensions.yaml`) for the provided data source.

## 2. Step-by-Step Execution Guide

This guide follows the **GUI-focused workflow** for interactive learning and validation.

### Step 1: Input Data Selection

* **Action:** Launch the SemanticLayerBuilder GUI.
* **Task:** Select the input data source.
    * **Data Type:** [**XML File** / **SQL Tables**] *(Select one)*
    * **Source Location:**
        * *If XML:* Enter the full path to the XML file (e.g., `/Users/dev/data/transactions_q3.xml`).
        * *If SQL:* Enter the connection credentials (e.g., hostname, database name, user/pass).
* **Configuration Hints (Optional):**
    * *If known:* List any specific columns to exclude (e.g., `audit_timestamp`, `raw_id`).

### Step 2: Schema Review and PII Validation

* **Action:** The agent analyzes the schema/structure and presents the inferred fields.
* **Task:** Review the list of fields displayed:
    1.  **Confirm Data Types:** Verify that the agent correctly identified field types (e.g., `string`, `integer`, `date`).
    2.  **Review PII Flags:** For any column flagged as PII (e.g., `email`, `address`):
        * **Action A (Secure):** Check the box to **EXCLUDE** the column from the final semantic layer.
        * **Action B (Mask/Use):** Review and confirm if masking/hashing is required before use.
    3.  **Finalize Field List:** Use the GUI to exclude any irrelevant raw columns.

### Step 3: Semantic Layer Refinement

This is the core learning step. Iterate through the **Dimensions** and **Metrics** tabs.

#### 3.1. Dimensions Tab

* **Goal:** Define user-friendly, business-focused names.
* **Task:** For each inferred dimension (e.g., `p_cat`):
    * **Edit Name:** Change the name to the desired business term (e.g., `Product Category`).
    * **Define Hierarchy:** If applicable, group related dimensions (e.g., `Year` $\rightarrow$ `Month` $\rightarrow$ `Day`).

#### 3.2. Metrics Tab

* **Goal:** Define the numerical calculations used for reporting.
* **Task:** For each inferred metric (e.g., a count on the fact table):
    * **Edit Name:** Change the name to a clear term (e.g., `Total Orders`, `Average Price`).
    * **Confirm/Adjust Aggregation:** Verify the suggested aggregation function (`SUM`, `AVG`, `COUNT`, etc.).
    * **Review Expression:** For complex metrics (e.g., calculated fields), review the generated expression (e.g., `sales_amount - discount_amount`).

### Step 4: Output Generation and Validation

* **Action:** Click the **"Generate YAML"** button.
* **Agent Process:**
    1.  The agent generates `metrics.yaml` and `dimensions.yaml` based on the refined definitions.
    2.  The agent performs a final validation against the MCP Server schema.
* **Task:**
    * If validation **SUCCEEDS**, review the output files in the specified directory.
    * If validation **FAILS**, address the specific error message provided by the agent and return to Step 3.