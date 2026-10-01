# Start from an official Python image (same version as the local venv)
FROM python:3.9-slim

# All following commands run inside /app in the container
WORKDIR /app

# Install dependencies first so this layer is cached when only code changes
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Flask listens on port 5000
EXPOSE 5000

# --host=0.0.0.0 makes the server reachable from outside the container
CMD ["python3", "-m", "flask", "--app", "hello", "run", "--host=0.0.0.0"]
