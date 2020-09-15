
from krakenhelper.helper import Date


class cache:
    def __init__(self):
        self.cache = {}
        a=1

    def get(self, record_type, record_id):

        if not self.cache.get(record_type, None):
            return None

        if not self.cache[record_type].get(record_id, None):
            return None

        return self.cache[record_type][record_id].get('record', None)


    def post(self, record):
        record_type = record.get('@type', None)
        record_id = record.get('@id', None)

        if not self.cache.get(record_type, None):
            self.cache[record_type] = {}

        if not self.cache[record_type].get(record_id, None):
            self.cache[record_type][record_id] = {}

        
        self.cache[record_type][record_id]['record'] = record
        
        d = Date()
        self.cache[record_type][record_id]['last_updated'] = d.now()

        # Check space, remove old items if not enough space



    def search(self, record_type, key, value):

        # Error handling
        if not key or not value:
            return None

        if not self.cache.get(record_type, None):
            return None

        # Iterates through records and return id of one that fits
        for i in self.cache.get(record_type, []):
            if self.cache[record_type][i]['record'][key] == value:
                return i

        return None