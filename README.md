# 🧠 Skillmotion.AI Assistant

A comprehensive voice-enabled virtual assistant for AI-powered skill development and career analytics. This full-stack application combines advanced AI capabilities with an intuitive interface to provide personalized career guidance, skill gap analysis, and learning recommendations.

## ✨ Features

### 🎤 Voice-First Interaction
- **Voice Commands**: Natural language processing for hands-free interaction
- **Text-to-Speech**: All responses are converted to speech using edge-tts
- **Multi-Modal Input**: Support for voice, text, and click interactions
- **Real-time Audio Feedback**: Immediate voice responses to user queries

### 📄 Resume Analysis
- **PDF Processing**: Advanced resume parsing using PyMuPDF and pdfminer.six
- **Skill Extraction**: AI-powered skill identification and categorization
- **Gap Analysis**: Compare your skills against job requirements
- **Personalized Recommendations**: Tailored learning paths and career advice

### 🤖 AI-Powered Intelligence
- **Dual LLM Support**: Integration with both Groq and OpenAI APIs
- **Intelligent Prompting**: Configuration-driven prompt chains for consistent results
- **Context Awareness**: Maintains conversation context for better responses
- **Skill Profiling**: Comprehensive skill assessment and profiling

### 🎯 Career Services
- **Skill Profile Creation**: Build detailed professional skill inventories
- **Gap Analysis**: Identify areas for professional development
- **Learning Plans**: Generate personalized 90-day development roadmaps
- **Assessment Tools**: Evaluate current capabilities and growth areas
- **Job Role Matching**: Analyze fitness for specific positions

## 🏗 Architecture

### Frontend (Single-File Architecture)
- **Pure Web Technologies**: HTML5, CSS3, and Vanilla JavaScript
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **Web Speech API**: Native browser voice recognition
- **Real-time Communication**: Seamless backend integration
- **Progressive Enhancement**: Works across all modern browsers

### Backend (Python/Flask)
- **Modular Design**: Clean separation of concerns
- **Async Processing**: Non-blocking operations for better performance
- **File Processing**: Safe handling of PDF uploads and processing
- **API Integration**: Robust LLM service integration with fallbacks
- **Audio Generation**: Server-side TTS using edge-tts

### Configuration-Driven
- **JSON Configuration**: Easy modification of prompts and workflows
- **Skill Database**: Extensible job role and skill mappings
- **Environment Variables**: Secure API key management
- **Modular Prompts**: Reusable prompt templates for different scenarios

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ 
- Modern web browser with speech recognition support
- API keys for Groq and/or OpenAI

### Installation

1. **Clone and Setup**:
```bash
git clone <repository-url>
cd skillmotion_ai_assistant
pip install -r requirements.txt
```

2. **Environment Configuration**:
Create a `.env` file with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

3. **Launch Application**:
```bash
python run.py
```

4. **Access the Application**:
- Frontend: http://localhost:8080
- Backend API: http://localhost:5000
- The application will automatically open both services

## 📁 Project Structure

```
skillmotion_ai_assistant/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── resume_parser.py    # PDF processing and text extraction
│   ├── llm_query.py       # LLM integration and query management
│   └── tts.py             # Text-to-speech generation
├── frontend/
│   └── index.html         # Complete single-file frontend
├── config/
│   └── prompts.json       # AI prompts and configuration
├── temp_audio/            # Generated audio files (auto-created)
├── run.py                 # Application launcher with threading
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (user-created)
└── README.md             # This file
```

## 🎯 Usage Guide

### Basic Interaction
1. **Welcome**: The assistant greets you with available options
2. **Voice Input**: Click the microphone button and speak naturally
3. **Text Input**: Type messages in the chat interface
4. **Service Selection**: Click on service cards or speak your choice

### Resume Analysis Workflow
1. **Upload Resume**: Drag & drop or click to upload PDF resume
2. **Job Role Input**: Specify your target position
3. **AI Analysis**: Receive comprehensive skill gap analysis
4. **Learning Plan**: Get personalized development recommendations
5. **Audio Feedback**: Listen to analysis summary and recommendations

### Available Services
- **Skill Profile Creation**: Comprehensive professional assessment
- **Gap Analysis**: Compare current vs. required skills
- **Content Planning**: Personalized learning roadmaps
- **Assessments**: Skill evaluation and testing
- **Resume Analysis**: CV optimization for specific roles

## 🔧 Configuration

### Prompts and Workflows
Edit `config/prompts.json` to customize:
- AI response templates
- Job role skill databases
- Analysis workflows
- Welcome messages and options

### Adding New Job Roles
Add entries to the `job_skills_database` in `prompts.json`:
```json
"new_role": [
  "Required Skill 1",
  "Required Skill 2",
  "Required Skill 3"
]
```

### Voice Configuration
Modify voice settings in the TTS component:
- Voice selection (male/female/neutral)
- Speech rate and volume
- Language and accent options

## 🛠 Technical Details

### Dependencies
- **Flask**: Web framework and API server
- **PyMuPDF/pdfminer.six**: PDF processing
- **edge-tts**: Text-to-speech generation
- **Groq/OpenAI**: LLM service integration
- **python-dotenv**: Environment management

### Browser Requirements
- Modern browser (Chrome, Firefox, Safari, Edge)
- Microphone access for voice input
- Audio playback capability
- File upload support

### Performance Optimization
- Async audio generation
- File caching for TTS
- Threaded server execution
- Efficient PDF processing
- Response streaming

## 🔐 Security

### API Key Management
- Environment variable storage
- No hardcoded credentials
- Secure key rotation support

### File Processing
- Safe PDF handling
- Temporary file cleanup
- Input validation and sanitization
- Error handling and recovery

### Network Security
- CORS configuration
- Request validation
- Rate limiting ready
- SSL/TLS support ready

## 🚀 Deployment

### Local Development
- Use `python run.py` for local testing
- Both servers run automatically
- Hot reload for development

### Production Deployment
- Configure proper WSGI server (gunicorn)
- Set up reverse proxy (nginx)
- Enable SSL/TLS certificates
- Configure environment variables
- Set up monitoring and logging

## 📈 Future Enhancements

### Planned Features
- Multi-language support with Google Translate
- Advanced analytics and reporting
- Integration with job boards and career platforms
- Mobile application companion
- Team collaboration features
- Advanced assessment algorithms

### Technical Roadmap
- Docker containerization
- Cloud deployment options
- Database integration for user data
- Advanced caching mechanisms
- API versioning and documentation
- Performance monitoring and optimization

## 🤝 Contributing

We welcome contributions! Please see our contribution guidelines for:
- Code style and standards
- Testing requirements
- Documentation updates
- Feature requests and bug reports

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋‍♂️ Support

For support, questions, or feedback:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

---

**Made with ❤️ for career development and AI-powered learning**