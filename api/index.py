import sys
import os

# Ensure the project root is on the Python path so that
# `from utils import ...` and Flask's template/static lookups work.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Import the Flask app – this is the WSGI entry-point that Vercel invokes.
from app import app

# Vercel expects the handler at module level
app = app
