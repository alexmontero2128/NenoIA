import os

# Database Configuration
database_uri = os.getenv('DATABASE_URI', 'sqlite:///default.db')

def get_database_uri():
    return database_uri

# Flask Configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    DEBUG = os.getenv('DEBUG', False)
    TESTING = os.getenv('TESTING', False)