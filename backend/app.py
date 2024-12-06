from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Path to the saved model
MODEL_PATH = 'backend/model/model.h5'

# Load the model
model = load_model(MODEL_PATH)

@app.route('/extract_features', methods=['POST'])
def extract_features():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Use your existing extract_features function from script_ig.py
        profile_info, features = extract_features_instaloader(username) 

        if not features:
            return jsonify({'error': 'Failed to extract features'}), 500

        return jsonify({'features': features})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])  # New endpoint
def analyze():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Extract features
        features = extract_features_instaloader(username)

        if not features:
            return jsonify({'error': 'Failed to extract features'}), 500

        # Make prediction
        prediction = model.predict([features])
        fake_probability = float(prediction[0])

        # Return result as JSON
        return jsonify({
            'fake_probability': fake_probability,
            'is_fake': fake_probability == 1
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the incoming JSON payload
        data = request.get_json()
        
        # Validate the input
        if not data or 'features' not in data:
            return jsonify({'error': 'Invalid input, must include "features" field'}), 400

        features = data['features']

        if len(features) != 11:  # Adjust based on your model's input shape
            return jsonify({'error': f'Invalid input size, expected 11 features, got {len(features)}'}), 400

        input_data = np.array(features).reshape(1, -1)  # Shape (1, 11)

        prediction = model.predict(input_data)
        fake_probability = float(prediction[0][0])  

        # Return result as JSON
        return jsonify({
            'fake_probability': fake_probability,
            'is_fake': fake_probability >= 0.5  # Assuming 0.5 threshold for binary classification
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
