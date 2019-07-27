import datetime

class Session():
    
    def __init__(self, debug=False):
        self.data = {"start": datetime.datetime.today().strftime('%d/%m/%Y %H:%M'), "end": None,
                     "name": None
                     }
        self.debug = debug
    
    def close(self):
        self.data["end"] = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')