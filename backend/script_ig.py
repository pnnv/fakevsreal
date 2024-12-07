import instaloader
import requests
import re
import json

# Constants
API_URL = "http://127.0.0.1:5000/predict"  # The URL of your Flask app

def extract_features(username):
    """
    Extracts features from an Instagram profile using Instaloader.
    """
    loader = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(loader.context, username)

    # Extract additional profile info
    profile_info = {
        "Username": profile.username,
        "Full Name": profile.full_name,
        "Biography": profile.biography,
        "External URL": profile.external_url,
        "Private": profile.is_private,
        "Verified": profile.is_verified,
        "Business Account": profile.is_business_account,
        "Posts": profile.mediacount,
        "Followers": profile.followers,
        "Follows": profile.followees,
    }

    # Extract feature vector
    profile_pic = 1 if profile.profile_pic_url else 0  # 1 if profile picture exists, else 0
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

    return profile_info, features

def send_to_model(features):
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
        # Extract features and profile info
        profile_info, features = extract_features(username)
        display_profile_info(profile_info)  # Display all profile details
        display_features(features)  # Display the feature vector

        # Send features to the model for prediction
        print("\n=== Prediction ===")
        result = send_to_model(features)
        print(json.dumps(result, indent=4))  # Nicely format JSON output

    except instaloader.exceptions.ProfileNotExistsException:
        print("Error: Profile does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
