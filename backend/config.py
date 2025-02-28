# config.py - Configuration Settings
#from dotenv import load_dotenv
import os
# Load environment variables from .env file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'edac877add000011fc0de3a4cc598673'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#load_dotenv()