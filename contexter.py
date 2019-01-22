from . import zutils
from . import config
import discord

class Contexter:
    called_with = {}
    def __init__(self, message, configs: config.Config = None, auth_func = None):
        if isinstance(configs, config.Config):
            self.config = configs.of(message.guild)  # type: dict
        else:
            self.config = configs

        self.m = message  # type: discord.Message
        self.deprefixed_content = self.m.content[len(self.config["PREFIX"]):]
        self.auth_func = auth_func

    def check_auth(self, *args, **kwargs):
        if not self.auth_func:
            return True
        else:
            return self.auth_func(self, *args, **kwargs)

    def find_role(self, query):
        if self.config["ROLE_BY_CONFIG"]:
            return self.find_role_config(query)
        else:
            return self.find_role_dynamic(query)

    def find_role_config(self, query):
        return self.m.guild.get_role(zutils.query_dict_softcase(self.config["ROLE_TO_ID"], query))

    def find_role_dynamic(self, query):
        if zutils.check_int(query):
            return self.m.guild.get_role(zutils.check_int(query))
        if isinstance(query, str):
            try:
                return next(role for role in self.m.guild.roles if role.name == query)
            except StopIteration:
                try:
                    return next(role for role in self.m.guild.roles if role.name.lower() == query.lower())
                except StopIteration:
                    return None

    def find_channel(self, query, dynamic=True):
        try:
            return self.m.guild.get_role(zutils.query_dict_softcase(self.config["ROLE_TO_ID"][query], query))
        except KeyError:
            if not dynamic:
                return
            if isinstance(query, int):
                return self.m.guild.get_channel(query)
            if isinstance(query, str):
                try:
                    res = next(channel for channel in self.m.guild.channels if channel.name == query)
                except StopIteration:
                    res = next(channel for channel in self.m.guild.channels if channel.name.lower() == query.lower())
                return res
