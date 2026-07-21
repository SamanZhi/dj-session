import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "sessions.json"

class Storage:
    @staticmethod
    def load():
        if not SESSION_FILE.exists():
            return {}
        
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
        
    @staticmethod
    def save(data):
        with open(SESSION_FILE, "w") as f:
            json.dump(data, f, indent=4)