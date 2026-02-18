# Dockerfile

# 1. Use an official, lightweight Python image
FROM python:3.12-slim

# 2. Set environment variables to optimize Python for Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies (Crucial for MySQL and compiling packages)
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy the rest of your project code into the container
COPY . /app/

# 7. Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# 8. Expose the port Gunicorn will run on
EXPOSE 8000

# 9. Use the entrypoint script to start the application
ENTRYPOINT ["/app/entrypoint.sh"]