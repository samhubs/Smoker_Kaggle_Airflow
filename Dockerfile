FROM apache/airflow:latest

USER root 

# # Copy kaggle.json into the container
# COPY ./kaggle.json /home/airflow/.kaggle/kaggle.json
# RUN chown -R airflow: /home/airflow/.kaggle
# RUN chmod 600 /home/airflow/.kaggle/kaggle.json

RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
    
# Install the Python dependencies as root
COPY requirements.txt .

# Switch to the airflow user for pip install
USER airflow
RUN pip install --user --no-cache-dir -r requirements.txt

# Install Flask, pandas, and lightgbm for model serving
RUN pip install --user Flask pandas lightgbm

# Copy Flask server and model files to the container
COPY flask_server.py /opt/airflow/
COPY models/lgb_classifier.txt /opt/airflow/

# Expose port 5000 for the Flask server
EXPOSE 5000
# Ensure the airflow user has access to these files
# RUN chown -R airflow: /opt/airflow/flask_server.py /opt/airflow/lgb_classifier.txt


# Switch to the airflow user for running the service
USER root
