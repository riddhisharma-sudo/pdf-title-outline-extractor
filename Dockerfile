FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --prefer-binary --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Command to run your main script (customize if needed)
CMD ["python", "main.py"]


