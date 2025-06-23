#!/usr/bin/env python3
"""
Skillmotion AI Assistant Runner
Starts both frontend and backend servers using threading
"""

import threading
import time
import os
import sys
import signal
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from pathlib import Path

class FrontendServer:
    def __init__(self, port=8080, directory="frontend"):
        self.port = port
        self.directory = directory
        self.server = None
        
    def run(self):
        """Run the frontend server"""
        try:
            # Change to frontend directory
            os.chdir(self.directory)
            
            # Create HTTP server
            handler = SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                self.server = httpd
                print(f"🌐 Frontend server running at http://localhost:{self.port}")
                httpd.serve_forever()
        except Exception as e:
            print(f"❌ Frontend server error: {e}")
    
    def stop(self):
        """Stop the frontend server"""
        if self.server:
            self.server.shutdown()

class BackendServer:
    def __init__(self):
        self.process = None
    
    def run(self):
        """Run the backend server"""
        try:
            # Change to backend directory
            backend_path = Path("backend")
            if backend_path.exists():
                os.chdir(backend_path)
            
            # Import and run Flask app
            from backend.app import run_flask_app
            print("🚀 Backend server starting...")
            run_flask_app()
            
        except ImportError:
            # Fallback: run as subprocess
            try:
                self.process = subprocess.Popen([
                    sys.executable, "-m", "backend.app"
                ], cwd=os.getcwd())
                print("🚀 Backend server started as subprocess")
                self.process.wait()
            except Exception as e:
                print(f"❌ Backend server error: {e}")
        except Exception as e:
            print(f"❌ Backend server error: {e}")
    
    def stop(self):
        """Stop the backend server"""
        if self.process:
            self.process.terminate()

class SkillmotionRunner:
    def __init__(self):
        self.frontend_server = FrontendServer()
        self.backend_server = BackendServer()
        self.threads = []
        self.running = True
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            print("\n🛑 Shutting down Skillmotion AI Assistant...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        required_packages = [
            'flask', 'flask-cors', 'python-dotenv', 
            'PyMuPDF', 'pdfminer.six', 'requests', 
            'edge-tts', 'groq', 'openai'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                # Handle special cases
                if package == 'PyMuPDF':
                    try:
                        __import__('fitz')
                    except ImportError:
                        missing_packages.append(package)
                elif package == 'pdfminer.six':
                    try:
                        __import__('pdfminer')
                    except ImportError:
                        missing_packages.append(package)
                elif package == 'edge-tts':
                    try:
                        __import__('edge_tts')
                    except ImportError:
                        missing_packages.append(package)
                else:
                    missing_packages.append(package)
        
        if missing_packages:
            print("⚠️  Missing required packages:")
            for package in missing_packages:
                print(f"   - {package}")
            print("\n📦 Install missing packages with:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def create_directories(self):
        """Create required directories"""
        directories = ['temp_audio', 'backend', 'frontend', 'config']
        
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def check_environment(self):
        """Check environment variables"""
        env_file = Path('.env')
        if not env_file.exists():
            print("⚠️  .env file not found. Please create it with your API keys.")
            return False
        
        required_vars = ['GROQ_API_KEY', 'OPENAI_API_KEY']
        missing_vars = []
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print("⚠️  Missing environment variables:")
            for var in missing_vars:
                print(f"   - {var}")
            print("\n🔑 Please add these to your .env file")
        
        return True  # Allow running even with missing API keys for testing
    
    def run(self):
        """Run both servers"""
        print("🧠 Starting Skillmotion AI Assistant...")
        print("=" * 50)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Check dependencies
        if not self.check_dependencies():
            sys.exit(1)
        
        # Create directories
        self.create_directories()
        
        # Check environment
        self.check_environment()
        
        try:
            # Start backend server in a separate thread
            backend_thread = threading.Thread(
                target=self.backend_server.run,
                name="BackendServer",
                daemon=True
            )
            backend_thread.start()
            self.threads.append(backend_thread)
            
            # Give backend time to start
            time.sleep(2)
            
            # Start frontend server in a separate thread
            frontend_thread = threading.Thread(
                target=self.frontend_server.run,
                name="FrontendServer",
                daemon=True
            )
            frontend_thread.start()
            self.threads.append(frontend_thread)
            
            print("\n✅ Skillmotion AI Assistant is running!")
            print("🌐 Frontend: http://localhost:8080")
            print("🚀 Backend:  http://localhost:5000")
            print("\n📝 Instructions:")
            print("   1. Open http://localhost:8080 in your browser")
            print("   2. Upload your resume (PDF format)")
            print("   3. Specify your target job role")
            print("   4. Get AI-powered career insights!")
            print("\n🎤 Voice interaction is supported!")
            print("Press Ctrl+C to stop the servers")
            
            # Keep main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if threads are still alive
                for thread in self.threads:
                    if not thread.is_alive():
                        print(f"⚠️  Thread {thread.name} has stopped")
                        
        except KeyboardInterrupt:
            print("\n🛑 Received interrupt signal")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop all servers"""
        self.running = False
        
        print("🛑 Stopping servers...")
        
        # Stop backend
        self.backend_server.stop()
        
        # Stop frontend
        self.frontend_server.stop()
        
        print("✅ Skillmotion AI Assistant stopped")

def main():
    """Main entry point"""
    runner = SkillmotionRunner()
    runner.run()

if __name__ == "__main__":
    main()