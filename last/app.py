from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
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
