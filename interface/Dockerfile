FROM python:3.11-bullseye

# Looks one level up, as we have 1 requirements for all projects for now
COPY requirements.txt .
RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

# Copy app code into container
COPY interface /app

# Install dependencies
WORKDIR /app

# Run streamlit
CMD streamlit run --server.enableCORS=false --server.port=8001 Home.py
