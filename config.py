import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'quicker-cid-server-secret-key-production-2024'
    # Render에서 자동으로 제공하는 PostgreSQL URL 사용
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"DATABASE_URL found: {database_url[:50]}...")  # 로그용 (보안상 일부만)
        if database_url.startswith('postgres://'):
            # Render의 postgres:// URL을 postgresql://로 변경
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("Converted postgres:// to postgresql://")
        SQLALCHEMY_DATABASE_URI = database_url
        print("Using PostgreSQL database")
    else:
        print("No DATABASE_URL found, falling back to SQLite")
        SQLALCHEMY_DATABASE_URI = 'sqlite:///quicker.db'
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///quicker.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 