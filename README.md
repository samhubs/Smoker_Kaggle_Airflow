# Smoker Status Prediction Using Biosignals

## Overview
This project utilizes biosignal data to predict smoker status, showcasing an end-to-end machine learning workflow with Apache Airflow, Docker, and LightGBM.

## Prerequisites
- Docker
- Apache Airflow
- Python (with libraries listed in `requirements.txt`)

## Installation
Clone the repository and navigate to the project directory. Build and start Docker containers using:


## Project Structure
- `Dockerfile`: Sets up the environment.
- `docker-compose.yml`: Configures Airflow services.
- `dags/`: Contains Airflow DAGs for data processing and model training.
- `models/`: Stores the trained LightGBM model.

## Running the Project
Start the Airflow webserver and access the UI at `localhost:8080`. Trigger DAGs for data processing and model training.

## Model Training
Details on data processing, feature engineering, and the LightGBM model training are provided in the DAG files.

## API Reference
The Flask server offers endpoints for model predictions and visualizations.

## Contributing
Guidelines for contributing are provided.

## Acknowledgments
Thanks to the contributors of the [Kaggle Dataset](https://www.kaggle.com/datasets/gauravduttakiit/smoker-status-prediction-using-biosignals).
