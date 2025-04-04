# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
EXPOSE 8000

# Command to run the FastAPI application with autoreload
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
