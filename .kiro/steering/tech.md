# Technology Stack

## Primary Languages & Frameworks

- **Python 3.10+**: Primary language for agent implementations
- **Jupyter Notebooks**: Interactive tutorials and examples (.ipynb files)
- **TypeScript/JavaScript**: Some MCP server implementations and frontend applications

## Core Dependencies

### Agent Frameworks
- **Strands Agents**: Primary framework for agent examples
- **LangGraph**: Graph-based agent workflows
- **LangChain**: Agent orchestration and tools
- **CrewAI**: Multi-agent collaboration
- **LlamaIndex**: Data-augmented agents
- **OpenAI Agents**: OpenAI SDK-based agents
- **PydanticAI**: Type-safe agent framework

### AWS Services
- **Amazon Bedrock**: LLM access (Claude, Nova, etc.)
- **Amazon Bedrock AgentCore**: Runtime, Gateway, Memory, Identity, Tools, Observability
- **AWS Lambda**: Serverless functions
- **Amazon ECR**: Container registry
- **Amazon S3**: Storage
- **Amazon Cognito**: Authentication
- **IAM**: Access management

### Key Libraries
- `bedrock-agentcore`: AgentCore Python SDK
- `bedrock-agentcore-starter-toolkit`: CLI for deployment
- `boto3`: AWS SDK for Python
- `mcp>=1.9.0`: Model Context Protocol
- `strands-agents`: Strands framework
- `strands-agents-tools`: Built-in tools
- `langchain[aws]`: LangChain with AWS integrations
- `langgraph`: Graph-based workflows
- `uv`: Fast Python package manager

## Infrastructure as Code

- **AWS CloudFormation**: YAML/JSON templates
- **AWS CDK**: Python-based infrastructure
- **Terraform**: HCL-based infrastructure with state management

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install with uv (faster)
uv pip install -r requirements.txt
```

### Jupyter Notebooks
```bash
# Register kernel
python -m ipykernel install --user --name=notebook-venv --display-name="Python (notebook-venv)"

# List kernels
jupyter kernelspec list

# Run notebook
jupyter notebook path/to/notebook.ipynb
```

### AgentCore Deployment (Starter Toolkit)
```bash
# Configure agent
agentcore configure -e my_agent.py

# Deploy to AWS
agentcore launch

# Invoke deployed agent
agentcore invoke '{"prompt": "Hello"}'

# Clean up resources
agentcore cleanup
```

### Local Testing
```bash
# Start agent locally
python my_agent.py

# Test with curl (in another terminal)
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```

### Docker
```bash
# Build image
docker build -t my-agent .

# Run container
docker run -p 8080:8080 my-agent
```

## Development Tools

- **Docker/Finch**: Container runtime for local development
- **AWS CLI**: AWS command-line interface
- **Git**: Version control
- **JupyterLab**: Interactive development environment

## Testing

- Test files typically named: `test_local.py`, `test_agentcore_runtime.py`
- Use `pytest` for unit tests
- Integration tests often use boto3 to invoke deployed agents

## Configuration Files

- `requirements.txt`: Python dependencies
- `pyproject.toml`: Python project metadata (some projects)
- `.env` / `.env.example`: Environment variables
- `Dockerfile`: Container definitions
- `README.md`: Project documentation
- `ARCHITECTURE.md`: Architecture details (use cases)
- `DEPLOYMENT.md`: Deployment instructions (use cases)
