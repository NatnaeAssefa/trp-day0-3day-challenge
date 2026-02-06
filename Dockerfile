# Project Chimera — runtime and test environment
# Python 3.11+ per pyproject.toml
FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install project and deps (includes pytest)
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "pytest", "tests/", "-v"]
