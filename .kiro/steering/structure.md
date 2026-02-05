# Project Structure

## Repository Organization

```
amazon-bedrock-agentcore-samples/
├── 01-tutorials/              # Interactive learning & foundations
├── 02-use-cases/              # End-to-end applications
├── 03-integrations/           # Framework & protocol integrations
├── 04-infrastructure-as-code/ # IaC templates (CFN, CDK, Terraform)
├── 05-blueprints/             # Full-stack reference applications
├── requirements.txt           # Root dependencies
├── README.md                  # Main documentation
├── CONTRIBUTING.md            # Contribution guidelines
└── LICENSE                    # Apache 2.0 license
```

## Folder Conventions

### 01-tutorials/
Organized by AgentCore component:
- `01-AgentCore-runtime/`: Hosting agents and MCP servers
- `02-AgentCore-gateway/`: API-to-tool transformations
- `03-AgentCore-identity/`: Authentication and authorization
- `04-AgentCore-memory/`: Memory patterns and integration
- `05-AgentCore-tools/`: Code Interpreter and Browser tools
- `06-AgentCore-observability/`: Monitoring and tracing
- `07-AgentCore-evaluations/`: Agent quality assessment
- `08-AgentCore-policy/`: Fine-grained access control
- `09-AgentCore-E2E/`: Complete end-to-end example

Each tutorial contains:
- Jupyter notebooks (`.ipynb`)
- `README.md` with overview
- `images/` for diagrams
- Supporting Python scripts

### 02-use-cases/
Each use case is self-contained with:
- Main agent implementation (e.g., `cost_optimization_agent.py`)
- `README.md`: Overview and features
- `ARCHITECTURE.md`: Architecture details (optional)
- `DEPLOYMENT.md`: Deployment instructions (optional)
- `requirements.txt`: Dependencies
- `deploy.py`: Deployment script
- `cleanup.py`: Resource cleanup script
- `test_local.py`: Local testing
- `test_agentcore_runtime.py`: Runtime testing
- `tools/`: Custom tool implementations
- `images/`: Architecture diagrams
- `.gitignore`: Ignore patterns
- `pyproject.toml`: Project metadata (optional)

### 03-integrations/
Organized by integration type:
- `agentic-frameworks/`: Framework-specific examples (Strands, LangGraph, CrewAI, etc.)
- `observability/`: Observability platform integrations
- `IDP-examples/`: Identity provider examples (Okta, EntraID)
- `ux-examples/`: UI/UX patterns (Streamlit, etc.)
- `vector-stores/`: Vector database integrations

### 04-infrastructure-as-code/
Three parallel implementations:
- `cloudformation/`: YAML/JSON templates
- `cdk/`: Python CDK stacks
- `terraform/`: HCL configurations

Each contains the same samples:
- `basic-runtime/`: Simple agent deployment
- `mcp-server-agentcore-runtime/`: MCP server hosting
- `multi-agent-runtime/`: Multi-agent systems
- `end-to-end-weather-agent/`: Complete agent with tools and memory

### 05-blueprints/
Production-ready full-stack applications:
- Complete frontend and backend
- Infrastructure code
- Authentication and authorization
- Deployment automation
- Example: `end-to-end-customer-service-agent/`, `shopping-concierge-agent/`

## Common File Patterns

### Agent Implementation Files
- Main agent: `{name}_agent.py` or `agent.py`
- Entry point uses `BedrockAgentCoreApp` with `@app.entrypoint` decorator
- Tools defined with `@tool` decorator
- Strands `Agent` initialized with model, tools, and system_prompt

### Tool Organization
```
tools/
├── __init__.py
├── {domain}_tools.py    # e.g., cost_explorer_tools.py
└── {domain}_tools.py    # e.g., budget_tools.py
```

### Configuration Files
- `.env.example`: Template for environment variables
- `config.py` or `config/`: Configuration management
- `utils.py` or `utils/`: Shared utilities

### Testing Files
- `test_local.py`: Local development testing
- `test_agentcore_runtime.py`: Deployed agent testing
- `test_*.py`: Additional test files

### Documentation Files
- `README.md`: Primary documentation (always present)
- `ARCHITECTURE.md`: Architecture details
- `DEPLOYMENT.md`: Deployment guide
- `images/`: Diagrams and screenshots

## Code Organization Patterns

### Agent Structure
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

@tool
def my_tool(param: str) -> str:
    """Tool description for LLM"""
    # Implementation
    return result

model = BedrockModel(model_id="...")
agent = Agent(model=model, tools=[my_tool], system_prompt="...")

@app.entrypoint
async def process_request(payload):
    prompt = payload.get("prompt")
    async for event in agent.stream_async(prompt):
        yield event

if __name__ == "__main__":
    app.run()
```

### MCP Server Structure
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from mcp.server import Server
from mcp.types import Tool

app = BedrockAgentCoreApp(protocol="mcp")
server = Server("server-name")

@server.call_tool()
async def handle_tool(name: str, arguments: dict):
    # Tool implementation
    return result

@app.entrypoint
def mcp_entrypoint():
    return server

if __name__ == "__main__":
    app.run()
```

## Naming Conventions

- Folders: `kebab-case` (e.g., `cost-optimization-agent`)
- Python files: `snake_case` (e.g., `cost_optimization_agent.py`)
- Python classes: `PascalCase` (e.g., `CostOptimizationAgent`)
- Python functions/variables: `snake_case` (e.g., `get_cost_and_usage`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MODEL_ID`)
- Environment variables: `UPPER_SNAKE_CASE` (e.g., `AWS_REGION`)

## Import Conventions

Standard import order:
1. Standard library imports
2. Third-party imports (boto3, strands, etc.)
3. Local application imports (tools, utils)

Example:
```python
import logging
import os
from datetime import datetime

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
import boto3

from tools.my_tools import my_function
```
