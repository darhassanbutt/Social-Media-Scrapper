import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Initialization
cred = credentials.Certificate('social-scraper-b4a9a-firebase-adminsdk-xm3m7-56738d584a.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def save_to_firebase_instagram_userData(data,id,type):
    db.collection("instagram_userData").document(f"{id}_{type}").set(data)

def save_to_firebase_instagram_postData(data,id,type):
    db.collection("instagram_postData").document(f"{id}_{type}").set(data)

def save_to_firebase_youtube_channelData(data,id,type):
    db.collection("youtube_channelData").document(f"{id}_{type}").set(data)

def save_to_firebase_youtube_videoData(data,id,type):
    db.collection("youtube_videoData").document(f"{id}_{type}").set(data)

def save_to_firebase_linkedinData(data,id,type):
    db.collection("linkedin_ProfileData").document(f"{id}_{type}").set(data)

def save_to_firebase_facebook(data,id,type):
    db.collection("facebook_data").document(f"{id}_{type}").set(data)
