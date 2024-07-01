import hashlib
import hmac
import requests
import time
import uuid
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def generate_hmac_base64(message, secret_key):
    key = bytes(secret_key, 'utf-8')
    data = bytes(message, 'utf-8')
    h = hmac.new(key, data, hashlib.sha512)
    hash_result = h.digest()
    return base64.b64encode(hash_result).decode('utf-8')


# API details
api_secret = os.getenv('API_SECRET')
client_id = os.getenv("CLIENT_ID")
salt = os.getenv("SALT")
url = os.getenv("API_URL")
timestamp = str(int(time.time()))

# Example usage:
message = F"POST{client_id}{timestamp}{salt}"
hmac_base64 = generate_hmac_base64(message, api_secret)
print("Generated HMAC (Base64):", hmac_base64)




# Generate a unique request ID
request_id = uuid.uuid4().hex[:16]  # Generate a random 16-character alphanumeric string

# Current timestamp in Unix format
file_path = "/home/choice/Desktop/chatbot-components/audio_calls/53501fef-ef8b-4a08-b171-bcd7846ea639.mp3"

# Create Form-data payload
files = {
    'file': open(file_path, 'rb'),  # Replace with your audio file path
}
data = {
    'requestId': request_id,
}

# Prepare the canonical string
# canonical_string = f'POSTCT0001{timestamp}MgQ6CJOQAk1zwJX9'
# canonical_string = "POSTCT00011718779504MgQ6CJOQAk1zwJX9"

# Generate HMAC signature
# signature = hmac.new(
#     bytes(api_secret, 'utf-8'),
#     bytes(canonical_string, 'utf-8'),
#     hashlib.sha256
# ).hexdigest()

# Prepare headers with HMAC authentication
headers = {
    'X-Client-ID': client_id,
    'X-Signature': hmac_base64,
    'X-Timestamp': timestamp,
    'Content-Type': 'multipart/form-data',  # Specify Content-Type for Form-data
}

# Make the POST request
response = requests.post(url, headers=headers, files=files, data=data)

# Handle the response
if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.status_code, response.text)
