from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import mysql.connector

app = Flask(__name__)

app.secret_key = "your_secret_key"

model = pickle.load(open('model.pkl', 'rb'))

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="joseph",
    password="root",
    database="loginpage"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('intro.html')  # Render the intro page

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = user[0]  # Store username in the session
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Login failed. Please try again.')

    return render_template('login.html')  # Render the login form


@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('home'))

@app.route('/predict', methods=['POST'])
def predict():
    with open('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)

    N = int(request.form['N'])
    P = int(request.form['P'])
    K = int(request.form['K'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['rainfall'])

    user_input = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

    prediction = model.predict(user_input)
    prediction_scalar = prediction[0]
    val = encoder[prediction_scalar]

    return render_template('result.html', predicted_class=val)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
