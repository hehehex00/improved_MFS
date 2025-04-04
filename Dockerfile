# Use a Python base image (latest version)
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /datatoolbox

# Copy the entire src directory into the container
COPY src /datatoolbox

# Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt



# Command to run the main.py when the container starts
CMD ["streamlit", "run", "main.py"]
