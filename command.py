from .contexter import Contexter

class Command:
    def __init__(self, func, pre=None, post=None, fname: str = None, **kwargs):
        self.fname = fname
        self.func = func
        self.pres = []
        self.posts = []
        self.case_sens = kwargs.get("case_sens", True)
        self.ack = kwargs.get("ack", "")
        if not self.fname:
            self.fname = func.__name__  # type:str
        self.fname = self.fname.lower()

        if self.ack == "react":
            async def add_checkmark(ctx):
                await ctx.m.add_reaction("✅")

            self.posts.append(add_checkmark)

        elif self.ack == "delete":
            async def delete_m(ctx):
                await ctx.m.delete()

            self.posts.append(delete_m)

    async def execute(self, ctx : Contexter):
        pres = [await pre(ctx) for pre in self.pres]
        val = [await self.func(ctx)]
        posts = [await post(ctx) for post in self.posts]
        results = pres + val + posts
        for result in results:
            if not result:
                continue

            target_channel = ctx.config["DEFAULT_OUT"]
            if target_channel == "inplace":
                target_channel = ctx.m.channel
            else:
                target_channel = ctx.find_channel(target_channel, dynamic=True)

            if isinstance(result, str):
                await target_channel.send(result)