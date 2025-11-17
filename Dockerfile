# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt first for best Docker caching
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code to the container
COPY . .

# Optionally set container environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port that your app runs on (change if your app uses another port)
EXPOSE 8000

# Start your application (change app.py if your main file is named differently)
CMD ["python", "app.py"]
