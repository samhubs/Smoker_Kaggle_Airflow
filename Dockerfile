FROM apache/airflow:latest

USER root 

# # Copy kaggle.json into the container
# COPY ./kaggle.json /home/airflow/.kaggle/kaggle.json
# RUN chown -R airflow: /home/airflow/.kaggle
# RUN chmod 600 /home/airflow/.kaggle/kaggle.json

# Install the Python dependencies as root
COPY requirements.txt .

# Switch to the airflow user for pip install
USER airflow
RUN pip install --user --no-cache-dir -r requirements.txt

# Switch to the airflow user for running the service
USER root
