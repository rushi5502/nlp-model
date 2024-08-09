from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from mongodb_connection import get_db
import logging
from skills_extractor import extract_text_from_pdf, extract_skills_from_text, match_skills  # Import functions
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def convert_object_ids(obj):
    """Recursively convert ObjectId fields to strings."""
    if isinstance(obj, dict):
        return {key: convert_object_ids(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_object_ids(element) for element in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

def calculate_match_percentage(matched_skills, required_skills):
    """Calculate the percentage of matched skills."""
    if not required_skills:
        return 0
    return (len(matched_skills) / len(required_skills)) * 100

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/post/<postId>', methods=['GET'])
def get_post_by_id(postId):
    try:
        db = get_db()
        if db is None:
            logging.error('Database connection failed')
            return jsonify({'error': 'Database connection failed'}), 500
        
        # Log the received postId
        logging.debug(f'Received postId: {postId}')
        
        # Check if postId is a valid 24-character hexadecimal string
        if len(postId) != 24:
            logging.error('Invalid post ID length')
            return jsonify({'error': 'Invalid post ID length'}), 400
        
        try:
            post_id_obj = ObjectId(postId)
        except Exception as e:
            logging.error('Invalid post ID format')
            return jsonify({'error': 'Invalid post ID format'}), 400
        
        # Fetch the post from the database
        post = db['Post'].find_one({'_id': post_id_obj})
        
        if post is None:
            logging.info('Post not found')
            return jsonify({'error': 'Post not found'}), 404
        
        # Convert ObjectId to string for JSON serialization
        post = convert_object_ids(post)
        
        # Fetch applications associated with the post
        applications_cursor = db['Application'].find({'postId': post_id_obj})
        applications = list(applications_cursor)
        
        # Convert ObjectId fields in applications to strings
        applications = convert_object_ids(applications)
        
        # Extract required skills from the post
        required_skills = post.get('requiredSkills', [])
        
        # Extract resume URLs from applications
        resume_urls = [application.get('resumeUrl') for application in applications]
        
        # Extract skills from each resume and match with required skills
        resume_skills = {}
        matched_skills_per_resume = {}
        for application in applications:
            resume_url = application.get('resumeUrl')
            if resume_url:
                text = extract_text_from_pdf(resume_url)
                skills = extract_skills_from_text(text)
                resume_skills[resume_url] = skills
                
                # Match skills with the required skills for the post
                matched_skills = match_skills(skills, required_skills)
                matched_skills_per_resume[resume_url] = matched_skills
                
                # Calculate match percentage
                match_percentage = round(calculate_match_percentage(matched_skills, required_skills), 2)
                print(type(match_percentage))
                print(match_percentage)
                db['Application'].update_one(
                    {'resumeUrl': resume_url},
                    {'$set': {'matchPercentage': match_percentage}}
                )
        
        return jsonify({
            'post': post,
            'applications': applications,
            'requiredSkills': required_skills,
            'resumeSkills': resume_skills,
            'matchedSkillsPerResume': matched_skills_per_resume
        }), 200

    except Exception as e:
        logging.error(f'Error fetching post: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the app on the port provided by Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
