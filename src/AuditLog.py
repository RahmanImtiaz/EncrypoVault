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
        if AuditLog._AuditLog is None:
            AuditLog()
        return AuditLog._AuditLog

    def get_entries(self):
        return self._entries

    def add_entry(self, account_name, time, status):
        self._entries[time] = {
            'account_name': account_name,
            'status': status
        }

    def get_entries_in_range(self, start_time, end_time):
        result = {time: entry for time, entry in self._entries.items() if start_time <= time <= end_time}
        
        # Create a CountedEntries class that extends dict and adds a count method <- this is bcs we were using .count for a dictionary
        class CountedEntries(dict):
            def count(self):
                return sum(1 for entry in self.values() if entry['status'] == 'FAILED')
                
        # Return a CountedEntries instance instead of a plain dict <- now we can use .count() on this 
        return CountedEntries(result)