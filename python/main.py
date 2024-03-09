from flask import Flask, request, jsonify
from functools import wraps
from psycopg import connect
from post import post_data
from get import get_data
import os

app = Flask(__name__)

def get_db_connection():
    conn = connect(f"host={os.getenv('DATABASE_HOST')} \
                            dbname={os.getenv('DATABASE_NAME')} \
                            user={os.getenv('DATABASE_USER')} \
                            password={os.getenv('DATABASE_PASSWORD')}")
    return conn


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if auth_header:
            if auth_header == f"Bearer {os.getenv('VALID_TOKEN')}": 
                return f(*args, **kwargs)
            else:
                return jsonify({"error": "Unauthorized access, invalid token."}), 401
        else:
             return jsonify({"error": "Authorization token is missing."}), 401
        
    return decorated_function


@app.route('/api/resume/get', methods=['GET'])
def get():
    return get_data(get_db_connection())


@app.route('/api/resume/update', methods=['POST'])
@token_required
def post():
    contact = request.json.get('contact', {})
    education = request.json.get('education', [])
    work_experience = request.json.get('work_experience', [])
    skills = request.json.get('skills', {})
    projects = request.json.get('projects', [])
    certifications = request.json.get('certifications', [])

    return post_data(get_db_connection(), contact, education, work_experience, skills, projects, certifications)

    
if __name__ == '__main__':
    app.run(debug=True)
