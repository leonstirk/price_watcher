# Use official Playwright image with all dependencies
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright dependencies (already present, but this ensures up-to-date)
RUN playwright install --with-deps

# Copy source code
COPY . .

# Command to run your app (modify as needed)
CMD ["python", "lambda_function.py"]