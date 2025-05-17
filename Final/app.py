from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configure upload folder for Excel files
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_excel(file_path):
    return pd.read_excel(file_path)

def save_excel(file_path, df):
    df.to_excel(file_path, index=False)

@app.route('/')
def home():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.xlsx')]
    return render_template('index2.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return redirect(url_for('home'))

    return redirect(request.url)

@app.route('/select_sentiments/<filename>', methods=['GET', 'POST'])
def select_sentiments(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = load_excel(file_path)

    if request.method == 'POST':
        selected_text = request.form.get('selected_text')
        selected_sentiments = request.form.getlist('sentiments')

        # Check if the DataFrame is not empty
        if not df.empty:
            # Update DataFrame based on selected sentiments
            df.loc[df['Sanskrit Text'] == selected_text, selected_sentiments] = 1

            # Save the updated DataFrame to the Excel file
            save_excel(file_path, df)

    sanskrit_texts = df['Sanskrit Text'].tolist()
    sentiments = df.columns[1:].tolist()

    return render_template('select_sentiments.html', filename=filename, sanskrit_texts=sanskrit_texts, sentiments=sentiments)


if __name__ == '__main__':
    app.run(debug=True)
