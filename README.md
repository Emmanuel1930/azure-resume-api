### Crafting Your JSON Resume and Setting Up Azure Resources

### 1. **Craft Your JSON Resume:**

- Follow the schema provided by JSON Resume ([JSON Resume Schema](https://jsonresume.org/schema)) to structure your resume data in JSON format.
- Ensure your JSON resume includes essential sections like basics, work experience, education, skills, etc.

Example JSON Resume:

```json
jsonCopy code
{
  "basics": {
    "name": "John Doe",
    "label": "Software Developer",
    "email": "john.doe@example.com",
    "phone": "+1 (123) 456-7890",
    ...
  },
  "work": [
    {
      "company": "ABC Inc.",
      "position": "Senior Developer",
      "startDate": "2018-01-01",
      "endDate": "2022-06-30",
      ...
    },
    ...
  ],
  "education": [
    {
      "institution": "XYZ University",
      "area": "Computer Science",
      "studyType": "Bachelor",
      "startDate": "2014-09-01",
      "endDate": "2018-05-31",
      ...
    },
    ...
  ],
  ...
}

```


### Setting Up Azure Resources:
Resource Group Creation:

Access the Azure portal (https://azure.microsoft.com/en-us/get-started/azure-portal)

Search for "Resource groups" and click "create."

Provide details like name (e.g., ResumeAPIGroup) and region (e.g., Central South Africa North)

Confirm creation with "Review + Create" and then "Create."




### Creating Azure Cosmos DB Serverless API for Storing Data in Table Format

When setting up an Azure Cosmos DB serverless API to store data in a table format, it's crucial to understand the intricacies involved, including defining the partition key, managing the ID field, and handling metadata. Here's a comprehensive guide to navigate through these aspects effectively.

### Setting Up Azure Cosmos DB

1. **Creating an Azure Cosmos DB Account**:
    - Begin by creating a new Azure Cosmos DB account in the Azure portal.
    - Choose the appropriate API (such as SQL API but for this project it is NoSQL and Serverless) that supports storing data in JSON format.
2. **Understanding the Partition Key**: ( for this project the patition key is /lang i used thst intentionally because my resume supportted mutiple langueges)
    - The partition key in Cosmos DB determines how data is distributed across physical partitions.
    - Choose a property that has a high cardinality and is frequently used in queries to ensure optimal performance.
3. **Defining the ID Field**: ( for this project the id is Resume)
    - Each document in Cosmos DB must have a unique identifier (`id` field).
    - It's essential to manage the generation of this identifier to avoid conflicts and ensure uniqueness across your dataset.

### Storing Data in Table Format

1. **Creating a JSON Schema**:
    - Define a structured JSON schema that represents your data model, including nested objects and arrays as needed.
    - Example:
        
        ```json schema and also including the metafield for the cosmos table because without the metafield in the cosmos table the table will not be able to save
        jsonCopy code and the cosmos tablemetafield
        {
          "id": "unique_id_here",
          "partitionKey": "your_partition_key_value",
          "field1": "value1",
          "field2": ["array_value1", "array_value2"],
          "nestedObject": {
            "nestedField": "nested_value"
          }
        }
        
        ```
        
2. **Handling Metadata Fields**:
    - Cosmos DB automatically adds metadata fields (`_rid`, `_self`, `_etag`, `_attachments`, `_ts`) to each document.
    - These fields provide essential information about the document's metadata and versioning.
    - While querying data, consider excluding these fields from your application's response payload to streamline data transmission and enhance security.
3. **Best Practices and Considerations**:
    - **Partition Key Selection**: Optimize your partition key based on access patterns and query requirements.
    - **Scalability**: Leverage Cosmos DB's serverless pricing model for cost-effective scalability, paying only for the resources consumed.
    - **Consistency Levels**: Configure appropriate consistency levels based on your application's read and write requirements.

### Challenges and Solutions

1. **Partition Key Design**:
    - **Challenge**: Choosing an inefficient partition key can lead to uneven data distribution and performance issues.
    - **Solution**: Perform thorough analysis of your data access patterns and workload characteristics before finalizing the partition key.
2. **ID Field Management**:
    - **Challenge**: Managing the uniqueness and generation of the `id` field across distributed systems.
    - **Solution**: Utilize unique identifiers or composite keys that ensure uniqueness and prevent conflicts during data operations.
3. **Metadata Handling**:
    - **Challenge**: Dealing with metadata fields (`_rid`, `_self`, etc.) when processing query results.
    - **Solution**: Implement data cleaning functions in your application to filter out metadata fields before returning query results to users.

### Conclusion

Setting up an Azure Cosmos DB serverless API for storing data in table format involves careful planning of the partition key, management of the `id` field, and understanding of metadata handling. By following best practices and understanding these key concepts, you can effectively design scalable and efficient data storage solutions in Azure Cosmos DB. This approach ensures optimal performance and streamlined data management for your applications.


### Step-by-Step Guide to Create a Function App and Azure Function with HTTP Trigger

### 1. Log into Azure CLI and Set Subscription (if not already set)

```bash
bashCopy code
az login
az account set --subscription <subscription_id>

```

### 2. Create a Resource Group

```bash
bashCopy code
az group create --name ResumeFunctionGroup --location <region>
#you do not need to create another resource group if you have created intially for the Cosmos Bb
#skip this step if so but remember the name name of your resource group
```

Replace `<region>` with your preferred Azure region, e.g., `centralus`.

### Create a Storage Account (required for Function App)

```bash
bash code
az storage account create --name resumestorage --location <region> --resource-group ResumeFunctionGroup --sku Standard_LRS
#if you have created one intially for your Cosmos Db account skip this step
#but rememeber the name of your storage account it is important

```

### 4. Create a Function App within the Resource Group

```bash
bash code
az functionapp create --name ResumeFunctionApp --storage-account resumestorage --consumption-plan-location <region> --resource-group ResumeFunctionGroup --runtime python --runtime-version 3.10 --functions-version 4

```

- `-runtime` specifies the runtime environment (Python).
- `-runtime-version` specifies the version of Python (3.10 in this case).
- `-functions-version` specifies the version of Azure Functions runtime (4).

### create an HTTP Trigger Function inside the Function App

```bash
bash code
az functionapp function create --name ResumeHttpTrigger --namespace ResumeFunctions --authlevel anonymous --function-name ResumeHttpTrigger --resource-group ResumeFunctionGroup --runtime python --trigger-http --disable-app-insights


```

- `-authlevel` specifies the authentication level (anonymous allows public access).
- `-function-name` specifies the name of the function.
- `-trigger-http` creates an HTTP trigger function.
  ## Modify Function Code
Openfunction_app.py:

In the newly created project, navigate to the GetResume function folder.

Open function_app.py

Replace the default code:

Replace the default code with the following Python code to fetch data from CosmosDB:

```python
import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient, exceptions
from datetime import datetime
import json

# Environment variables
COSMOS_DB_ENDPOINT = os.environ['COSMOS_DB_ENDPOINT']
COSMOS_DB_KEY = os.environ['COSMOS_DB_KEY']
COSMOS_DB_DATABASE = os.environ['COSMOS_DB_DATABASE']
COSMOS_DB_CONTAINER = os.environ['COSMOS_DB_CONTAINER']

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
database = client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)
# Define the function app
app = func.FunctionApp()

@app.function_name("GetResumeData")
@app.route("getresumedata", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

```

By following these steps, you can effectively create a Function App and an Azure Function with an HTTP trigger using Azure CLI. This setup allows you to develop and deploy serverless functions for your resume project, handling HTTP requests and returning JSON data dynamically. Adjust the example code and configuration as per your project's requirements and data source integration.

```python
import azure.functions as func
import logging
import os
from azure.cosmos import CosmosClient, exceptions
from datetime import datetime
import json

# Environment variables
COSMOS_DB_ENDPOINT = os.environ['COSMOS_DB_ENDPOINT']
COSMOS_DB_KEY = os.environ['COSMOS_DB_KEY']
COSMOS_DB_DATABASE = os.environ['COSMOS_DB_DATABASE']
COSMOS_DB_CONTAINER = os.environ['COSMOS_DB_CONTAINER']

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_DB_ENDPOINT, credential=COSMOS_DB_KEY)
database = client.get_database_client(COSMOS_DB_DATABASE)
container = database.get_container_client(COSMOS_DB_CONTAINER)
# Define the function app
app = func.FunctionApp()

@app.function_name("GetResumeData")
@app.route("getresumedata", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

```

### **Configure Local Settings**

open the

1.  `local.settings.json`:
    - In the root of your function app project, open `local.settings.json`.
    - Add the following content to the file:

**COPY**

```python
    {
        "IsEncrypted": false,
        "Values": {
            "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
            "AzureWebJobsStorage": "UseDevelopmentStorage=true",
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "CosmosDB_URL": "<YOUR_COSMOS_DB_ENDPOINT>",
            "CosmosDB_Key": "<YOUR_COSMOS_DB_KEY>",
            "CosmosDB_Database": "<YOUR_COSMOSDB_DATABASE>",
            "CosmosDB_Container": "<YOUR_COSMOSDB_CONTAINER>"
        }
    }

```

### **Test Locally**

1. **Install Azure Functions Core Tools:**
    - Install the Azure Functions Core Tools if you haven’t already.
    - The installation instructions are [**here**](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2).
    - Open the terminal in VS Code.
2. **Run the Function:**
    
    **COPY**
    
    **COPY**
    
    ```bash
     func start
    
    ```
    
    - Test the function by navigating to it
        
        [**`http://localhost:7071/resumeapi?id=<value>`**](http://localhost:7071/resumeapi?id=1) in your browser or using a tool like Postman.
        

### **Deploy to Azure**

1. **Deploy the Function:**
    - In the Azure Functions extension in VS Code, right-click your function app project.
    - Select "Deploy to Function App".
    - Choose your subscription.
    - deploy to the function app you have created initally.

### **Step 5: Set Up GitHub Actions for CI/CD**

1. **Create a GitHub Repository:**
    - Initialize a new GitHub repository for your project.
    - Push your local function app code to GitHub.
2. **Create a GitHub Actions Workflow:**
    - In your GitHub repository, create a `.github/workflows/deployment.yml` file with the following content:
    
    ```yaml
      -name: Build and deploy Python project to Azure Function App - azureresumeapp
    
    on:
      push:
        branches:
          - main
      workflow_dispatch:
    
    env:
      AZURE_FUNCTIONAPP_PACKAGE_PATH: '.' # set this to the path to your web app project, defaults to the repository root
      PYTHON_VERSION: '3.10'
    
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4
    
          - name: Setup Python version
            uses: actions/setup-python@v2
            with:
              python-version: ${{ env.PYTHON_VERSION }}
    
          - name: Create and start virtual environment
            run: |
              python -m venv venv
              source venv/bin/activate
    
          - name: Install dependencies
            run: pip install -r requirements.txt
    
          - name: Zip artifact for deployment
            run: |
              zip -r release.zip ./* -x venv/\*
    
          - name: Upload artifact for deployment job
            uses: actions/upload-artifact@v2
            with:
              name: python-app
              path: release.zip
    
      deploy:
        runs-on: ubuntu-latest
        needs: build
        environment:
          name: 'production'
          url: ${{ steps.deploy-to-function.outputs.webapp-url }}
    
        steps:
          - name: Download artifact from build job
            uses: actions/download-artifact@v2
            with:
              name: python-app
    
          - name: Unzip artifact for deployment
            run: unzip -o release.zip
    
          - name: Deploy to Azure Functions
            uses: Azure/functions-action@v1
            with:
              app-name: azureresumeapp
              package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
              publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
              scm-do-build-during-deployment: true
              enable-oryx-build: true
            env:
              CosmosDB_URL: ${{ secrets.CosmosDB_URL }}
              CosmosDB_Key: ${{ secrets.CosmosDB_Key }}
              CosmosDB_Database: ${{ secrets.CosmosDB_Database }}
              CosmosDB_Container: ${{ secrets.CosmosDB_Container
    ```
    

To avoid having issue with the authentification level i employ you to use that simple structure workflow for a beginner if you are new techies
