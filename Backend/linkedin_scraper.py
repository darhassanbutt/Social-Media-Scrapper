from flask import Blueprint, jsonify, request
import http.client
import json
from firebase_config import save_to_firebase_linkedinData
from dotenv import load_dotenv
import os
import urllib.parse 

linkedin_blueprint = Blueprint('linkedin', __name__)

# Load environment variables from .env file
load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST_Linkedin')


@linkedin_blueprint.route('/linkedin', methods=['GET'])
def linkedin_scrape():
    url = request.args.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    data = get_linkedin_data(url)
    if data:
        save_to_firebase_linkedinData(data,url,"personalData")  
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

def get_linkedin_data(url):
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")
    encoded_url = urllib.parse.quote(url)
    print(RAPIDAPI_HOST,RAPIDAPI_KEY)
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    conn.request("GET", f"/get-linkedin-profile?linkedin_url={encoded_url}&include_skills=false&include_certifications=false&include_publications=false&include_honors=false&include_volunteers=false&include_projects=false&include_patents=false&include_courses=false&include_organizations=false&include_profile_status=false&include_company_public_url=false", headers=headers)
    
    res = conn.getresponse()
    if res.status == 200:
        data = res.read()
        return json.loads(data.decode("utf-8"))
    else:
        return None
