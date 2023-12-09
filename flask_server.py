from flask import Flask, request, jsonify, send_from_directory, render_template_string
import pandas as pd
from lightgbm import LGBMClassifier
import lightgbm
import os

app = Flask(__name__)

# Update the paths according to your Docker container's directory structure
MODEL_PATH = '/opt/airflow/lgb_classifier.txt'  
PLOTS_FOLDER = '/opt/airflow/plots'

# Load your trained model
# model = LGBMClassifier()
model = lightgbm.Booster(model_file=MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame(data, index=[0])
    prediction = model.predict(df)
    return jsonify({'prediction': list(prediction)})

@app.route('/')
def index():
    # List all .png files in the plots folder
    plot_files = [f for f in os.listdir(PLOTS_FOLDER) if f.endswith('.png')]

    # Generate HTML with links to the images
    html = "<h1>Welcome to the Plot Server!</h1>"
    for file in plot_files:
        image_url = f"/plots/{file}"
        html += f'<div><a href="{image_url}">{file}</a></div>'

    return render_template_string(html)

@app.route('/plots/<filename>')
def serve_plot(filename):
    return send_from_directory(PLOTS_FOLDER, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
