import os
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from .env file if it exists
    Returns a dictionary of environment variables
    """
    # Try to load from .env file
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Define required variables with default empty values
    env_vars = {
        'CAPTCHA_API_KEY': os.getenv('CAPTCHA_API_KEY', ''),
        'NOTRE_SITEKEY': os.getenv('NOTRE_SITEKEY', ''),
        'SACAI_API_URL': os.getenv('SACAI_API_URL', ''),
        'PROXY_USERNAME': os.getenv('PROXY_USERNAME', ''),
        'PROXY_PASSWORD': os.getenv('PROXY_PASSWORD', '')
    }
    
    return env_vars
    
def get_api_key():
    """Helper to get the CAPTCHA API key"""
    return os.getenv('CAPTCHA_API_KEY', '') 