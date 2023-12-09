import matplotlib.pyplot as plt
import pandas as pd

def generate_histograms(dataframe, output_folder):
    for column in dataframe.columns:
        plt.figure()
        dataframe[column].hist()
        plt.title(f'Histogram of {column}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plot_filename = f'{output_folder}/histogram_{column}.png'
        plt.savefig(plot_filename)
        plt.close()