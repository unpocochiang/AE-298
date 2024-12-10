import os
import sys

# Add the app's directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from app import app as application