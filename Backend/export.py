from flask import Flask, Response
import firebase_admin
from firebase_admin import credentials, firestore
import csv
import io
from flask import Blueprint, jsonify, request
from firebase_config import db

export_blueprint = Blueprint('export', __name__)

def export_collection_to_csv(collection_name, filename):
    try:
        # Fetch data from Firestore
        docs = db.collection(collection_name).stream()

        # Prepare CSV data in-memory
        csv_buffer = io.StringIO()
        writer = None
        for doc in docs:
            doc_data = doc.to_dict()
            doc_data['id'] = doc.id  # Include document ID

            # Write headers (keys) only once
            if writer is None:
                writer = csv.DictWriter(csv_buffer, fieldnames=doc_data.keys())
                writer.writeheader()
            writer.writerow(doc_data)

        # Return CSV file as a response
        csv_buffer.seek(0)
        response = Response(
            csv_buffer.getvalue(),
            mimetype='text/csv',
            content_type='application/csv'
        )
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    except Exception as e:
        return {"error": str(e)}, 500

# Instagram Endpoint
@export_blueprint.route('/exportinstagram', methods=['GET'])
def export_instagram_csv():
    return export_collection_to_csv('instagram_data', 'instagram_data.csv')

# Facebook Endpoint
@export_blueprint.route('/exportfacebook', methods=['GET'])
def export_facebook_csv():
    return export_collection_to_csv('facebook_data', 'facebook_data.csv')

# YouTube Endpoint
@export_blueprint.route('/exportyoutube', methods=['GET'])
def export_youtube_csv():
    return export_collection_to_csv('youtube_data', 'youtube_data.csv')

# LinkedIn Endpoint
@export_blueprint.route('/exportlinkedin', methods=['GET'])
def export_linkedin_csv():
    return export_collection_to_csv('linkedin_data', 'linkedin_data.csv')
