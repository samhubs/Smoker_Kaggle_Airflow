from airflow.decorators import dag, task
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from datetime import timedelta
from airflow.utils.dates import days_ago
from sklearn.preprocessing import StandardScaler, MinMaxScaler, FunctionTransformer
from sklearn.model_selection import KFold, StratifiedKFold, train_test_split

import optuna
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from lightgbm import LGBMClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV
from sklearn.metrics import accuracy_score, roc_auc_score, auc, roc_curve, classification_report, confusion_matrix, precision_score, recall_score, f1_score

@dag(
    schedule_interval=timedelta(days=1),
    start_date=days_ago(0),
    default_args={'owner':'airflow', 'retries':1, 'retry_delay':timedelta(minutes=5)},
    catchup=False,
    tags=['model_training_evaluation'],
)
def model_training():
    @task(task_id='Split_Data')
    def split_data():

        SEED = np.random.seed(44)

        X = pd.read_csv('/opt/airflow/data/X.csv')
        Y = pd.read_csv('/opt/airflow/data/Y.csv')

        X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                                                            test_size=0.33, 
                                                            random_state=SEED, 
                                                            shuffle =True)
        
        X_train.to_csv("/opt/airflow/data/X_train.csv", sep=',', index=False)
        X_test.to_csv("/opt/airflow/data/X_test.csv", sep=',', index=False)
        y_train.to_csv("/opt/airflow/data/y_train.csv", sep=',', index=False)
        y_test.to_csv("/opt/airflow/data/y_test.csv", sep=',', index=False)

    @task(task_id='model_training')
    def training():
        # X_train = pd.read_csv("/opt/airflow/data/X_train.csv")
        # X_test = pd.read_csv("/opt/airflow/data/X_test.csv")
        # y_train = pd.read_csv("/opt/airflow/data/y_train.csv")
        # y_test = pd.read_csv("/opt/airflow/data/y_test.csv")

        X = pd.read_csv('/opt/airflow/data/X.csv')
        Y = pd.read_csv('/opt/airflow/data/Y.csv')
        SEED = np.random.seed(44)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, 
                                                            test_size=0.33, 
                                                            random_state=SEED, 
                                                            shuffle =True)
        
        # Best hyperparameters for LGBM Classifier
        lgbm_params = {'n_estimators': 624, 
                    'max_depth': 46, 
                    'learning_rate': 0.06953273561619135, 
                    'min_child_weight': 2.4187716216112944, 
                    'min_child_samples': 230, 
                    'subsample': 0.9515130309407626, 
                    'subsample_freq': 4, 
                    'colsample_bytree': 0.402284262124352, 
                    'num_leaves': 71
                    }

        # Build the LightGBM model
        LGBMModel = LGBMClassifier(**lgbm_params, random_state=SEED)
        # Train the model
        LGBMModel.fit(X_train, y_train)

        #save the model 
        LGBMModel.booster_.save_model('/opt/airflow/models/lgb_classifier.txt') 

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

    split_data() >> training()


dag = model_training()