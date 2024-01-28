import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load the initial CSV file (if available)
a = pd.DataFrame()

def predict_mental_health(emp_id):
    # Check if the input Emp Id is present in the DataFrame
    try:
        emp_id = int(emp_id)  # Convert input to integer if possible
    except ValueError:
        return "The employee needs treatment"

    if not a.empty and emp_id in a['Emp Id'].values:
        # Get the corresponding Treatment value
        treatment_value = a.loc[a['Emp Id'] == emp_id, 'Treatment'].values[0]
        return "The employee doesn't need treatment"
    else:
        return "The employee needs treatment"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    global a  # Use the global DataFrame for storing uploaded data

    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return render_template('upload.html', message="No file part")

        file = request.files['file']

        # Check if the file is empty
        if file.filename == '':
            return render_template('upload.html', message="No selected file")

        # Save the uploaded file
        file.save("uploaded_file.xlsx" if file.filename.endswith('.xlsx') else "uploaded_file.csv")

        # Read the uploaded file
        try:
            if file.filename.endswith('.xlsx'):
                a = pd.read_excel("uploaded_file.xlsx", engine='openpyxl')
            else:
                a = pd.read_csv("uploaded_file.csv")
        except Exception as e:
            return render_template('upload.html', message=f"Error reading file: {str(e)}")

        # Redirect to the input page
        return redirect(url_for('input_page'))

    return render_template('upload.html')

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        # Use the existing predict_mental_health function
        emp_id = int(request.form['emp_id'])
        result = predict_mental_health(emp_id)

        return render_template('result.html', result=result)

    return render_template('input.html')

if __name__ == '__main__':
    app.run(debug=True)
