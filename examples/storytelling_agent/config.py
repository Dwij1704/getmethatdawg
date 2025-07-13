import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the Storytelling Agent"""
    
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
    GOOGLE_CLOUD_LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    GOOGLE_GENAI_USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'True').lower() == 'true'
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Application settings
    MAX_STORY_LENGTH = int(os.getenv('MAX_STORY_LENGTH', '20'))
    IMAGE_GENERATION = os.getenv('IMAGE_GENERATION', 'True').lower() == 'true'
    AUDIO_GENERATION = os.getenv('AUDIO_GENERATION', 'True').lower() == 'true'
    WEB_PORT = int(os.getenv('WEB_PORT', '5000'))
    
    # Validate required keys
    @classmethod
    def validate(cls):
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not cls.GOOGLE_API_KEY and not (cls.GOOGLE_CLOUD_PROJECT and cls.GOOGLE_GENAI_USE_VERTEXAI):
            missing_keys.append("GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT")
        
        if not cls.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY (required for images and TTS)")
            
        if not cls.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY (required for story generation)")
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        return True 