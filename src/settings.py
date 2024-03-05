from preset import Preset


class Settings:

    def __init__(self):
        self.presets = Preset()
        self.current_preset = self.presets.load_preset_by_name('preset-1')
