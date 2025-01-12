from flask import Flask, request, send_file, render_template_string, redirect, url_for, jsonify
import os
import secrets
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import socket
from pyngrok import ngrok, conf
import logging
import configparser
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_default_config():
    """Create default configuration file if it doesn't exist"""
    if not os.path.exists('config.ini') and os.path.exists('config.template.ini'):
        shutil.copy('config.template.ini', 'config.ini')
        logger.info("Created default config.ini file. Please edit it with your ngrok auth token.")
        return False
    return True

def load_config():
    """Load configuration from config.ini"""
    if not os.path.exists('config.ini'):
        create_default_config()
        return None
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

def setup_ngrok(config):
    """Setup ngrok with the provided configuration"""
    if not config or 'ngrok' not in config:
        logger.error("Configuration file is missing or invalid")
        return False

    auth_token = config['ngrok'].get('auth_token', '').strip()
    if auth_token == '' or auth_token == 'your_auth_token_here':
        logger.error("Please set your ngrok auth token in config.ini")
        return False

    try:
        conf.get_default().auth_token = auth_token
        return True
    except Exception as e:
        logger.error(f"Error configuring ngrok: {str(e)}")
        return False

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configuration
UPLOAD_FOLDER = 'uploads'
METADATA_FILE = 'file_metadata.json'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template for the upload form
UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .btn { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h2>Upload File</h2>
    <form method="post" enctype="multipart/form-data">
        <div class="form-group">
            <input type="file" name="file" required>
        </div>
        <button type="submit" class="btn">Upload</button>
    </form>
    {% if message %}
    <div class="result">
        <h3>File Uploaded Successfully!</h3>
        <p>Access Link: {{ message.link }}</p>
        <p>Access Key: {{ message.key }}</p>
        <p>Share these with the person you want to share the file with.</p>
    </div>
    {% endif %}
</body>
</html>
'''

# HTML template for accessing files
ACCESS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Access File</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        .btn { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>Access File</h2>
    <form method="post">
        <div class="form-group">
            <label>Access Key:</label>
            <input type="text" name="key" required>
        </div>
        <button type="submit" class="btn">Access File</button>
    </form>
    {% if error %}
    <p class="error">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

def load_metadata():
    """Load file metadata from JSON file"""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_metadata(metadata):
    """Save file metadata to JSON file"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)

def get_public_ip():
    """Get the public IP address of the server"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "localhost"

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        # Start ngrok tunnel
        public_url = ngrok.connect(5000).public_url
        logger.info(f"ngrok tunnel started at: {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Error starting ngrok: {str(e)}")
        return None

def get_public_url():
    """Get the public URL for the server"""
    try:
        tunnels = ngrok.get_tunnels()
        if tunnels:
            return tunnels[0].public_url
        return None
    except:
        return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file:
            # Generate unique filename and access key
            filename = secure_filename(file.filename)
            file_id = secrets.token_urlsafe(8)
            access_key = secrets.token_urlsafe(16)
            
            # Save file
            safe_filename = f"{file_id}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, safe_filename))
            
            # Save metadata
            metadata = load_metadata()
            metadata[file_id] = {
                'filename': filename,
                'access_key': access_key,
                'upload_time': datetime.now().isoformat(),
                'safe_filename': safe_filename
            }
            save_metadata(metadata)
            
            # Generate access link using ngrok public URL
            public_url = get_public_url()
            if not public_url:
                return jsonify({'error': 'Could not generate public URL'}), 500
                
            access_link = f"{public_url}/access/{file_id}"
            
            if request.headers.get('Accept') == 'application/json':
                return jsonify({
                    'link': access_link,
                    'key': access_key
                })
            
            return render_template_string(UPLOAD_TEMPLATE, 
                message={'link': access_link, 'key': access_key})
    
    return render_template_string(UPLOAD_TEMPLATE, message=None)

@app.route('/access/<file_id>', methods=['GET', 'POST'])
def access_file(file_id):
    metadata = load_metadata()
    if file_id not in metadata:
        return 'File not found', 404
    
    if request.method == 'POST':
        access_key = request.form.get('key')
        if access_key == metadata[file_id]['access_key']:
            filename = metadata[file_id]['safe_filename']
            return send_file(
                os.path.join(UPLOAD_FOLDER, filename),
                as_attachment=True,
                download_name=metadata[file_id]['filename']
            )
        return render_template_string(ACCESS_TEMPLATE, error='Invalid access key')
    
    return render_template_string(ACCESS_TEMPLATE)

if __name__ == '__main__':
    # Load configuration
    config = load_config()
    if not config:
        logger.error("Please configure your ngrok auth token in config.ini")
        exit(1)

    # Setup ngrok
    if not setup_ngrok(config):
        logger.error("Failed to setup ngrok. Please check your configuration.")
        exit(1)

    # Start ngrok tunnel
    try:
        port = config['server'].getint('port', 5000)
        public_url = ngrok.connect(port).public_url
        logger.info(f"Server is publicly accessible at: {public_url}")
        
        # Set maximum content length from config
        max_size = config['server'].getint('max_file_size', 16)
        app.config['MAX_CONTENT_LENGTH'] = max_size * 1024 * 1024  # Convert MB to bytes
        
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        exit(1)
