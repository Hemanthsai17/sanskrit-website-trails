from flask import Flask, render_template, request, session, redirect
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Define a list of Excel sheet names
excel_sheets = ['Sheet1', 'Sheet2', 'Sheet3']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_sheet = request.form['sheet']
        # Load the selected Excel sheet into a Pandas DataFrame
        df = pd.read_excel('C:\\Users\\sskir\\Desktop\\flask\\one more\\raghuvamsha_sarga_03.xlsx', sheet_name=selected_sheet)
        # Perform any processing on the DataFrame here

        # Store the DataFrame as a serialized string in the session
        session['df'] = df.to_json()
        session['row_index'] = 0  # Initialize row index

        return redirect('/result')

    return render_template('index.html', excel_sheets=excel_sheets)

@app.route('/result', methods=['GET', 'POST'])
def result():
    # Retrieve the stored DataFrame and row index from the session
    df_json = session.get('df')
    row_index = session.get('row_index')

    if not df_json:
        return redirect('/')  # Redirect to the index page if DataFrame is not available

    df = pd.read_json(df_json)  # Convert the serialized DataFrame back to a DataFrame object

    if request.method == 'POST':
        if 'next' in request.form:
            row_index += 1  # Move to the next row
        elif 'previous' in request.form:
            row_index -= 1  # Move to the previous row

    num_rows = len(df)
    num_columns = len(df.columns)
    sloka = df.iloc[row_index, 0]  # Assuming the "sloka" is in the first column

    # Get the selected columns to display
    selected_columns = request.form.getlist('columns')

    # Get the row values for the selected columns
    row_values = df.iloc[row_index][selected_columns].values

    # Disable/enable previous and next buttons based on the row index
    disable_previous = row_index == 0
    disable_next = row_index == num_rows - 1

    return render_template('result.html', sloka=sloka, row_values=row_values,
                           selected_columns=selected_columns, disable_previous=disable_previous,
                           disable_next=disable_next)

if __name__ == '__main__':
    app.run(debug=True)
