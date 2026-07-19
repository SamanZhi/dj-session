class SessionStore:
    def __init__(self, session_key=None):
        self.session_key = session_key
        self._session = {}

        self.accessed = False
        self.modified = False

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
        self.modified = True
        return self._session.pop(key, default)
    
    def __contains__(self, key):
        return key in self._session