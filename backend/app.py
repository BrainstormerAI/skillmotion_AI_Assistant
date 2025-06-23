import os
import json
import asyncio
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import tempfile
import threading
from resume_parser import ResumeParser
from llm_query import LLMQuery
from tts import TTSGenerator

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize components
resume_parser = ResumeParser()
llm_query = LLMQuery()
tts_generator = TTSGenerator()

# Load configuration
with open('config/prompts.json', 'r') as f:
    config = json.load(f)

@app.route('/')
def health_check():
    return jsonify({"status": "Skillmotion AI Assistant Backend Running"})

@app.route('/api/welcome', methods=['GET'])
async def get_welcome_message():
    """Get welcome message and generate TTS audio"""
    try:
        welcome_text = config['welcome_message']
        options = config['options']
        
        # Generate TTS audio
        audio_path = await tts_generator.generate_speech(welcome_text)
        
        return jsonify({
            "message": welcome_text,
            "options": options,
            "audio_url": f"/api/audio/{os.path.basename(audio_path)}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        audio_path = os.path.join('temp_audio', filename)
        return send_file(audio_path, mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/upload-resume', methods=['POST'])
async def upload_resume():
    """Handle resume upload and initial processing"""
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            file.save(tmp_file.name)
            
            # Parse resume
            resume_text = resume_parser.extract_text_from_pdf(tmp_file.name)
            
            # Extract skills using LLM
            skills_prompt = config['prompts']['skill_extraction'].format(
                resume_text=resume_text
            )
            extracted_skills = await llm_query.query_llm(skills_prompt)
            
            # Clean up temp file
            os.unlink(tmp_file.name)
            
            return jsonify({
                "resume_text": resume_text,
                "extracted_skills": extracted_skills,
                "status": "success"
            })
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-resume', methods=['POST'])
async def analyze_resume():
    """Perform comprehensive resume analysis for a specific job role"""
    try:
        data = request.get_json()
        
        if not data or 'job_role' not in data or 'extracted_skills' not in data:
            return jsonify({"error": "Missing required data"}), 400
        
        job_role = data['job_role'].lower().replace(' ', '_')
        extracted_skills = data['extracted_skills']
        
        # Get required skills for the job role
        required_skills = config['job_skills_database'].get(
            job_role, 
            ["General professional skills", "Communication", "Problem solving", "Teamwork"]
        )
        
        # Perform gap analysis
        gap_analysis_prompt = config['prompts']['gap_analysis'].format(
            job_role=data['job_role'],
            current_skills=extracted_skills,
            required_skills=', '.join(required_skills)
        )
        
        gap_analysis = await llm_query.query_llm(gap_analysis_prompt)
        
        # Generate learning plan
        learning_plan_prompt = config['prompts']['learning_plan'].format(
            skill_gaps=gap_analysis,
            current_level="Mid-level",  # This could be enhanced with user input
            target_role=data['job_role']
        )
        
        learning_plan = await llm_query.query_llm(learning_plan_prompt)
        
        # Generate TTS for the analysis
        analysis_text = f"Based on your resume analysis for the {data['job_role']} position, here's what I found: {gap_analysis[:200]}... I've also created a personalized learning plan for you."
        audio_path = await tts_generator.generate_speech(analysis_text)
        
        return jsonify({
            "gap_analysis": gap_analysis,
            "learning_plan": learning_plan,
            "required_skills": required_skills,
            "analysis_summary": analysis_text,
            "audio_url": f"/api/audio/{os.path.basename(audio_path)}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
async def chat():
    """Handle general chat interactions"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message']
        context = data.get('context', '')
        
        # Determine intent and generate appropriate response
        response_text = await llm_query.query_llm(
            f"Context: {context}\nUser Query: {user_message}\n\nProvide a helpful response as an AI career development assistant."
        )
        
        # Generate TTS
        audio_path = await tts_generator.generate_speech(response_text)
        
        return jsonify({
            "response": response_text,
            "audio_url": f"/api/audio/{os.path.basename(audio_path)}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/skill-profile', methods=['POST'])
async def create_skill_profile():
    """Create a comprehensive skill profile"""
    try:
        data = request.get_json()
        
        profile_prompt = config['prompts']['skill_profile'].format(
            background=data.get('background', ''),
            experience=data.get('experience', ''),
            goals=data.get('goals', '')
        )
        
        skill_profile = await llm_query.query_llm(profile_prompt)
        
        # Generate TTS
        summary_text = f"I've created your skill profile. Here's a summary of your current capabilities and development recommendations."
        audio_path = await tts_generator.generate_speech(summary_text)
        
        return jsonify({
            "skill_profile": skill_profile,
            "audio_url": f"/api/audio/{os.path.basename(audio_path)}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask_app():
    """Run Flask app in a separate thread"""
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

if __name__ == '__main__':
    run_flask_app()