import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import math

# tokens
from apikeys import *

# rapid api
import requests
import json

# for slash commands
from discord import app_commands

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

# slash commands
@client.tree.command(name = 'help')
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(
        "```"
        "==General commands=="
        "\n\t$zdravo     🙋‍♂️"
        "\n\t$cao        🧏‍♂️"
        "\n\t$frlikocka  🎲"
        "\n\t$mudrost    🧠"
        "\n\t$jbgcount   📊"
        "\n\n"
        "==Voice commands=="
        "\n\t$join"
        "\n\t$dc"
        "\n\t$play"
        "\n\t$stop"
        "\n\n"
        "==Media=="
        "\n\tme_zdrobi"
        "\n\trezil"
        "\n\tgluposti"
        "\n\tsiguren_li_si"
        "```"
    )

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
    await ctx.send(jbgcounter)

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
            jbgcounter = jbgcounter + 1

def checkKmb(message):
    splitmessage = message.split(" ")
    for part in splitmessage:
        if part == 'kmb':
            return 1

@client.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
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