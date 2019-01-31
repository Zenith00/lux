import asyncio
import logging
import discord
from .contexter import Contexter
from . import zutils
from .command import Command
#test
class Lux(discord.Client):
    commands = {}

    def __init__(self, config, *args, **kwargs):
        self.config = config
        self.auth_function = kwargs.get("auth_function", True)
        super(Lux, self).__init__(*args, **kwargs)

    async def on_ready(self):
        logging.info("Ready!")

    async def on_connect(self):
        logging.info("Connected")

    async def on_message(self, message):
        ctx = Contexter(message, self.config, auth_func=self.auth_function)
        if message.content.startswith(ctx.config["PREFIX"]):
            command_raw = message.content[len(ctx.config["PREFIX"]):].lower()
            if command_raw in self.commands:
                await self.commands[command_raw].execute(ctx)
            elif command_raw.split(" ")[0] in self.commands:
                await self.commands[command_raw.split(" ")[0]].execute(ctx)

    @zutils.parametrized
    def command(func, self, name: str = None, **attrs):
        logging.info(f"Registered function: func: {func.__name__}, override name = {name}")
        command = Command(func, fname=name, **attrs)
        self.add_command(command)
        return command

    def add_command(self, command):
        self.commands[command.fname] = command

    def run_forever(self, func, delay=1, *args, **kwargs):
        async def forevered(*args_, **kwargs_):
            while True:
                func(*args_, **kwargs_)
                asyncio.sleep(delay)

        self.loop.run_until_complete(forevered(*args, **kwargs))
