from . import zutils
import discord


class Contexter:
    def __init__(self, message, config):
        self.config = config  # type: dict
        self.m = message  # type: discord.Message
        self.deprefixed_content = self.m.content[len(self.config["PREFIX"]):]

    def find_role(self, query):
        if self.config["ROLE_BY_CONFIG"]:
            return self.find_role_config(query)
        else:
            return self.find_role_dynamic(query)


    def find_role_config(self, query):
        return self.m.guild.get_role(zutils.query_dict_softcase(self.config["ROLE_TO_ID"][query], query))

    def find_role_dynamic(self, query):
        if isinstance(query, int):
            return self.m.guild.get_role(int)
        if isinstance(query, str):
            try:
                res = next(role for role in self.m.guild.roles if role.name == query)
            except StopIteration:
                res = next(role for role in self.m.guild.roles if role.name.lower() == query.lower())
            return res

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
