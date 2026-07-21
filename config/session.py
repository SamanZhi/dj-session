import secrets

from .storage import Storage

class SessionStore:
    def __init__(self, session_key=None):
        self._session_key = session_key
        self._session = {}

        self.accessed = False
        self.modified = False

        if self.session_key:
            self._session = Storage.load().get(self.session_key, {})
        else:
            self._session_key = secrets.token_hex(16)

    def save(self):
        sessions = Storage.load()
        sessions[self.session_key] = self._session
        Storage.save(sessions)
    
    @property
    def session_key(self):
        return self._session_key
    
    def __getitem__(self, key):
        self.accessed = True
        return self._session[key]
    
    def __setitem__(self, key, value):
        self.modified = True
        self._session[key] = value

    def get(self, key, default=None):
        self.accessed = True
        return self._session.get(key, default)

    def pop(self, key, default=None):
        self.accessed = True
        self.modified = True
        return self._session.pop(key, default)
    
    def __contains__(self, key):
        self.accessed = True
        return key in self._session