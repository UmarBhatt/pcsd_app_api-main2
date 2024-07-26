# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN python -m venv /opt/venv && . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app's source code into the container at /app
COPY . .

# Set the environment variable for the PATH
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]