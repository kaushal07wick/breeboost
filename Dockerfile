# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Command to run Streamlit app by default
CMD ["streamlit", "run", "dashboard/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
