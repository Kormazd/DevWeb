from flask import Flask
from flask_cors import CORS
from flask import Flask, request
import hashlib
from jwt_utils import build_token

ADMIN_PASSWORD = 'd278077bbfe7285a144d4b5b11adb9cf'

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
	payload = request.get_json()
	if not payload or 'password' not in payload:
		return 'Unauthorized', 401
	provided_password: str = str(payload.get('password', ''))
	provided_hash = hashlib.md5(provided_password.encode()).hexdigest()
	if provided_hash != ADMIN_PASSWORD:
		return 'Unauthorized', 401
	token = build_token()
	return {'token': token}, 200

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

if __name__ == "__main__":
    app.run(port=5001)


