from .contexter import Contexter

class Command:
    def __init__(self, func, pre=None, post=None, fname: str = None, **kwargs):
        self.fname = fname
        self.func = func
        self.pres = []
        self.posts = []
        self.case_sens = kwargs.get("case_sens", True)
        self.onlyme = kwargs.get("onlyme", False)
        if not self.fname:
            self.fname = func.__name__  # type:str
        self.fname = self.fname.lower()


    async def process_config(self, ctx : Contexter):
        if ctx.config["ACK_TYPE"] == "react":
            async def add_checkmark(ctx):
                await ctx.m.add_reaction("✅")
            self.posts.append(add_checkmark)

        if ctx.config["ACK_TYPE"] == "delete":
            async def delete_m(ctx):
                await ctx.m.delete()
            self.posts.append(delete_m)

    async def execute(self, ctx : Contexter):
        if self.onlyme and ctx.m.author.id != 129706966460137472:
            return

        pres = [await pre(ctx) for pre in self.pres]
        val = [await self.func(ctx)]
        posts = [await post(ctx) for post in self.posts]
        results = pres + val + posts
        for result in results:
            if not result:
                continue
            print(result)
            if not isinstance(result, list):
                result = [result]
            for subresult in result:
                target_channel = ctx.config["DEFAULT_OUT"]
                if target_channel == "inplace":
                    target_channel = ctx.m.channel
                else:
                    target_channel = ctx.find_channel(target_channel, dynamic=True)
                if isinstance(subresult, str):
                    await target_channel.send(subresult)