from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

# Folder where plots are saved
PLOTS_FOLDER = '/home/sameer/GitHub_projects/Airflow tutorials/Smoke_markers_binary_classification/plots'

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
