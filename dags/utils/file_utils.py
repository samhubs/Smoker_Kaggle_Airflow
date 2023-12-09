import pandas as pd
import numpy as np

#Save filess
def save_files(df, suffix):
    try:
        df.to_csv('/opt/airflow/data' + suffix +'.csv')
    except Exception as e:
        raise(f"Could not write the dataframe due to {e}")
