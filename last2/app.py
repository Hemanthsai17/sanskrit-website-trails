from flask import Flask, render_template, request, redirect, session
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'
EXCEL_FOLDER = 'excel_files/'

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        college = request.form['college']
        course = request.form['course']

        session['name'] = name
        session['college'] = college
        session['course'] = course

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform login authentication here

        session['logged_in'] = True

        return redirect('/home')

    return render_template('login.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect('/login')

    name = session['name']
    college = session['college']
    course = session['course']

    excel_files = get_excel_files()
    selected_file = None
    file_data = None
    current_row = session.get('current_row', 0)

    if request.method == 'POST':
        selected_file = request.form['excel_file']
        if selected_file:
            if 'next' in request.form:
                current_row += 1
            elif 'previous' in request.form:
                current_row -= 1
            elif 'save' in request.form:
                selected_options = request.form.getlist('options')
                save_options(selected_file, current_row, selected_options)

            file_data, total_rows = read_excel_file(selected_file, current_row)
            if current_row >= total_rows:
                current_row = 0
            elif current_row < 0:
                current_row = total_rows - 1

            session['current_row'] = current_row

    options = get_options()

    return render_template('home.html', name=name, college=college, course=course, excel_files=excel_files, selected_file=selected_file, file_data=file_data, current_row=current_row, options=options)

def get_excel_files():
    excel_files = []
    for file in os.listdir(EXCEL_FOLDER):
        if file.endswith('.xlsx'):
            excel_files.append(file)
    return excel_files

def read_excel_file(filename, row_number):
    filepath = os.path.join(EXCEL_FOLDER, filename)
    df = pd.read_excel(filepath)
    total_rows = len(df)
    row_data = df.iloc[row_number]
    return row_data.to_dict(), total_rows

def get_options():
    # Modify this function to return your desired options
    options = [ 'nirveda, indifference', 'viṣāda, moroseness', 'dainya, meekness', 'glāni, a feeling that one is in a faulty position', 'śrama, fatigue', 'mada, madness', 'garva, pride', 'śaṅkā, doubt', 'trāsa, shock', 'āvega, intense emotion', 'unmāda, craziness', 'apasmāra, forgetfulness', 'vyādhi, disease', 'moha, bewilderment', 'mṛti, death', 'ālasya, laziness', 'jāḍya, invalidity', 'vrīḍā, shame', 'avahitthā, concealment', 'smṛti, remembrance', 'vitarka, argument', 'cintā, contemplation', 'mati, attention', 'dhṛti, forbearance', 'harṣa, jubilation', 'autsukya, eagerness', 'augrya, violence', 'amarṣa, anger', 'asūyā, jealousy', 'cāpalya, impudence', 'nidrā, sleep', 'supti, deep sleep', 'prabodha, awakening']
    return options

def save_options(filename, row_number, selected_options):
    filepath = os.path.join(EXCEL_FOLDER, filename)
    df = pd.read_excel(filepath)
    df.at[row_number, 'TargetColumn'] = ', '.join(selected_options)
    df.to_excel(filepath, index=False)

if __name__ == '__main__':
    app.run(debug=True)
