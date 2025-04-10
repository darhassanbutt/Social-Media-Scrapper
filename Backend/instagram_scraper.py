from flask import Blueprint, jsonify, request
import http.client
import json
from firebase_config import save_to_firebase_instagram_userData,save_to_firebase_instagram_postData
from dotenv import load_dotenv
import os

instagram_blueprint = Blueprint('instagram', __name__)

# Load environment variables from .env file
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST_Instagram')


# Routes for User Data
@instagram_blueprint.route('/instagram/user/info', methods=['GET'])
def instagram_user_scrape():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    data = get_instagram_user(username)
    if data:
        save_to_firebase_instagram_userData(data, username, "user")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve user data"}), 500


@instagram_blueprint.route('/instagram/user/followers', methods=['GET'])
def instagram_followers_scrape():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    data = get_instagram_followers(username)
    if data:
        save_to_firebase_instagram_userData(data, username, "followers")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve followers data"}), 500


@instagram_blueprint.route('/instagram/user/following', methods=['GET'])
def instagram_followings_scrape():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    data = get_instagram_following(username)
    if data:
        save_to_firebase_instagram_userData(data, username, "following")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve following data"}), 500


@instagram_blueprint.route('/instagram/user/posts', methods=['GET'])
def instagram_posts_scrape():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    data = get_instagram_posts(username)
    if data:
        save_to_firebase_instagram_userData(data, username, "posts")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve posts and reels data"}), 500


@instagram_blueprint.route('/instagram/user/stories', methods=['GET'])
def instagram_stories_scrape():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    data = get_instagram_stories(username)
    if data:
        save_to_firebase_instagram_userData(data, username, "stories")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve stories data"}), 500


# Routes for Post Data
@instagram_blueprint.route('/instagram/post/info', methods=['GET'])
def instagram_post_info_scrape():
    post_id = request.args.get('url')
    
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400
    
    data = get_instagram_post_info(post_id)
    if data:
        save_to_firebase_instagram_postData(data, post_id, "post_info")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve post info"}), 500


@instagram_blueprint.route('/instagram/post/likes', methods=['GET'])
def instagram_post_likes_scrape():
    post_id = request.args.get('url')
    
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400
    
    data = get_instagram_post_likes(post_id)
    if data:
        save_to_firebase_instagram_postData(data, post_id, "post_likes")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve post likes"}), 500


@instagram_blueprint.route('/instagram/post/comments', methods=['GET'])
def instagram_post_comments_scrape():
    post_id = request.args.get('url')
    
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400
    
    data = get_instagram_post_comments(post_id)
    if data:
        save_to_firebase_instagram_postData(data, post_id, "post_comments")
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve post comments"}), 500


# Helper Functions for API Requests
def make_request_to_api(endpoint,x, identifier):
    conn = http.client.HTTPSConnection("instagram-scraper-api2.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    url = f"{endpoint}?{x}={identifier}"
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    if res.status == 200:
        data = res.read()
        return json.loads(data.decode("utf-8"))
    else:
        return None


# API Endpoints
def get_instagram_user(username):
    return make_request_to_api("/v1/info","username_or_id_or_url", username)


def get_instagram_followers(username):
    return make_request_to_api("/v1/followers","username_or_id_or_url", username)


def get_instagram_following(username):
    return make_request_to_api("/v1/following", "username_or_id_or_url",username)


def get_instagram_posts(username):
    return make_request_to_api("/v1.2/posts","username_or_id_or_url", username)


def get_instagram_stories(username):
    return make_request_to_api("/v1/stories", "username_or_id_or_url",username)


def get_instagram_post_info(post_id):
    return make_request_to_api("/v1/post_info", "code_or_id_or_url",post_id)


def get_instagram_post_likes(post_id):
    return make_request_to_api("/v1/likes","code_or_id_or_url" ,post_id)


def get_instagram_post_comments(post_id):
    return make_request_to_api("/v1/comments","code_or_id_or_url", post_id)
