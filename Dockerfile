# Use a slim Python image for efficiency
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for scientific libraries and Git
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /research

# Install Python scientific stack for the world-happiness data-science project
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    seaborn \
    pandas \
    requests \
    wbgapi \
    pycountry \
    country_converter \
    jupyterlab

# Expose the Jupyter port
EXPOSE 8888

# Start Jupyter Lab 
# --allow-root is used here for container simplicity; 
# --ip=0.0.0.0 allows connections from outside the container
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]