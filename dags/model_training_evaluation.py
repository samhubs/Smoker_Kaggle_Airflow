from airflow.decorators import dag, task
from airflow.sensors.external_task_sensor import ExternalTaskSensor
import numpy as np
import pandas as pd 
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier

# Define the DAG for model training and evaluation
@dag(
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 11, 9, 19, 30), #9 Dec, 12:30 PM MST,
    default_args={'owner': 'airflow', 'retries': 1, 'retry_delay': timedelta(minutes=5)},
    catchup=False,
    tags=['model_training_evaluation'],
)
def model_training():
    # Task to split the dataset into training and testing sets

    # Wait for Data processing DAG to complete
    wait_for_dag1 = ExternalTaskSensor(
        task_id='wait_for_dag1_task',
        external_dag_id='data_processing',  # Replace with the actual dag_id of dag1
        external_task_id='save_data_task',  # Replace with a task_id from dag1 to wait on
        timeout=600,
        poke_interval=30,
        mode='reschedule',
    )

    @task(task_id='split_data')
    def split_data():
        SEED = np.random.seed(44)
        X = pd.read_csv('/opt/airflow/data/X.csv')
        Y = pd.read_csv('/opt/airflow/data/Y.csv')
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=SEED, shuffle=True)
        X_train.to_csv("/opt/airflow/data/X_train.csv", sep=',', index=False)
        X_test.to_csv("/opt/airflow/data/X_test.csv", sep=',', index=False)
        y_train.to_csv("/opt/airflow/data/y_train.csv", sep=',', index=False)
        y_test.to_csv("/opt/airflow/data/y_test.csv", sep=',', index=False)

    # Task for training the model
    @task(task_id='model_training_saving')
    def training():
        SEED = np.random.seed(44)
        X_train = pd.read_csv('/opt/airflow/data/X_train.csv')
        y_train = pd.read_csv('/opt/airflow/data/y_train.csv')

        # Define hyperparameters for the LGBM Classifier
        lgbm_params = {
            'n_estimators': 624, 'max_depth': 46, 'learning_rate': 0.06953273561619135,
            'min_child_weight': 2.4187716216112944, 'min_child_samples': 230,
            'subsample': 0.9515130309407626, 'subsample_freq': 4,
            'colsample_bytree': 0.402284262124352, 'num_leaves': 71
        }

        # Initialize and train the LGBM model
        LGBMModel = LGBMClassifier(**lgbm_params, random_state=SEED)
        LGBMModel.fit(X_train, y_train)
        # Save the trained model
        LGBMModel.booster_.save_model('/opt/airflow/models/lgb_classifier.txt')

    # Define the sequence of tasks
    wait_for_dag1 >> split_data() >> training()

# Instantiate the DAG
dag = model_training()


# Train the model
# LGBMModel.fit(X_train, y_train)
    
    # @task(task_id='Hyperparameter_tuning')
    # def hyperparameter_tuning_optuna():
    #     X = pd.read_csv('/opt/airflow/data/X.csv')
    #     Y = pd.read_csv('/opt/airflow/data/Y.csv')
    #     X_train = pd.read_csv("/opt/airflow/data/X_train.csv")
    #     X_test = pd.read_csv("/opt/airflow/data/X_test.csv")
    #     y_train = pd.read_csv("/opt/airflow/data/y_train.csv")
    #     y_test = pd.read_csv("/opt/airflow/data/y_test.csv")

    #     # Create an Optuna objective function
    #     def objective(trial):
    #         params = {
    #             'n_estimators' : trial.suggest_int('n_estimators', 500, 1000),
    #             'max_depth' : trial.suggest_int('max_depth', 30, 50),
    #             'learning_rate' : trial.suggest_float('learning_rate',1e-3, 0.25, log=True),
    #             'min_child_weight' : trial.suggest_float('min_child_weight', 0.5, 4),
    #             'min_child_samples' : trial.suggest_int('min_child_samples', 1, 250),
    #             'subsample' : trial.suggest_float('subsample', 0.2, 1),
    #             'subsample_freq' : trial.suggest_int('subsample_freq', 0, 5),
    #             'colsample_bytree' : trial.suggest_float('colsample_bytree', 0.2, 1),
    #             'num_leaves' : trial.suggest_int('num_leaves', 50, 100),
    #         }
            
    #         # Build the lgbm model
    #         lgbmmodel_optuna = LGBMClassifier(**params,
    #         )
    #         # Evaluate the model
    #         cv = cross_val_score(lgbmmodel_optuna, X, Y, cv = 4, scoring='roc_auc').mean()
    #         return cv

    #     # Create the Optuna study
    #     study = optuna.create_study(direction='maximize')
    #     study.optimize(objective, n_trials=25, timeout=2000)

    #     pd.DataFrame(study.best_params).to_csv("/opt/airflow/data/optim_params.csv")