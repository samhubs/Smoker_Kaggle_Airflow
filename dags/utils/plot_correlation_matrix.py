import pandas as pd
from matplotlib import pyplot as plt

def correlation_matrix(df, output_folder):
    # Assuming df is your DataFrame
    # Calculate the correlation matrix
    corr_matrix = df.corr()
    import matplotlib.pyplot as plt

    plt.matshow(corr_matrix)
    plt.colorbar()
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
    plt.show()
    plot_filename = f'{output_folder}/correlation_matrix.png'
    plt.savefig(plot_filename)
