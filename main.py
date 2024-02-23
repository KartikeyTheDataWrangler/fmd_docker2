import os
import sys
import numpy as np
import pickle
from flask import Flask, request, jsonify

# Fixing file path separator
with open(file=r'artifacts\current_best_model\model.pkl', mode="rb") as file:
    current_model = pickle.load(file)

app = Flask(__name__)

# Define an endpoint for making predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the request
        data = request.get_json(force=True)
        input_data = np.array(data['input']).reshape(1, -1)

        # Make prediction using the loaded model
        prediction = current_model.predict(input_data)

        # Return the prediction as JSON response
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)

