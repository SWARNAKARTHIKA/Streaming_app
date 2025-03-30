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
        song_urls = [s3_client.generate_presigned_url('get_object',
                                              Params={'Bucket': S3_BUCKET, 'Key': song},
                                              ExpiresIn=3600) for song in songs]

    except NoCredentialsError:
        song_urls = []

    return render_template("index.html", songs=song_urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
