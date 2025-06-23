import edge_tts
import asyncio
import os
import tempfile
import hashlib
from datetime import datetime

class TTSGenerator:
    def __init__(self):
        # Create temp directory for audio files
        self.temp_dir = 'temp_audio'
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Available voices (you can add more)
        self.voices = {
            'female': 'en-US-JennyNeural',
            'male': 'en-US-GuyNeural',
            'default': 'en-US-AriaNeural'
        }
        
        self.default_voice = self.voices['default']
        self.default_rate = '+0%'
        self.default_volume = '+0%'
    
    async def generate_speech(self, text, voice=None, rate=None, volume=None):
        """Generate speech from text using edge-tts"""
        try:
            # Use defaults if not specified
            voice = voice or self.default_voice
            rate = rate or self.default_rate
            volume = volume or self.default_volume
            
            # Create a unique filename based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_{text_hash}_{timestamp}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Check if file already exists (cache)
            if os.path.exists(filepath):
                return filepath
            
            # Generate speech
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume
            )
            
            await communicate.save(filepath)
            
            # Clean up old files (keep only last 50 files)
            await self._cleanup_old_files()
            
            return filepath
            
        except Exception as e:
            print(f"TTS generation error: {e}")
            raise Exception(f"Failed to generate speech: {str(e)}")
    
    async def _cleanup_old_files(self, max_files=50):
        """Clean up old audio files to prevent disk space issues"""
        try:
            files = []
            for filename in os.listdir(self.temp_dir):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(self.temp_dir, filename)
                    files.append((filepath, os.path.getctime(filepath)))
            
            # Sort by creation time, newest first
            files.sort(key=lambda x: x[1], reverse=True)
            
            # Remove excess files
            if len(files) > max_files:
                for filepath, _ in files[max_files:]:
                    try:
                        os.unlink(filepath)
                    except:
                        pass  # Ignore errors during cleanup
                        
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    async def get_available_voices(self):
        """Get list of available voices"""
        try:
            voices = await edge_tts.list_voices()
            return [
                {
                    'name': voice['Name'],
                    'short_name': voice['ShortName'],
                    'gender': voice['Gender'],
                    'locale': voice['Locale']
                }
                for voice in voices
                if voice['Locale'].startswith('en')  # English voices only
            ]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return list(self.voices.values())
    
    def set_default_voice(self, voice_name):
        """Set the default voice for TTS generation"""
        self.default_voice = voice_name
    
    def set_speech_parameters(self, rate=None, volume=None):
        """Set default speech parameters"""
        if rate:
            self.default_rate = rate
        if volume:
            self.default_volume = volume
    
    async def generate_welcome_message(self, options):
        """Generate welcome message with options"""
        welcome_text = "Welcome to Skillmotion AI Assistant. I can help you with: "
        
        option_texts = []
        for i, option in enumerate(options, 1):
            option_texts.append(f"{i}. {option['title']}")
        
        full_text = welcome_text + ", ".join(option_texts) + ". Please say or select an option."
        
        return await self.generate_speech(full_text)
    
    async def generate_response_with_emotion(self, text, emotion='neutral'):
        """Generate speech with different emotional tones"""
        voice_mapping = {
            'excited': 'en-US-AriaNeural',
            'calm': 'en-US-JennyNeural', 
            'professional': 'en-US-DavisNeural',
            'friendly': 'en-US-JaneNeural',
            'neutral': self.default_voice
        }
        
        rate_mapping = {
            'excited': '+10%',
            'calm': '-10%',
            'professional': '+0%',
            'friendly': '+5%',
            'neutral': '+0%'
        }
        
        selected_voice = voice_mapping.get(emotion, self.default_voice)
        selected_rate = rate_mapping.get(emotion, self.default_rate)
        
        return await self.generate_speech(text, voice=selected_voice, rate=selected_rate)