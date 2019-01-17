class Contexter:
    def __init__(self, message, config):
        self.config = config
        self.m = message

    def find_role(self, query):
        if self.config.ROLE_BY_self.config:
            return self.find_role_config(query)
        else:
            return self.find_role_dynamic(query)

    def find_role_config(self, query):
        if query in self.config.ROLE_TO_ID.keys():
            return self.m.guild.get_role(self.config.ROLE_TO_ID[query])
        elif query.lower() in self.config.ciROLE_TO_ID.keys():
            return self.m.guild.get_role(self.config.ciROLE_TO_ID[query.lower()])
        raise Exception(f"Role: [{query}] not found in config")

    def find_role_dynamic(self, query):
        if isinstance(query, int):
            return next(role for role in self.m.guild.roles if role.id == query)
        if isinstance(query, str):
            try:
                res = next(role for role in self.m.guild.roles if role.name == query)
            except StopIteration:
                res = next(role for role in self.m.guild.roles if role.name.lower() == query.lower())
            return res