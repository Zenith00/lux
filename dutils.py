import discord


def message2dict(message: discord.Message):
    return {k: message.__getattribute__(k) for k in message.__slots__}
