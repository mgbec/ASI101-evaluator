FROM public.ecr.aws/lambda/python:3.12

# Copy requirements and install dependencies
COPY requirements_minimal.txt .
RUN pip install --no-cache-dir -r requirements_minimal.txt

# Copy application code
COPY test_agent.py .
COPY goal_hijack_evaluator.py .

# Set the CMD to your handler
CMD ["test_agent.app"]
