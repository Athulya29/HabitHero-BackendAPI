import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'habithero-secret-key-2024-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///habithero.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-2024-change-in-production'