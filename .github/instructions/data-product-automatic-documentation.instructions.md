---
name: Data Product Automatic Documentation
description: "Generate standardized data product documentation markdown from pipeline and table YAML files. USE FOR: generate documentation.md, create data product documentation, refresh README documentation, extract published tables, extract schedule refresh, extract input tables, keep overview and outputs sections editable."
Department: Shared
Author: Vagenende Dimitri
version: 5080b0b3
---

# Automatic Data Product Documentation.

## Purpose

Generate a consistent English markdown documentation file for a data product with this exact section order:
1. Overview
2. Published Tables
3. Schedule Refresh
4. Input Tables
5. Outputs and Consumers
6. Semantic Model Relations (only when a root `pbi` folder with `config_semantic_model.yml` exists)

The generated markdown file must be near-complete while preserving semi-manual sections as editable tables.
Also generate a separate Confluence publication script from the embedded canonical implementation in this document.
The final objective is mandatory publication to Confluence, not only file generation.

## Use Cases

Use this instruction when the user asks to:
1. Create or update documentation.md 
2. Generate a README-style data product documentation file from YAML files.
3. Standardize documentation output across multiple repositories.
4. Auto-fill technical sections while keeping business fields manual.

Do not use this instruction for:
1. Generic architecture narratives with no structured source files.
2. Unstructured wiki content not tied to pipeline/table YAML.

## Required Repository Conventions

This skill assumes the repository follows standardized folders and files:
1. A data product specification YAML.
2. One or more pipeline files matching pipeline*.yml.
3. input_tables folders containing input table YAML files.
4. published_tables folders containing published table YAML files.

If some expected files are missing, continue generation with explicit Need to be fill manually markers.

## Output Contract

Generate one English markdown file named documentation.md unless the user explicitly asks for another filename.
Also generate one Confluence publication script at docs/generated_publish_to_confluence.py.

The output must:
1. Follow the 5-section order exactly, and add section 6 only when a root `pbi` folder with `config_semantic_model.yml` exists.
2. Use markdown headings and markdown tables.
3. Be deterministic and stable between runs.
4. Keep semi-manual sections editable.
5. Generate docs/generated_publish_to_confluence.py from the embedded canonical script in this file using the dynamic value provided by the user (Page ID only).
6. Include clear placeholders and setup instructions for Confluence publication.
7. Include a mandatory publication step to Confluence as final outcome.
8. Include a clear publication status block at the end:
   1. Published: YES or NO
   2. If NO, exact blocking reason and required user action
9. Use Need to be fill manually for any missing values or technical placeholders.
10. Translating the cron schedule logic to English for the Next Refresh field.

## Confluence Publication Script Contract

Generate docs/generated_publish_to_confluence.py with these rules:
1. Script must publish docs/documentation.md to Confluence.
2. Use the embedded canonical script from this document as the source implementation.
3. Generated script must be a strict byte-for-byte copy of the embedded canonical script (same classes, methods, imports, constants, and flow).
4. Only the configuration values in main may be user-specific when needed:
   1. PAGE_ID (ask user - found in the Confluence URL)
5. Keep AWS Parameter Store loading logic exactly as in the source script using boto3 and parameter name `/platform/pro/common/confluence_credentials` (no hardcoded API token).
6. Do not use Icarus.
7. Read both `username` and `api_token` from the same AWS Parameter Store parameter.
7. Inform the user clearly that they must provide:
   1. PAGE_ID
    2. Confluence credentials parameter configured in AWS Parameter Store at `/platform/pro/common/confluence_credentials`.
8. Keep only one prompt question to the user: the Confluence page number (PAGE_ID).
9. Do not ask the user for Confluence username or API token.
10. If PAGE_ID is missing, ask only for PAGE_ID and do not ask any additional confirmation question.
11. If the AWS Parameter Store key or required fields are missing, stop with a clear error.
12. If there is any ambiguity, copy the full script content directly from the embedded canonical script section into docs/generated_publish_to_confluence.py before publication.

## Canonical Confluence Script Implementation (Embedded)

Use this exact script content when generating docs/automatic_documentation_confluence.py:

```python
"""
Script to publish a Markdown file to Confluence
Supports authentication via AWS Parameter Store
"""
import boto3
import json
from pathlib import Path

import requests
from markdown import markdown


class ConfluencePublisher:
    def __init__(
        self, confluence_url: str, username: str, api_token: str, page_id: str
    ) -> None:
        """
        Initialize Confluence client

        Args:
            confluence_url: Base Confluence URL (e.g., https://your-domain.atlassian.net)
            username: Your Confluence email
            api_token: Confluence API token
            page_id: Existing Confluence page ID to update
        """
        self.confluence_url = confluence_url.rstrip("/")
        self.auth = (username, api_token)
        self.page_id = page_id
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def markdown_to_confluence_storage(self, md_content: str) -> str:
        """
        Convert Markdown to Confluence storage format (HTML)

        Args:
            md_content: Markdown content

        Returns:
            HTML formatted for Confluence
        """
        # Basic conversion - you can use more advanced libraries
        html_content = markdown(md_content, extensions=["tables", "fenced_code"])
        return html_content

    def update_page(self, content: str, title: str | None = None) -> dict:
        """
        Update an existing Confluence page

        Args:
            content: HTML content
            title: Optional page title override

        Returns:
            Confluence API response
        """
        return self._update_page(page_id=self.page_id, content=content, title=title)

    def _update_page(
        self, page_id: str, content: str, title: str | None = None
    ) -> dict:
        """Update an existing page"""
        # Get current version
        url = f"{self.confluence_url}/wiki/rest/api/content/{page_id}"
        response = requests.get(url, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        current_page = response.json()

        # Keep existing title when no new title is provided
        page_title = title or current_page.get("title")

        # Increment version
        new_version = current_page["version"]["number"] + 1

        # Update
        payload = {
            "version": {"number": new_version},
            "title": page_title,
            "type": "page",
            "body": {"storage": {"value": content, "representation": "storage"}},
        }

        response = requests.put(url, json=payload, auth=self.auth, headers=self.headers)
        response.raise_for_status()
        return response.json()


def main() -> None:
    """Main function"""

    # ===== CONFIGURATION =====
    # Option 1: From Parameter Store
    CONFLUENCE_URL = "https://luminus.atlassian.net"
    PAGE_ID = "{{PAGE_ID}}"
    PARAM_NAME = "/platform/pro/common/confluence_credentials"
    REGION_NAME = "eu-west-3"
    MD_FILE_PATH = "docs/documentation.md"  # Path to your MD file

    if not PAGE_ID:
        PAGE_ID = input("Confluence page number (PAGE_ID): ").strip()
    if not PAGE_ID:
        raise ValueError("PAGE_ID is required to update a Confluence page.")

    # Retrieve credentials from AWS Parameter Store
    ssm = boto3.client("ssm", region_name=REGION_NAME)
    try:
        response = ssm.get_parameter(Name=PARAM_NAME, WithDecryption=True)
    except Exception as exc:
        raise ValueError(
            "Unable to load AWS Parameter Store key '/platform/pro/common/confluence_credentials'."
        ) from exc

    credentials = json.loads(response["Parameter"]["Value"])
    username = credentials.get("username")
    api_token = credentials.get("api_token")
    if not username or not api_token:
        raise ValueError(
            "Missing 'username' or 'api_token' in AWS Parameter Store key '/platform/pro/common/confluence_credentials'."
        )

    # ===== EXECUTION =====
    try:
        # Read Markdown file
        md_content = Path(MD_FILE_PATH).read_text(encoding="utf-8")

        # Initialize publisher
        publisher = ConfluencePublisher(
            confluence_url=CONFLUENCE_URL,
            username=username,
            api_token=api_token,
            page_id=PAGE_ID,
        )

        # Convert Markdown to Confluence HTML
        html_content = publisher.markdown_to_confluence_storage(md_content)

        print(f"Updating existing page (ID: {PAGE_ID})...")
        result = publisher.update_page(content=html_content)
        print("✅ Page updated successfully!")

        # Display link
        result_page_id = result.get("id", PAGE_ID)
        page_url = (
            f"{CONFLUENCE_URL}/wiki/pages/viewpage.action?pageId={result_page_id}"
        )
        print(f"🔗 Page URL: {page_url}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()

```

## Mandatory Confluence Publication Workflow

After generating documentation and script, publication to Confluence is required:
1. Validate PAGE_ID is configured.
2. Validate AWS Parameter Store key `/platform/pro/common/confluence_credentials` exists and contains `username` and `api_token`.
3. If one prerequisite is missing:
    1. Display ACTION REQUIRED with explicit remediation steps.
    2. If PAGE_ID is missing, ask only one question: the Confluence page number.
    3. Re-run validation.
4. Execute publication script.
5. Report final Confluence page URL and publication timestamp.
6. If publication still fails, stop with explicit root-cause message and next required action.

## Canonical Structure

### 1. Overview (Semi-Manual)

Render a table with these properties:
1. Data Product Name
2. Data Product Type (Source Aligned or Consumer Aligned)
3. Domain
4. Data Product Owner
5. Data Engineer
6. Data Source
7. Status
8. Intake Documentation Link
9. Data Product Portal Link
10. Snowflake Schema
11. Code Repository
12. Next Refresh

Rules:
1. Auto-fill fields when data exists in sources.
2. Keep unknown business values as Need to be fill manually.
3. Include a Goal subsection with a concise paragraph.
4. For Data Product Type, use values from `data_product_pattern` in `.cruft.json` (e.g., "Source Aligned" or "Consumer Aligned").
5. Status can be only: in progress or done.
6. Data Product Owner must be `data_product_owner` from `.cruft.json`.
7. Data Engineer must be `developer_name` from `.cruft.json`.
8. Next Refresh must be the English translation of the cron schedule logic (e.g., "At 08:00 on day 1 of every month" for "0 8 1 * *").

### 2. Published Tables (Automatic)

For each discovered published table:
1. Create a numbered subsection.
2. Add the table description.
3. Render a columns table with:
   1. Column
   2. Data Type
   3. Description
   4. Quality Checks
4. Include table-level checks when available.

Rules:
1. Never use Need to be fill manually in the Quality Checks field.
2. If no quality checks are available, keep the Quality Checks cell empty.

Ordering rules:
1. Preserve pipeline declaration order if present.
2. Otherwise sort deterministically by table name.

### 3. Schedule Refresh (Automatic)

Extract scheduling metadata from pipeline files and render a property table with:
1. Schedule type
2. Trigger datasets
3. Max active runs
4. Max active tasks
5. Retries
6. Start date

If event-driven scheduling is detected, list trigger datasets explicitly.

### 4. Input Tables (Automatic)

Render one table with columns:
1. Input Table
2. Columns

Rules:
1. Populate from input table YAML files.
2. Keep deterministic ordering.
3. In Input Table, display the table name without the `.yml` extension.
4. In Columns, use compact comma-separated column names (e.g., `col1, col2`).

### 5. Outputs and Consumers (Semi-Manual)

Render an editable table with:
1. Output
2. Type
3. Link
4. Description

Rules:
1. Output can only be: Excel, Power BI, or SAP automation.
2. The Link column is mandatory and must be left as Need to be fill manually for user completion.
3. If unknown, use placeholders or Need to be fill manually for fields other than Output.

### 6. Semantic Model Relations (Conditional Automatic)

Only when the repository root contains a `pbi` folder and a `pbi/config_semantic_model.yml` file:
1. Parse semantic model tables from `pbi/config_semantic_model.yml`.
2. Parse relationships between those tables from the same file.
3. Generate a Mermaid graph that visualizes table relationships.
4. Include the Mermaid graph in section 6.

## Discovery and Extraction Rules

1. Recursively discover pipeline files using pipeline*.yml.
2. For each pipeline, read input and published table references.
3. Resolve referenced table YAML files relative to the pipeline folder.
4. Parse each table YAML for:
   1. Dataset or table name
   2. Description
   3. Columns
   4. Checks
5. Convert quality checks to readable labels when possible:
   1. missing -> No missing values
   2. duplicate -> No duplicate values
   3. invalid reference -> warn with referenced table/column when available

## Formatting Rules

1. English language only.
2. Clear, concise markdown.
3. Stable output for minimal diffs across runs.
4. No removal of semi-manual sections.
5. Explicit Need to be filled manully for missing values instead of silent omission.
6. Include generation date at the top of the file.

## Error Handling Rules

1. Never fail silently.
2. Continue partial generation when possible.
3. Mark missing files, invalid YAML, or unresolved references explicitly in output.

## Quality Checklist Before Finalizing

1. Section order is exactly 1 to 5 as defined, plus section 6 only when a root `pbi` folder with `config_semantic_model.yml` exists.
2. Overview and Outputs and Consumers remain editable.
3. Published Tables, Schedule Refresh, and Input Tables are auto-populated.
4. Markdown tables render correctly.
5. Output remains readable on Git platforms and Jira attachments.

## Jira Publication Handoff (Optional)

When requested by the user, provide publication-ready output for Jira API workflows:
1. Attach generated markdown file to the target issue.
2. Add a comment with generation timestamp.
3. Keep publication logic separate from documentation generation logic.
