# Use a slim Python image for efficiency
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Installing poetry dependency management
RUN pip install poetry

# Copy poetry configuration
COPY pyproject.toml ./



# Install dependencies using poetry
RUN poetry install

# Copy your application code
COPY . .



# Environment variables for database connection (replace with your details)
ENV DATABASE_URL=postgresql://user:password@host:port/database

# Expose port for the FastAPI application (default: 8000)
EXPOSE 8000

# Command to run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
