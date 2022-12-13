import discord
from discord.ext import commands
import random
import math

# tokens
from apikeys import *

# rapid api
import requests
import json

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

# commands
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

# connect/disconnect voice
@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Ne si vo kanal, more...glup")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Zaminuvam...")
    else:
        await ctx.send("Ne sum vo kanal, more...glup")

client.run(FINKITOKEN)