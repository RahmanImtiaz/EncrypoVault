class AuditLog:
    _AuditLog = None

    def __new__(cls):
        if cls._AuditLog is None:
            cls._AuditLog = super(AuditLog, cls).__new__(cls)
            cls._AuditLog.__initialized = False
        return cls._AuditLog

    def __init__(self):
        if getattr(self, '_initialized', False):
            return
        self._entries = {}
        self._initialized = True

    @staticmethod
    def get_instance():
        return AuditLog._AuditLog

    def get_entries(self):
        return self._entries

    def add_entry(self, account_name, time, status):
        self._entries[time] = {
            'account_name': account_name,
            'status': status
        }

