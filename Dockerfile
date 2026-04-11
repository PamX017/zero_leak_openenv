# Use a lightweight, official Python runtime
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements from the server directory
COPY server/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the specific port Hugging Face Spaces requires
EXPOSE 7860

# Run the FastAPI server using uvicorn
# We point to server.app:app because the working directory in the container is /app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]