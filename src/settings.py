from preset import Preset


class Settings:

    def __init__(self):
        self.preset = Preset()
        self.current_preset = self.preset.load_preset_by_name('preset-1')

    def load_preset(self, preset):
        self.current_preset = self.preset.load_preset_by_name(preset)

    def save_preset(self):
        data = Preset.load_presets_data()
        
        to_save = []
        
        for preset in data["presets"]:
            
            if preset["name"] == self.current_preset.get_name():
                to_save.append({
                        "name": self.current_preset.name,
                        "delay": self.current_preset.delay,
                        "direction": self.current_preset.direction,
                        "tt_degree": self.current_preset.tt_degree,
                        "pause": self.current_preset.pause
                    })
            else:
                to_save.append(preset)
        
        Preset.save_presets_data({"presets": to_save})
        