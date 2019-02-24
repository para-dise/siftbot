import discord
from discord.ext import commands
import asyncio

allowed_users = []
owner_id = "your discord user ID"

def has_membership():
    def predicate(ctx):
        if ctx.message.author.id in allowed_users:
            print("Yes")
            return True
        else:
            print("No")
            return False
    return commands.check(predicate)

class Sift():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def allow(self, ctx, member):
        if ctx.message.author.id != owner_id:
            return
        allowed_users.append(str(member))
        await self.bot.say("``{}`` now has access to the bot. [{}]".format(member, allowed_users))

    @commands.group(pass_context=True)
    async def sift(ctx):
        pass

    @sift.command(pass_context=True)
    @has_membership()
    async def grep(self, ctx, *, v):
        if not len(v) > 4:
            await self.bot.say("Search query too small.")
            return
        import subprocess
        from subprocess import Popen
        from os import listdir
        from os.path import isfile, join
        import time
        results = 0
        files = [f for f in listdir("databases") if isfile(join("databases", f))]
        start_time = time.time()
        for fool in files:
            cmd = ['grep', v, 'databases/{}'.format(fool)]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            for line in p.stdout:
                results += 1
                _line = line.decode("utf-8")
                embresult = discord.Embed(title='{}'.format(fool), description='```{}```'.format(_line), colour=0xcc6666)
                await asyncio.sleep(1)
                await self.bot.say(embed=embresult)
        elapsed_time = time.time() - start_time
        await self.bot.say("Search completed in: ``{}`` seconds".format(elapsed_time))

    @sift.command(pass_context=True)
    @has_membership()
    async def search(self, ctx, *, v):
        if not len(v) > 4:
            await self.bot.say("Search query too small.")
            return
        import subprocess
        from subprocess import Popen
        from os import listdir
        from os.path import isfile, join
        import time
        results = 0
        files = [f for f in listdir("databases") if isfile(join("databases", f))]
        start_time = time.time()
        for fool in files:
            cmd = ['./sift', v, 'databases/{}'.format(fool)]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            for line in p.stdout:
                results += 1
                _line = line.decode("utf-8")
                embresult = discord.Embed(title='{}'.format(fool), description='```{}```'.format(_line), colour=0xcc6666)
                await asyncio.sleep(1)
                await self.bot.say(embed=embresult)
        elapsed_time = time.time() - start_time
        await self.bot.say("Search completed in: ``{}`` seconds".format(elapsed_time))


def setup(bot):
    bot.add_cog(Sift(bot))
