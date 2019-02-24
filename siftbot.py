from discord.ext import commands

token = 'your token'
owner_id = "your discord user ID"

startup_extensions = ["sift"]

bot = commands.Bot(command_prefix='$', description=description)

def is_owner():
    def predicate(ctx):
        if ctx.message.author.id == owner_id:
            return True
        else:
            return False
    return commands.check(predicate)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
@is_owner()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command()
@is_owner()
async def reloadall(extension_name : str):
    """Loads an extension."""
    for cog in startup_extensions:
        bot.unload_extension(cog)
        await bot.say("{} unloaded.".format(cog))
        bot.load_extension("{} loaded.".format(cog))

@bot.command()
@is_owner()
async def reload(extension_name : str):
    """Reloads an extension."""
    try:
        bot.unload_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("``{}`` reloaded.".format(extension_name))

@bot.command()
@is_owner()
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@bot.command(pass_context=True)
@is_owner()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command(pass_context=True)
async def collections(ctx):
    return # Remove this line if you actually have these files.
    await bot.say("I do not provide access to collection #1-5 because of drastic CPU usage when searching. Same goes for anti-public.")
    await bot.send_file(ctx.message.channel, "collections/collection1.torrent")
    await bot.send_file(ctx.message.channel, "collections/collection2-5&antipublic.torrent")

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.run(token)
