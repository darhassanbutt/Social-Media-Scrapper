from flask import Blueprint, jsonify, request
import http.client
import json
from firebase_config import save_to_firebase_youtube_channelData, save_to_firebase_youtube_videoData
from dotenv import load_dotenv
import os
import json

youtube_blueprint = Blueprint('youtube', __name__)

# Load environment variables from .env file
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST_Youtube')


# Routes for Channel Data
@youtube_blueprint.route('/youtube/channel/info', methods=['GET'])
def youtube_channel_info_scrape():
    channel_id = request.args.get('id')
    if not channel_id:
        return jsonify({"error": "Channel ID is required"}), 400

    data = get_youtube_channel_info(channel_id)
    if data:
        save_to_firebase_youtube_channelData(data, channel_id, "channel_info")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve channel data"}), 500


@youtube_blueprint.route('/youtube/channel/videos', methods=['GET'])
def youtube_channel_videos_scrape():
    channel_id = request.args.get('id')
    if not channel_id:
        return jsonify({"error": "Channel ID is required"}), 400

    data = get_youtube_channel_videos(channel_id)
    if data:
        save_to_firebase_youtube_channelData(data, channel_id, "channel_videos")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve channel videos"}), 500


@youtube_blueprint.route('/youtube/channel/playlist', methods=['GET'])
def youtube_channel_playlist_scrape():
    channel_id = request.args.get('id')
    if not channel_id:
        return jsonify({"error": "Channel ID is required"}), 400

    data = get_youtube_channel_playlist(channel_id)
    if data:
        save_to_firebase_youtube_channelData(data, channel_id, "channel_playlist")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve playlists"}), 500


@youtube_blueprint.route('/youtube/channel/shorts', methods=['GET'])
def youtube_channel_shorts_scrape():
    channel_id = request.args.get('id')
    if not channel_id:
        return jsonify({"error": "Channel ID is required"}), 400

    data = get_youtube_channel_shorts(channel_id)
    if data:
        save_to_firebase_youtube_channelData(data, channel_id, "channel_shorts")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve shorts"}), 500


# Routes for Video Data
@youtube_blueprint.route('/youtube/video/info', methods=['GET'])
def youtube_video_info_scrape():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400

    data = get_youtube_video_info(video_id)
    if data:
        save_to_firebase_youtube_videoData(data, video_id, "video_info")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve video info"}), 500


@youtube_blueprint.route('/youtube/video/subtitle', methods=['GET'])
def youtube_video_subtitle_scrape():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({"error": "Video ID is required"}), 400

    data = get_youtube_video_subtitle(video_id)
    if data:
        save_to_firebase_youtube_videoData(data, video_id, "video_subtitle")
        return jsonify(data)
    return jsonify({"error": "Failed to retrieve subtitles"}), 500


# Helper Functions for API Requests
def make_request_to_api(endpoint, x, identifier):
    conn = http.client.HTTPSConnection("youtube-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }
    url = f"{endpoint}?{x}={identifier}"
    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    if res.status != 200:
        print(f"Error: {res.status}, {res.reason}")
        return None

    data = res.read()
    return json.loads(data.decode("utf-8"))


# API Endpoints


def get_youtube_channel_info(channel_id):
    
    data = make_request_to_api("/channel/about", "id", channel_id)

    if not data:
        return None

    # Filter and restructure the data
    filtered_data = {
        "channelId": data.get("channelId"),
        "channelHandle": data.get("channelHandle"),
        "title": data.get("title"),
        "description": data.get("description"),
         "country": data.get("country"),
         "joinedDate": data.get("joinedDate"),
         "subscriberCount": data.get("subscriberCount"),
         "viewCount": data.get("viewCount"),
         "videosCount": data.get("videosCount"),

        "avatarUrls": [item.get('url') for item in data.get('avatar', []) if 'url' in item],
        "bannerUrls": [item.get('url') for item in data.get('banner', []) if 'url' in item],
        "keywords" : data.get("keywords",[]),
           
        "links": [{
          "title":link.get("title"),
          "link":link.get("link")
           } for link in data.get('links',[])] ,
    }


    return filtered_data

def get_youtube_channel_videos(channel_id):
    return make_request_to_api("/channel/videos", "id", channel_id)

def get_youtube_channel_playlist(channel_id):
    return make_request_to_api("/channel/playlists", "id", channel_id)

def get_youtube_channel_shorts(channel_id):
    return make_request_to_api("/channel/shorts", "id", channel_id)

def get_youtube_video_info(video_id):
    return make_request_to_api("/video/info", "id", video_id)

def get_youtube_video_subtitle(video_id):
    return make_request_to_api("/subtitles", "id", video_id)
