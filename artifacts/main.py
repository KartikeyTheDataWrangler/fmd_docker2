import os
import sys
import numpy as np
import pickle
from flask import Flask, request, render_template

# Fixing file path separator
with open(file=r'current_best_model/model.pkl', mode="rb") as file:
    current_model = pickle.load(file)

app = Flask(__name__)

# Define an endpoint for rendering the HTML form
@app.route('/')
def home():
    return render_template('index.html')

# Define an endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data = request.form.to_dict(flat=False)
        input_data = np.array([(data[key]) for key in sorted(data.keys())]).reshape(1, -1)

        # Make prediction using the loaded model
        prediction = current_model.predict(input_data)

        # Return the prediction to the HTML template
        return render_template('index.html', prediction=prediction[0])
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)
