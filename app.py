
from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Path to save the data
FILE_PATH = 'wwwroot/output/bmi_data.xlsx'

def save_data(weight, height, bmi, category):
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
    else:
        df = pd.DataFrame(columns=['Weight (kg)', 'Height (cm)', 'BMI', 'Category', 'Record Time'])
    new_data = pd.DataFrame({
        'Weight (kg)': [weight], 
        'Height (cm)': [height], 
        'BMI': [bmi], 
        'Category': [category],
        'Record Time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(FILE_PATH, index=False)

def calculate_bmi(weight, height):
    height_m = height / 100  
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])

            if not (0.1 <= weight <= 150) or not (10 < height <= 200):
                return render_template('index.html', error="Invalid input. Weight must be between 0.1 and 150 kg, and height must be between 10 and 200 cm.")

            bmi = calculate_bmi(weight, height)
            category = get_bmi_category(bmi)
            save_data(weight, height, bmi, category)

            return render_template('index.html', bmi=bmi, category=category)
        except ValueError:
            return render_template('index.html', error="Invalid input. Please enter valid numbers.")

    return render_template('index.html')

@app.route('/download')
def download_file():
    return send_file(FILE_PATH, as_attachment=True)

@app.route('/report')
def report():
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        data = df.to_dict(orient='records')
    else:
        data = []
    return render_template('report.html', data=data)

@app.route('/bmi_explanation')
def bmi_explanation():
    return render_template('bmi_explanation.html')



if __name__ == '__main__':
    app.run(debug=True)
