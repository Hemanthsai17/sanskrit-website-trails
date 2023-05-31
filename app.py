from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.form['file']
        df = pd.read_excel(file)  # Read the selected Excel file
        columns = df.columns.tolist()  # Get the column names

        if 'current_row' in request.form:
            current_row = int(request.form['current_row'])
        else:
            current_row = 0  # Start with the first row
        
        num_rows = len(df)  # Total number of rows

        # Get the values of selected columns for the current row
        values = df.loc[current_row, columns].tolist()

        # Retrieve selected options from checkboxes
        selected_options = request.form.getlist('options')

        # Save selected options to the Excel file
        target_column = "SelectedOptions"
        for option in selected_options:
            df.loc[current_row, target_column] = option
        df.to_excel(file, index=False)

        return render_template('index.html', file=file, columns=columns, values=values,
                               current_row=current_row, num_rows=num_rows,
                               selected_options=selected_options,
                               target_column=target_column)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
