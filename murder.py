# made with love /// murder#0001
# this shit got skidded hard asf by some retards, just gonna release it. there is no help menu, look at the source for commands.

#--------------------------------------------------------------------------------------------------
import discord, json, os, time, random
from discord.ext import commands
from discord import Embed
#--------------------------------------------------------------------------------------------------

#Client & Configuration
config = json.load(open('config.json'))

snipe_message_author = {}
snipe_message_content = {}

filterWords = False
filterImages = False

editWords = [
    "baboon", "kys", "nigger", "n1gger", "swat", "die",
    "nuke", "selfbot", "monkey", "gorilla", "retard", "fag",
    "tranny", "raid", "transformer"
]

client = commands.Bot(
    command_prefix = config["Client"]["Prefix"],
    case_insensitive=True,
    help_command=None,
    self_bot=True
)

#--------------------------------------------------------------------------------------------------
#Register Events
@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Logged in as: {}\n> version: 1.0\n'.format(client.user))


@client.event
async def on_command_error(ctx, error):
    print("[!] [ERROR]: {}".format(str(error)))

@client.event
async def on_message(message):
    for word in editWords:
        if word in message.content.lower() and filterWords:
            time.sleep(3.5)
            try:
                return await message.edit(content="xyz", delete_after=3)
            except: pass
    
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content

#--------------------------------------------------------------------------------------------------
#Commands

@client.command()
async def banner(ctx, user:discord.Member):
    await ctx.message.delete()
    if user == None:
        user = ctx.author
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    await ctx.send(f"{banner_url}")

@client.command()
async def av(ctx, *, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    avatarurl = user.avatar_url
    await ctx.send(avatarurl)

@client.command(aliases=['setting', 'toggle', 'untoggle'])
async def settings(ctx, setting="None"):
    global filterWords, filterImages, logMessages

    validTXT = """```ini
[ Made By: murder#0001 ]

Command parsed successfully!
Successfully toggled: {} {}
    
[ Made by: murder#0001 ]```"""

    invalidTXT = """```ini
[ ]

Invalid option parsed
Valid options are: \"filter\", \"images\", \"messages\"

[ Made by: murder#0001 ]```"""

    if setting.lower() == "filter":
        if filterWords:
            filterWords = False
            await ctx.message.edit(content=validTXT.format("filter", "off"), delete_after=5)
        else:
            filterWords = True
            await ctx.message.edit(content=validTXT.format("filter", "on"), delete_after=5)

    elif setting.lower() == "images":
        await ctx.message.edit(content="in development", delete_after=3)

    else:
        await ctx.message.edit(content=invalidTXT, delete_after=5)
    
@client.command(aliases=['log'])
async def snipe(ctx):
    try:
        await ctx.message.edit(content="""```ini
[ Made By: murder#0001 ]
[ Message sent by: {} in: {}]

Message content: {}

[ Made by: murder#0001 ]```""".format(snipe_message_author[ctx.channel.id], f"#{ctx.channel.name}", snipe_message_content[ctx.channel.id]), delete_after=5)
    except KeyError:
        await ctx.send(f"There are no recently deleted messages in #{ctx.channel.name}", delete_after=10)

@client.command()
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/murder", 
    )
    await client.change_presence(activity=stream)
    print("[#] [ACTION]: Set streaming status in channel: \"{}\".".format(ctx.channel.name))
    await ctx.message.edit(content="""```ini
[ Made By: murder#0001 ]
    
set stream status to: {}
check your status!

[ Made by: murder#0001 ]```""".format(message), delete_after=5)

@client.command(aliases=['create', 'geninvite'])
async def createinvite(ctx, guildid: int):
    try:
        guild = client.get_guild(guildid)
        await ctx.send("Got guild: {}".format(guild))
        channel = guild.channels[0]
        await ctx.send("Got channel: {}".format(channel))
        invitelink = await channel.create_invite(max_uses=1)
        await ctx.send("Created invite")
        await ctx.send(invitelink)
    except Exception as e:
        await ctx.send("check console")
        print(e)

@client.command(aliases=['clean', 'delete'])
async def purge(ctx, amount: int):
    if amount > 200:
        return await ctx.reply("you cant purge more than 200", delete_after=3)
    
    await ctx.message.delete()
    
    deleted = 0
    slept = 0
    ratelimited = 0
    
    async for message in ctx.channel.history(limit=amount):
        try:
            if message.author == client.user:
                await message.delete()
                deleted += 1
                if (random.randint(0, 16) == 4): #To avoid ratelimit/term, sleep every so often.
                    time.sleep(7.5)
                    slept += 1
            else:
                pass
        except discord.errors.HTTPException:
            ratelimited += 1
        except:
            pass
        
    print("[#] [ACTION]: Finished purge in channel: \"{}\".".format(ctx.channel.name))
    await ctx.send("""```ini
[ Made By: murder#0001 ]

Successfully deleted {} messages.
Slept: {} times.

You were ratelimited: {} times.

[ Made by: murder#0001 ]```""".format(deleted, slept, ratelimited), delete_after=5)

@client.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'```ini\n[ Murder Test ]\n\nClient ms is: {round(client.latency * 1000)}ms \n\n[ Made By: murder#0001 ]\n```', delete_after=3)

@client.command()
async def hi(ctx):
    await ctx.message.delete()
    await ctx.send("https://tenor.com/view/kitten-kiss-cute-pet-cat-gif-20374133")
#--------------------------------------------------------------------------------------------------
client.run(config["Client"]["Token"], bot=False, reconnect=True)
