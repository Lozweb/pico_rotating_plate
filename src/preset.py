import json


class Preset:

    def __init__(self):
        self.name = None
        self.tt_degree = None
        self.pause = None
        self.delay = None
        self.direction = None

    @staticmethod
    def load_presets_data():
        f = open('presets.json', 'a')
        data = f.read()
        return json.loads(data)

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
            
