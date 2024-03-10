from preset import Preset


class Settings:

    def __init__(self):
        self.preset = Preset()
        self.current_preset = self.preset.load_preset_by_name('preset-1')

    def load_preset(self, preset):
        self.current_preset = self.preset.load_preset_by_name(preset)

    @staticmethod
    def save_preset(preset_to_save: Preset):
        data = Preset.load_presets_data()

        presets = []

        for preset in data['presets']:
            presets.append(preset)

        print(preset_to_save.name)
