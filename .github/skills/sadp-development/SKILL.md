---
name: source_aligned_data_product_building_with_vulcan
description: "This skill helps in creating custom ingestions aligned with data sources using the Vulcan framework at Luminus. It covers the entire development process, from initial setup to deployment in Airflow/Conveyor, including API management, data transformation, and publication to Snowflake."
Department: Shared
Author: Vagenende Dimitri
version: e5d8ec5e
---

## Description

This skill helps in creating custom ingestions aligned with data sources using the **Vulcan** framework at **Luminus**. It covers the entire development process, from initial setup to deployment in **Airflow/Conveyor**, including API management, data transformation, and publication to **Snowflake**.

The skill is designed to standardize the creation of custom ingestions while allowing the necessary flexibility to adapt to different data sources (REST APIs, databases, files, etc.). It follows **DNA** best practices and ensures consistency with existing processes at **Luminus**.

## Architecture Pattern

```text
src/
├── app/
│   └── {source}_runner_ingestion.py    # Entry point / CLI
└── {source}_ingestion/
    ├── __init__.py
    ├── schemas.py                      # Schema definitions
    ├── client/
    │   └── {source}_client.py           # API client
    └── jobs/
        └── {source}_ingestion_job.py    # Orchestration logic

dags/
├── common.py                           # Custom operators
├── data_product_dags.py                # Pipeline definitions
└── data_products/
    ├── data_products_specification.yml
    └── pipelines/
        └── {pipeline_name}/
            ├── pipeline_{name}.yml
            ├── input_tables/
            │   └── {table}.yml
            └── published_tables/
                └── {table}.yml
```

## Setup & Configuration

### 1. Repository Initialization

- Use **DNA team template**.
- Follow: *How to initialize a gitlab repository?*

### 2. Dependencies Installation

Add to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
neo-icarus = {source = "luminus", version = "2.0.0"}
retail-bee = { source = "luminus",version = "^0.4.2",}
```

Install via CLI:

```bash
poetry lock
poetry install
```

### 3. Credentials Management

Store credentials in **AWS Parameter Store**:

- **Path format**: `.../api/{your_ingestion_name}`
- **Reference**: *How to use credentials in a safe way?*

## Client Layer

**Purpose**: Handle all API/HTTP interactions.

**File**: `src/{source}_ingestion/client/{source}_client.py`

### Key Responsibilities

- Credential loading from Parameter Store.
- Request construction with proper authentication.
- Retry logic and error handling.
- Response parsing and normalization.
- Return predictable Python structures.

### Standard Methods

```python
class YourIngestionClient:
    def __init__(self, env: str, debug: bool = False):
        """Initialize client with environment and debug mode"""
        
    def connect(self) -> None:
        """Establish connection and load credentials"""
        
    def _load_credentials_from_parameter_store(self) -> dict:
        """Load API credentials from AWS Parameter Store"""
        
    def load_data(self, **kwargs) -> pd.DataFrame:
        """Fetch data from API - customize per use case"""
```

### Authentication Patterns to Consider

- API key in header / body / URL param.
- OAuth with refresh tokens.
- mTLS certificates.
- Time-sensitive signatures (AWS Signature v4).
- Multiple auth methods for different endpoints.

### Testing Tip

```python
# Add debug parameter to print collected data
if self.debug:
    print(df.head())
```

## Job Layer

**Purpose**: Orchestration between client and platform utilities.

**File**: `src/{source}_ingestion/jobs/{source}_ingestion_job.py`

### Key Responsibilities

- Call client methods to fetch raw records.
- Iterate through configured argument combinations.
- Apply schema casting/typing rules.
- Add technical columns (run metadata, timestamps, IDs).
- Return clean pandas DataFrames ready for ingestion.

### Vulcan Integration

```python
from vulcan.jobs import VulcanIngestionJob
from vulcan.arguments import VulcanBaseArguments

class YourIngestionJob(VulcanIngestionJob):
    # Implementation...
```

    def __init__(
        self,
        vulcan_args: VulcanBaseArguments,
        # Add your custom parameters
    ):
        super().__init__(vulcan_args)
        
    def custom_ingest(self) -> int:
        """
        Main ingestion logic - called by Vulcan framework
        Returns: number of records ingested
        """
        # 1. Fetch data using client
        # 2. Apply transformations
        # 3. Write to S3 as parquet
        # 4. Return record count

### Standard Methods (Keep As-Is)

- `aws` - AWS session management.
- `_app_updated_at` - Timestamp generation.
- `log_ingestion_context` - Logging metadata.

### Debugging

```python
# Use logging instead of print (Conveyor doesn't show print)
logger.info(f"Fetched {len(df)} records")
logger.info(f"Schema: {df.dtypes}")
```

## Schema Definition

**Purpose**: Define and validate data structures.

**File**: `src/{source}_ingestion/schemas.py`

### Example

```python
import pyarrow as pa

def _get_your_table_schema() -> pa.Schema:
    """Schema for your_table loaded from API"""
    return pa.schema([
        pa.field("id", pa.string(), nullable=False),
        pa.field("name", pa.string(), nullable=False),
        pa.field("value", pa.float64(), nullable=True),
        pa.field("category", pa.string(), nullable=True),
        pa.field("updated_at", pa.timestamp("us", tz="UTC"), nullable=False),
    ])
```

### Best Practices

- Define one function per table.
- Use PyArrow types for consistency.
- Mark primary keys as `nullable=False`.
- Always include `updated_at` timestamp field.

## Runner Layer

**Purpose**: Execution entrypoint and argument parsing.

**File**: `src/app/{source}_runner_ingestion.py`

### Key Responsibilities

- Initialize runtime context (project, environment, AWS config).
- Parse CLI/runtime arguments.
- Instantiate and execute job.
- Handle errors and logging.
- Propagate failures with clear messages.

### Structure

```python
def main():
    # 1. Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", required=True)
    parser.add_argument("--date", required=True)
```
    # Add custom arguments
    
    args = parser.parse_args()
    
    # 2. Initialize Vulcan context
    vulcan_args = VulcanBaseArguments(...)
    
    # 3. Create and run job
    job = YourIngestionJob(vulcan_args, ...)
    result = job.run()
    
    # 4. Log results
    logger.info(f"Ingestion completed: {result} records")

if __name__ == "__main__":
    main()
Tips
Keep runner logic minimal
Validate required arguments early
Log effective parameters used
Fail fast with explicit error messages
One runner per API/source
Airflow/DAG Layer
Purpose: Orchestration and scheduling

Structure
dags/
├── common.py                    # Custom operators
├── data_product_dags.py         # Pipeline definitions
└── data_products/
    ├── data_products_specification.yml
    └── pipelines/{pipeline_name}/
Custom Operator
File: dags/common.py

from vulcan.operators import VulcanBaseOperator

class YourCustomIngestionOperator(VulcanBaseOperator):
    path_to_executable: str = "src.app.{source}_runner_ingestion"
    task_id: str = "{source}_ingestion_task"
    use_vulcan_image: bool = False
    operator_settings: Optional[Dict[str, Any]] = None
    
    def __init__(
        self,
        data_product_specification: "DataProductsSpecification",
        pipeline_specification: "PipelineSpecification",
        input_table_config: Optional["InputTableConfig"] = None,
        published_table_configs: Optional[List["PublishedTableConfig"]] = None,
        **kwargs
    ):
        super().__init__(...)
Pipeline Definition
File: dags/data_product_dags.py

def get_pipeline_specification() -> PipelineSpecification:
    """Load pipeline metadata from YAML"""
    
def construct_{table}_taskgroup(
    pipeline_specification: PipelineSpecification,
    data_product_specification: DataProductsSpecification,
) -> TaskGroup:
    """Build TaskGroup for specific table ingestion"""
    
# Generate DAGs
vulcan.dag_factory.data_product_dag_factory(
    environment=env,
    path_to_data_products="dags/data_products",
    default_tags={"team": "your_team"},
    custom_ingestion_taskgroup_constructors={
        "your_table": construct_your_table_taskgroup,
    }
)
YAML Configuration
Input Table (input_tables/{table}.yml)
Defines ingestion contract for raw/staging tables:

table_name: your_table
ingestion_technology: custom
processing_pattern: full  # or incremental
natural_keys:
  - id
updated_at_field: updated_at
source_system: your_source
custom_ingestion_options:
  s3_staging_path: s3://bucket/raw/{table}/

columns:
  - name: id
    type: STRING
    nullable: false
  - name: value
    type: FLOAT
    nullable: true
  - name: updated_at
    type: TIMESTAMP_NTZ
    nullable: false
Published Table (published_tables/{table}.yml)
Defines business-facing dataset contract:

dataset_name: your_published_table
description: "Business description of the dataset"
columns:
  - name: id
    type: STRING
    description: "Unique identifier"
  - name: value
    type: FLOAT
    description: "Metric value"
Pipeline (pipeline_{name}.yml)
Orchestration settings:

pipeline_name: your_pipeline
schedule: "0 6 * * *"  # Cron expression
retries: 3
concurrency: 1
input_tables:
  - your_table
published_tables:
  - your_published_table
Data Product (data_products_specification.yml)
Top-level metadata:

product_name: your_data_product
version: "1.0"
repository: "neo/your_team/your_repo"
snowflake_schema: your_schema
pipelines:
  - pipeline_{name}.yml
Data Flow
API → Client: Fetch raw data from source
Client → Job: Return normalized Python structures
Job → S3 Raw: Write parquet files to S3 bucket
S3 Raw → Snowflake (p schema): Vulcan loads to private schema
p schema → dbt → official schema: Transform and publish
API/Database
    ↓
Client (HTTP/Auth)
    ↓
Job (Transform + Metadata)
    ↓
S3 Raw (Parquet)
    ↓
Snowflake p schema
    ↓
dbt transformations
    ↓
Snowflake official schema
Testing Strategy
Local Testing
# Test client independently
client = YourClient(env="dev", debug=True)
client.connect()
df = client.load_data()
print(df.head())
S3 Upload Test
from bee import s3_upload

s3_upload(
    df=test_df,
    bucket="your-bucket",
    key="test/your_file.parquet"
)
Conveyor Testing
Deploy to dev environment
Use logger.info() extensively (print doesn't show)
Check Airflow logs for debugging
Verify S3 files are created
Check Snowflake p schema for data
Common Patterns
Full Refresh Pattern
def custom_ingest(self) -> int:
    # Fetch all data
    df = self.client.load_data()
    
    # Add metadata
    df["updated_at"] = self._app_updated_at
    
    # Write to S3
    self._write_to_s3(df, "your_table")
    
    return len(df)
Incremental Pattern
def custom_ingest(self) -> int:
    # Get last ingestion timestamp
    last_ts = self._get_last_timestamp()
    
    # Fetch only new/updated records
    df = self.client.load_data(since=last_ts)
    
    # Process and write
    df["updated_at"] = self._app_updated_at
    self._write_to_s3(df, "your_table")
    
    return len(df)
Paginated API Pattern
def load_data(self) -> pd.DataFrame:
    all_data = []
    page = 1
    
    while True:
        response = self._fetch_page(page)
        if not response["data"]:
            break
            
        all_data.extend(response["data"])
        page += 1
        
    return pd.DataFrame(all_data)
Checklist
Before Development
 Understand API authentication mechanism
 Test API calls manually
 Receive architect approval
 Define data model and schemas
 Determine full vs incremental refresh
Development
 Initialize repo from template
 Install dependencies (icarus, bee)
 Store credentials in Parameter Store
 Implement client with auth logic
 Implement job with Vulcan integration
 Define schemas in PyArrow
 Create runner with argument parsing
 Test locally where possible
Airflow/Orchestration
 Create custom operator
 Define pipeline TaskGroup constructor
 Write input_tables YAML
 Write published_tables YAML
 Write pipeline YAML
 Update data_products_specification YAML
 Register in dag_factory
Testing & Deployment
 Test S3 upload
 Deploy to dev Conveyor
 Check Airflow logs
 Verify S3 parquet files
 Verify Snowflake p schema
 Test dbt transformations
 Deploy to production
Useful Links
Example Implementation: Baringa Ingestion GitLab
DNA Documentation: Self-Service Data Ingestion Using Input Table YAMLs
Bee Package: DNA Retail AI Confluence
Icarus: GitLab Repository
Credentials Management: Finance General Documentation
Tips & Best Practices
✅ Do:

Read API documentation thoroughly before coding
Test API calls independently first
Use logging extensively in jobs (not print)
Keep runner logic minimal
Validate arguments early and fail fast
Add debug mode to client for testing
Define schemas explicitly with PyArrow
Follow naming convention for Parameter Store secrets
❌ Don't:

Hardcode credentials
Mix client and job responsibilities
Put heavy logic in runner
Use print statements (use logger in Conveyor)
Skip schema validation
Forget to add updated_at timestamp
Troubleshooting
Issue: Credentials not loading
Check Parameter Store path format: .../api/{ingestion_name}
Verify IAM permissions for Parameter Store access
Test credential loading in client independently
Issue: Data not appearing in Snowflake
Check S3 bucket for parquet files
Verify input_tables YAML configuration
Check Airflow task logs for errors
Confirm Vulcan metadata handling
Issue: Schema mismatch errors
Ensure PyArrow schema matches actual data
Check nullable constraints
Verify timestamp formats (UTC)
Compare with input_tables YAML definition
Issue: Conveyor logs not showing output
Replace print() with logger.info()
Check Airflow UI for task logs
Verify task is actually running (not skipped)