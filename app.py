from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)
