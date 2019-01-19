import traceback
import CONFIG
import CONFIG_DEFAULT
import copy
import pickle
import pprint

class Config:
    configs = {}

    def __init__(self):
        pass

    def get_token(self):
        return CONFIG.PINBOT["TOKEN"]

    def of(self, guild) -> dict:
        if guild.id not in self.configs.keys():
            self.initialize_default(guild_id=guild.id)
            self.save()
        return self.configs[guild.id]

    def initialize_default(self, guild_id):
        self.configs[guild_id] = copy.deepcopy(CONFIG_DEFAULT.PINBOT)
        self.save()

    def save(self):
        with open("configs.pickle", "wb") as f:
            pickle.dump(self.configs, f)
        return self

    def load(self):
        try:
            with open("configs.pickle", "rb") as f:
                self.configs = pickle.load(f)
        except IOError:
            print(traceback.format_exc())
        return self

    def generate_readable(self, guild_id = None):
        if not guild_id:
            return pprint.pformat(self.configs)
        else:
            return pprint.pformat(self.configs[guild_id])
