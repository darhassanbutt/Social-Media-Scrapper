from flask import Blueprint, jsonify, request
import http.client
import json
from firebase_config import save_to_firebase_facebook
from dotenv import load_dotenv
import os

facebook_blueprint = Blueprint('facebook', __name__)

# Load environment variables from .env file
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST_Facebook')

@facebook_blueprint.route('/facebook', methods=['GET'])
def facebook_scrape():
    post_id = request.args.get('post_id')
    
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400
    
    data = get_facebook_data(post_id)
    if data:
        save_to_firebase_facebook(data,post_id,"post")  
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

def get_facebook_data(post_id):
    conn = http.client.HTTPSConnection("facebook-scraper3.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    conn.request("GET", f"/post?post_id={post_id}", headers=headers)

    res = conn.getresponse()
    if res.status == 200:
        data = res.read()
        return json.loads(data.decode("utf-8"))
    else:
        return None
