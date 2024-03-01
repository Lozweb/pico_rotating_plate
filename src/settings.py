import ujson as json


class Settings:

    # 500 = 45° | 89 = +/- 1°
    def __init__(self):
        self.tt_degree = 4080  # = 360°
        self.pause = 8  # 360/8 = 45 °
        self.delay = 1  # paused 1s
        self.direction = 1  # horaire
        self.presets = {"preset": [
            {"name": "preset-1", "tt_degree": 4080, "pause": 8, "delay": 1, "direction": 1},
            {"name": "preset-2", "tt_degree": 4080, "pause": 16, "delay": 2, "direction": 1}
        ]}

    def get_step(self):
        return self.tt_degree // self.pause  # 4000 / 8 = 500

    def set_direction(self, direction: str):
        if direction == "horaire":
            self.direction = 1
        else:
            self.direction = -1

    def init_default_preset(self):
        try:
            with open("settings.json", "w") as f:
                json.dump(self.presets, f)
        except:
            print("Error, Could not save")
