from flask import Flask
from instagram_scraper import instagram_blueprint
from facebook_scraper import facebook_blueprint
from linkedin_scraper import linkedin_blueprint
from youtube_scraper import youtube_blueprint
from export import export_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.register_blueprint(instagram_blueprint, url_prefix='/scraper')
app.register_blueprint(facebook_blueprint, url_prefix='/scraper')
app.register_blueprint(linkedin_blueprint, url_prefix='/scraper')
app.register_blueprint(youtube_blueprint, url_prefix='/scraper')
app.register_blueprint(export_blueprint, url_prefix='/export')

if __name__ == "__main__":
    app.run(debug=True)
