from flask import Flask, request, render_template, send_file
import boto3
import os

app = Flask(__name__)

# AWS S3 configuration
S3_BUCKET_NAME = 'your-bucket-name'
S3_ACCESS_KEY = 'your-access-key-id'
S3_SECRET_KEY = 'your-secret-key-id'
S3_REGION = 'your-aws-region'

@app.route('/')
def index():
    return render_template('code.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Extracting user data from the form
    user_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'message': request.form['message']
    }

    # Write user data to a text file
    filename = 'user_data.txt'
    with open(filename, 'w') as file:
        file.write(f"Name: {user_data['name']}\nEmail: {user_data['email']}\nMessage: {user_data['message']}")

    # Upload file to S3
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)
    s3_client.upload_file(filename, S3_BUCKET_NAME, filename)

    # Delete the local file
    os.remove(filename)

    return render_template('code2.html')

@app.route('/download')
def download():
    # Download file from S3
    filename = 'user_data.txt'
    s3_client = boto3.client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY, region_name=S3_REGION)
    s3_client.download_file(S3_BUCKET_NAME, filename, filename)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
