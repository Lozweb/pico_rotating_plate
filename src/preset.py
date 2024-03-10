import json


class Preset:

    def __init__(self):
        self.name = None
        self.tt_degree = None
        self.pause = None
        self.delay = None
        self.direction = None

    def set_values(self, name: str, tt_degree: int, pause: int, delay:int, direction:int):
        self.name = name,
        self.tt_degree = tt_degree,
        self.pause = pause,
        self.delay = delay,
        self.direction = direction

    @staticmethod
    def load_presets_data():
        f = open('presets.json', 'a')
        data = f.read()
        f.close()
        return json.loads(data)

    @staticmethod
    def save_presets_data(data):
        f = open('presets.json', 'w')
        json_data = json.dumps(data)
        f.write(json_data)
        f.close()

    def load_preset_by_name(self, name: str):
        data = self.load_presets_data()
        for preset in data['presets']:
            if preset['name'] == name:
                self.name = preset['name']
                self.tt_degree = preset['tt_degree']
                self.pause = preset['pause']
                self.delay = preset['delay']
                self.direction = preset['direction']
        return self
    
    def get_name(self):
        return self.name
    
    def get_tt_degree(self):
        return self.tt_degree
    
    def get_pause(self):
        return self.pause
    
    def get_delay(self):
        return self.delay
    
    def get_direction(self):
        return self.direction
