FROM public.ecr.aws/docker/library/python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir bedrock-agentcore strands-agents

# Copy application code
COPY test_agent.py .
COPY goal_hijack_evaluator.py .

# Expose port for AgentCore Runtime
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/ping || exit 1

# Run the agent
CMD ["python", "test_agent.py"]
