class Settings:

    # 500 = 45° | 89 = +/- 1°
    def __init__(self):
        self.tt_degree = 4080  # = 360°
        self.pause = 8  # 360/8 = 45 °
        self.delay = 1  # paused 1s
        self.direction = 1  # horaire

    def get_step(self):
        return self.tt_degree // self.pause  # 4000 / 8 = 500

    def set_direction(self, direction: str):
        if direction == "horaire":
            self.direction = 1
        else:
            self.direction = -1
