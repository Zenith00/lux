import logging
import discord
from .contexter import Contexter
from . import zutils
from .command import Command

class Lux(discord.Client):
    commands = {}

    def __init__(self, config, *args, **kwargs):
        self.config = config
        super(Lux, self).__init__(*args, **kwargs)

    async def on_ready(self):
        logging.info("Ready!")

    async def on_connect(self):
        logging.info("Connected")

    async def on_message(self, message):
        if message.content.startswith(self.config["PREFIX"]):
            command_raw = message.content[len(self.config["PREFIX"]):].lower()
            if command_raw in self.commands:
                await self.commands[command_raw].execute(Contexter(message, self.config))
            elif command_raw.split(" ")[0] in self.commands:
                await self.commands[command_raw.split(" ")[0]].execute(Contexter(message, self.config))

    @zutils.parametrized
    def command(func, self, name: str = None, **attrs):
        logging.info(f"Registered function: func: {func.__name__}, override name = {name}")
        command = Command(func, fname=name, **attrs)
        self.add_command(command)
        return command

    def add_command(self, command):
        self.commands[command.fname] = command

