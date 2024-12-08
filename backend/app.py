# # app.py
# from flask import Flask, request, jsonify
# import numpy as np
# import instaloader
# import pickle
# from tensorflow.keras.models import load_model
# from flask_cors import CORS  # Import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the model and scaler
# MODEL_PATH = './model/model.h5'
# SCALER_PATH = './model/scaler.pkl'
# model = load_model(MODEL_PATH)
# with open(SCALER_PATH, 'rb') as f:
#     scaler = pickle.load(f)

# # Create the Instaloader instance once
# loader = instaloader.Instaloader() 

# def extract_features_instaloader(username):
#     """
#     Extracts features from an Instagram profile using Instaloader.
#     """
#     try:
#         profile = instaloader.Profile.from_username(loader.context, username)

#         # Extract feature vector
#         profile_pic = 1 if profile.profile_pic_url else 0
#         nums_length_username = sum(c.isdigit() for c in profile.username) / len(profile.username)
#         fullname_words = len(profile.full_name.split())
#         nums_length_fullname = sum(c.isdigit() for c in profile.full_name) / max(len(profile.full_name), 1)
#         name_equals_username = 1 if profile.full_name.replace(" ", "").lower() == profile.username.lower() else 0
#         description_length = len(profile.biography)
#         external_url = 1 if profile.external_url else 0
#         is_private = 1 if profile.is_private else 0
#         num_posts = profile.mediacount
#         num_followers = profile.followers
#         num_follows = profile.followees

#         features = [
#             profile_pic,
#             nums_length_username,
#             fullname_words,
#             nums_length_fullname,
#             name_equals_username,
#             description_length,
#             external_url,
#             is_private,
#             num_posts,
#             num_followers,
#             num_follows,
#         ]

#         return features

#     except instaloader.exceptions.ProfileNotExistsException:
#         print("Error: Profile does not exist.")
#         return None
#     except Exception as e:
#         print(f"Error: {e}")
#         return None


# @app.route('/predict', methods=['POST'])  
# def predict():
#     try:
#         # Get username from the request
#         data = request.get_json()
#         username = data.get('username')

#         if not username:
#             return jsonify({'error': 'Username is required'}), 400

#         # Extract features using instaloader
#         features = extract_features_instaloader(username)

#         if not features:
#             return jsonify({'error': 'Failed to extract features'}), 500

#         # Apply the scaler before prediction
#         input_data = np.array(features).reshape(1, -1)  # Shape (1, 11)
#         scaled_input_data = scaler.transform(input_data)
        
#         prediction = model.predict(scaled_input_data)
#         fake_probability = float(prediction[0][0])  

#         # Return result as JSON
#         return jsonify({
#             'fake_probability': fake_probability,
#             'is_fake': fake_probability >= 0.5 
#         })

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)


# app.py
from flask import Flask, request, jsonify
import numpy as np
import instaloader
import pickle
from tensorflow.keras.models import load_model
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model and scaler
MODEL_PATH = './model/model.h5'
SCALER_PATH = './model/scaler.pkl'
model = load_model(MODEL_PATH)
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

# Create the Instaloader instance once
loader = instaloader.Instaloader() 

def extract_features_instaloader(username):
    """
    Extracts features and profile information from an 
    Instagram profile using Instaloader.
    """
    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        # Extract feature vector
        profile_pic = 1 if profile.profile_pic_url else 0
        nums_length_username = sum(c.isdigit() for c in profile.username) / len(profile.username)
        fullname_words = len(profile.full_name.split())
        nums_length_fullname = sum(c.isdigit() for c in profile.full_name) / max(len(profile.full_name), 1)
        name_equals_username = 1 if profile.full_name.replace(" ", "").lower() == profile.username.lower() else 0
        description_length = len(profile.biography)
        external_url = 1 if profile.external_url else 0
        is_private = 1 if profile.is_private else 0
        num_posts = profile.mediacount
        num_followers = profile.followers
        num_follows = profile.followees

        features = [
            profile_pic,
            nums_length_username,
            fullname_words,
            nums_length_fullname,
            name_equals_username,
            description_length,
            external_url,
            is_private,
            num_posts,
            num_followers,
            num_follows,
        ]

        # Extract profile information
        profile_info = {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "is_private": profile.is_private,
            "num_posts": profile.mediacount,
            "num_followers": profile.followers,
            "num_follows": profile.followees,
            "external_url": profile.external_url,
        }

        return features, profile_info

    except instaloader.exceptions.ProfileNotExistsException:
        print("Error: Profile does not exist.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


@app.route('/predict', methods=['POST'])  
def predict():
    try:
        # Get username from the request
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Extract features using instaloader
        features, profile_info = extract_features_instaloader(username)

        if not features:
            return jsonify({'error': 'Failed to extract features'}), 500

        # Apply the scaler before prediction
        input_data = np.array(features).reshape(1, -1)  # Shape (1, 11)
        scaled_input_data = scaler.transform(input_data)
        
        prediction = model.predict(scaled_input_data)
        fake_probability = float(prediction[0][0])  

        # Return result as JSON
        return jsonify({
            'fake_probability': fake_probability,
            'is_fake': fake_probability >= 0.5,  # Assuming 0.5 threshold for binary classification
            'profile_info': profile_info  # Include profile info in the response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)