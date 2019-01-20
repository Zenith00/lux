import traceback
import CONFIG
import CONFIG_DEFAULT
import copy
import pickle
import pprint

class Config:
    server_configs = {}

    def __init__(self, botname):
        self.name = botname
        self.DEFAULTS = getattr(CONFIG_DEFAULT, self.name, {})
        self.CONFIG = getattr(CONFIG, self.name)
        pass

    def get_token(self):
        return getattr(self.CONFIG["TOKEN"])

    def of(self, guild) -> dict:
        if guild.id not in self.server_configs.keys():
            self.initialize_default(guild_id=guild.id)
            self.save()
        return self.server_configs[guild.id]

    def initialize_default(self, guild_id):
        self.server_configs[guild_id] = copy.deepcopy(self.DEFAULTS)
        self.save()

    def reset_key(self, guild_id, key):
        try:
            self.server_configs[guild_id][key] = copy.deepcopy(self.DEFAULTS[key])
        except KeyError:
            print(traceback.format_exc())
            del self.server_configs[guild_id][key]

    def save(self):
        with open("configs.pickle", "wb") as f:
            pickle.dump(self.server_configs, f)
        return self

    def load(self):
        try:
            with open("configs.pickle", "rb") as f:
                self.server_configs = pickle.load(f)
        except IOError:
            print(traceback.format_exc())
        return self

    def generate_readable(self, guild_id = None):
        if not guild_id:
            return pprint.pformat(self.server_configs)
        else:
            return pprint.pformat(self.server_configs[guild_id])
