# Use Python slim image as base
FROM python:3.10-slim 


# Upgrade pip
RUN pip install --upgrade pip
    
# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create and set the working directory
RUN mkdir -p /app/src
WORKDIR /app

# Copy the source files into the container
COPY src /app/src/
COPY main_fast.py /app/

# Environment variables
ENV PYTHONUNBUFFERED True

# Expose the port
EXPOSE 8002

# Command to run the FastAPI application
CMD ["uvicorn", "main_fast:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]
