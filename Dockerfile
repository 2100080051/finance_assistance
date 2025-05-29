# Use a lightweight base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by Hugging Face (must be 7860)
EXPOSE 7860

# Run the FastAPI server
CMD ["uvicorn", "orchestrator:app", "--host", "0.0.0.0", "--port", "7860"]
