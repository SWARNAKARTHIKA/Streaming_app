from flask import Flask, render_template
import boto3
from botocore.exceptions import NoCredentialsError

# AWS S3 Config
S3_BUCKET = "swarnasoucdn"
S3_REGION = "ap-south-1"

app = Flask(__name__)

s3_client = boto3.client("s3")

@app.route("/")
def index():
    try:
        # List all songs in S3 bucket
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        songs = [file["Key"] for file in response.get("Contents", []) if file["Key"].endswith(".mp3")]
        
        # Generate public URLs
        song_urls = [f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{song}" for song in songs]
    except NoCredentialsError:
        song_urls = []

    return render_template("index.html", songs=song_urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
