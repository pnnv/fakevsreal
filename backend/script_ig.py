import instaloader
import requests
import numpy as np  
import json
import time

# Constants
API_URL = "http://127.0.0.1:5000/predict"  # URL of your Flask app

def extract_features_instaloader(username):  # Renamed function
    """
    Extracts features from an Instagram profile using Instaloader.
    """
    loader = instaloader.Instaloader()

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

        return features

    except instaloader.exceptions.ProfileNotExistsException:
        print("Error: Profile does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def send_to_model(features):  # Modified to send features
    """
    Sends the features to the Flask backend for prediction.
    """
    payload = {"features": features}
    response = requests.post(API_URL, json=payload)
    return response.json()

def display_profile_info(profile_info):
    """
    Nicely display all the profile information.
    """
    print("\n=== Instagram Profile Information ===")
    for key, value in profile_info.items():
        print(f"{key}: {value}")

def display_features(features):
    """
    Display the feature vector.
    """
    feature_labels = [
        "Profile Picture",
        "Numbers/Length of Username",
        "Full Name Words",
        "Numbers/Length of Full Name",
        "Name Equals Username",
        "Description Length",
        "External URL",
        "Private",
        "Number of Posts",
        "Number of Followers",
        "Number of Follows",
    ]

    print("\n=== Feature Vector ===")
    for label, value in zip(feature_labels, features):
        print(f"{label}: {value}")

def main():
    username = input("Enter Instagram username: ")
    try:
        # Extract features using the renamed function
        features = extract_features_instaloader(username)

        if features:
            # Display the feature vector
            display_features(features)

            # Send features to the model for prediction
            print("\n=== Prediction ===")
            result = send_to_model(features)  # Send features to the API
            print(json.dumps(result, indent=4))  # Nicely format JSON output

            # Add a delay to avoid rate limiting (adjust as needed)
            time.sleep(2)

    except instaloader.exceptions.ProfileNotExistsException:
        print("Error: Profile does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()

# import instaloader
# import requests
# import re
# import json
# import time

# # Constants
# API_URL = "http://127.0.0.1:5000/analyze"  # The URL of your Flask app


# def extract_features_instaloader(username):  # Renamed function
#     """
#     Extracts features from an Instagram profile using Instaloader.
#     """
#     loader = instaloader.Instaloader()

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


# def send_to_model(username):
#     """
#     Sends the username to the Flask backend for analysis and prediction.
#     """
#     payload = {"username": username}  # Send only the username
#     response = requests.post(API_URL, json=payload)
#     return response.json()


# def display_profile_info(profile_info):
#     """
#     Nicely display all the profile information.
#     """
#     print("\n=== Instagram Profile Information ===")
#     for key, value in profile_info.items():
#         print(f"{key}: {value}")


# def display_features(features):
#     """
#     Display the feature vector.
#     """
#     feature_labels = [
#         "Profile Picture",
#         "Numbers/Length of Username",
#         "Full Name Words",
#         "Numbers/Length of Full Name",
#         "Name Equals Username",
#         "Description Length",
#         "External URL",
#         "Private",
#         "Number of Posts",
#         "Number of Followers",
#         "Number of Follows",
#     ]

#     print("\n=== Feature Vector ===")
#     for label, value in zip(feature_labels, features):
#         print(f"{label}: {value}")


# def main():
#     username = input("Enter Instagram username: ")
#     try:
#         # Extract features using the renamed function
#         features = extract_features_instaloader(username)

#         if features:
#             # Display the feature vector
#             display_features(features)

#             # Send the username to the /analyze endpoint for prediction
#             print("\n=== Prediction ===")
#             result = send_to_model(
#                 username)  # Send username to the API
#             print(json.dumps(result, indent=4))  # Nicely format JSON output

#             # Add a delay to avoid rate limiting (adjust as needed)
#             time.sleep(2)

#     except instaloader.exceptions.ProfileNotExistsException:
#         print("Error: Profile does not exist.")
#     except Exception as e:
#         print(f"Error: {str(e)}")


# if __name__ == "__main__":
#     main()