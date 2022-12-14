import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
# import math

# tokens
from apikeys import *

# rapid api
import requests
import json

# for slash commands
# from discord import app_commands

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

# on run


@client.event
async def on_ready():
    print("FINKI is online")
    print("---------------")

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    # global jbgcounter
    # with open('stats.txt', 'r')as f:
    #     jbgcounter = int(f.readline())

# slash commands


@client.tree.command(name = 'help', description = 'View all usable commands')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title = 'FINKI BOT Commands',
        description = 'List of all usable commands',
        color = discord.Color.blue(),
    )

    image = client.user.display_avatar
    embed.set_thumbnail(url = image)

    embed.add_field(
        name = '/help',
        inline = False,
        value = 'View all usable commands'
    )

    embed.add_field(
        name = '$zdravo\t🙋‍♂️',
        inline = True,
        value = 'say hello'
    )

    embed.add_field(
        name = '$cao\t🧏‍♂️',
        inline = True,
        value = 'say bye'
    )

    embed.add_field(
        name = '$frlikocka\t🎲',
        inline = True,
        value = 'get rand in range 1,6'
    )

    embed.add_field(
        name = '$mudrost\t🧠\t\t\t\t\t',
        inline = True,
        value = 'display life changing quote'
    )

    embed.add_field(
        name = '$jbgcount\t📊',
        inline = True,
        value = 'display jbgcounter'
    )

    embed.add_field(
        name = '\u200B', value = '\u200B', inline = True
    )

    embed.add_field(
        name = '$maus\t🐭',
        inline = True,
        value = 'za pred polaganje'
    )

    embed.add_field(
        name='$vino\t🍷',
        inline = True,
        value = 'za pred polaganje'
    )

    embed.add_field(
        name='\u200B', value='\u200B', inline=True
    )

    embed.add_field(
        name='$join',
        inline=True,
        value='enter vc'
    )

    embed.add_field(
        name='$dc',
        inline=True,
        value='leave vc'
    )

    embed.add_field(
        name='$play',
        inline=True,
        value='play media'
    )

    embed.add_field(
        name='$stop',
        inline=True,
        value='stop playing\nmedia'
    )

    embed.add_field(
        name = 'Media:',
        inline = True,
        value = 'me_zdrobi, rezil, gluposti, siguren_li_si, svetis, kasasozabo'
    )

    await interaction.response.send_message(embed=embed)

# regular commands


@client.command()
async def zdravo(ctx):
    await ctx.send("Mrsh...")


@client.command()
async def cao(ctx):
    await ctx.send("Nisto togas...")


@client.command()
async def frlikocka(ctx):
    await ctx.send(random.randint(1,6))


@client.command()
async def mudrost(ctx):
    url = "https://free-famous-quotes.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Key": MUDROSTTOKEN,
        "X-RapidAPI-Host": "free-famous-quotes.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    await ctx.send("***`" + json.loads(response.text)['quote']
                   + "\nby -" + json.loads(response.text)['author']
                   + "-`***")


@client.command()
async def jbgcount(ctx):
    with open('stats.txt', 'r') as f:
        jbgcounter = int(f.readline())
    await ctx.send(jbgcounter)


@client.command()
async def maus(ctx):
    for i in range(0,10):
        await ctx.send('🖱ovo je srecan maus. Podeli ga 10 '
                       'puta i polozices naredni ispit. Ignorisi i '
                       'pasces.')


@client.command()
async def vino(ctx):
    for i in range(0,10):
        await ctx.send('🍷 Ово је срећно вино. Подели га са 10 '
                       'људи и положићеш наредни испит. Имаћеш '
                       'разлог да пијеш. Игнориши и пашћеш.')


@client.command(aliases=['purge'])
async def purgespam(ctx, amount:int):
    if amount > 23:
        await ctx.send(f"Purging amount exceeding maximum ({amount}/23)")
    else:
        if ctx.message.author.id == AUTHORID:
            # if not ctx.message.content == '$purgespam':
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("This is a developer only command.")


# connect/disconnect voice
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('audio/dobarden.mp3')
        player = voice.play(source)

    else:
        await ctx.send("Ne si vo kanal, more...glup")


@client.command(pass_context = True)
async def dc(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Zaminuvam...")
    else:
        await ctx.send("Ne sum vo kanal, more...glup")

# play/stop audio


@client.command(pass_context = True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()


@client.command(pass_context = True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio('audio/' + arg + '.mp3')
    player = voice.play(source)

# detect words
jbgcounter = 0


def checkJebiga(message):
    global jbgcounter
    splitmessage = message.split(" ")
    for part in splitmessage:
        if part == 'jebiga':
            with open('stats.txt', 'r') as f:
                jbgcounter = int(f.readline())

            jbgcounter = jbgcounter + 1

            with open('stats.txt', 'w') as f:
                f.write(str(jbgcounter))


def checkKmb(message):
    splitmessage = message.split(" ")
    for part in splitmessage:
        if part == 'kmb':
            return 1


@client.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content).lower()
    channel = str(message.channel)

    # logs
    # print(f'{username} said: {user_message} in {channel}')

    # ban words
    if checkKmb(user_message) == 1:
        await message.delete()
        await message.channel.send("ne mi go spomnuvaj...")

    if not checkJebiga(user_message):
        await client.process_commands(message)

client.run(FINKITOKEN)
