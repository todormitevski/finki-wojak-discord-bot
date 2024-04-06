import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
from apikeys import *

# rapid api
import requests
import json

# sentiment analysis
from textblob import TextBlob

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print("FINKI Wojak is online")
    print("---------------")

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


# slash commands
@client.tree.command(name='help', description='View all usable commands')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title='FINKI WOJAK BOT Commands',
        description='List of all usable commands',
        color=discord.Color.blue(),
    )

    image = client.user.display_avatar
    embed.set_thumbnail(url=image)

    embed.add_field(
        name='/help',
        inline=False,
        value='View all usable commands'
    )

    embed.add_field(
        name='$zdravo\t🙋‍♂️',
        inline=True,
        value='say hello'
    )

    embed.add_field(
        name='$cao\t🧏‍♂️',
        inline=True,
        value='say bye'
    )

    embed.add_field(
        name='$frlikocka\t🎲',
        inline=True,
        value='get rand in range 1,6'
    )

    embed.add_field(
        name='$mudrost\t🧠',
        inline=True,
        value='display life changing quote'
    )

    embed.add_field(
        name='$wordcount\t📊',
        inline=True,
        value='display number of profanities cleared'
    )

    embed.add_field(
        name='$mood @user\t🎭',
        inline=True,
        value='assess mood based on recent messages'
    )

    embed.add_field(
        name='$maus\t🐭',
        inline=True,
        value='za pred polaganje'
    )

    embed.add_field(
        name='$vino\t🍷',
        inline=True,
        value='za pred polaganje'
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
        name='$play [media_name]',
        inline=True,
        value='play media'
    )

    embed.add_field(
        name='$stop',
        inline=True,
        value='stop playing\nmedia'
    )

    embed.add_field(
        name='\u200B',
        value='\u200B',
        inline=True
    )

    embed.add_field(
        name='Media:',
        inline=True,
        value='[redacted]'
    )

    await interaction.response.send_message(embed=embed)


# regular commands
@client.command()
async def zdravo(ctx):
    await ctx.send("Zdr...")


@client.command()
async def cao(ctx):
    await ctx.send("Cao...")


@client.command()
async def frlikocka(ctx):
    await ctx.send(random.randint(1, 6))


@client.command()
async def mudrost(ctx):
    url = "https://olato-quotes.p.rapidapi.com/motivation"
    querystring = {"quotes": "random quotes"}

    headers = {
        "X-RapidAPI-Key": API_TOKEN,
        "X-RapidAPI-Host": "olato-quotes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        quote_data = response.json()
        # second arg is default value of quote == null
        quote_text = quote_data.get('quote', 'Sorry, I couldn\'t fetch a quote at the moment.')

        formatted_quote = f"***\"{quote_text}\"***"
        await ctx.send(formatted_quote)
    else:
        await ctx.send("Sorry, I couldn't fetch a quote at the moment.")


@client.command()
async def wordcount(ctx):
    with open('stats.txt', 'r') as f:
        wordcounter = int(f.readline())
    await ctx.send("Number of profanities cleared: {}".format(wordcounter))


@client.command()
async def maus(ctx):
    for i in range(0, 10):
        await ctx.send('🖱ovo je srecan maus. Podeli ga 10 '
                       'puta i polozices naredni ispit. Ignorisi i '
                       'pasces.')


@client.command()
async def vino(ctx):
    for i in range(0, 10):
        await ctx.send('🍷 Ово је срећно вино. Подели га са 10 '
                       'puta и положићеш наредни испит. Имаћеш '
                       'разлог да пијеш. Игнориши и пашћеш.')


@client.command(aliases=['purge'])
async def purgespam(ctx, amount: int):
    if amount > 40:
        await ctx.send(f"Purging amount exceeding maximum ({amount}/40)")
    else:
        if ctx.message.author.id == AUTHORID:
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.send("This is a developer only command.")


# connect/disconnect voice
@client.command(pass_context=True)
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('audio/dobarden.mp3')
        player = voice.play(source)

    else:
        await ctx.send("Ne si vo kanal...")


@client.command(pass_context=True)
async def dc(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Zaminuvam...")
    else:
        await ctx.send("Ne sum vo kanal...")


# play/stop audio
@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(pass_context=True)
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    source = FFmpegPCMAudio('audio/' + arg + '.mp3')
    player = voice.play(source)


# detect profane words
def checkWords(message):
    splitmessage = message.split(" ")
    for part in splitmessage:
        if part == 'skit' or part == 'vnp':
            with open('stats.txt', 'r') as f:
                wordcounter = int(f.readline())

            wordcounter = wordcounter + 1

            with open('stats.txt', 'w') as f:
                f.write(str(wordcounter))

            return 1


# sentiment analysis
def analyze_mood(messages):
    total_sentiment = 0
    message_count = 0

    for message in messages:
        blob = TextBlob(message.content)
        total_sentiment += blob.sentiment.polarity
        message_count += 1

    # calculate average sentiment polarity
    if message_count > 0:
        average_sentiment = total_sentiment / message_count

        # classify mood based on average sentiment polarity
        if average_sentiment > 0.1:
            return "Happy"
        elif average_sentiment < -0.1:
            return "Sad"
        else:
            return "Neutral"
    else:
        return "Neutral"


@client.command()
async def mood(ctx, user: discord.Member):

    # get user's 10 most recent msgs
    recent_messages = []
    async for message in ctx.channel.history(limit=10):
        recent_messages.append(message)
    user_messages = [message for message in recent_messages if message.author == user]

    # mood analysis of specified user
    user_mood = analyze_mood(user_messages)

    # assessment
    mood_message = f"{user.mention}'s mood: {user_mood}"
    if user_mood == "Happy":
        image_path = "images/happy_wojak.png"
    elif user_mood == "Sad":
        image_path = "images/sad_wojak.png"
    else:
        image_path = "images/neutral_wojak.png"

    with open(image_path, "rb") as f:
        mood_image = discord.File(f)
        await ctx.send(content=mood_message, file=mood_image)


@client.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content).lower()
    channel = str(message.channel)

    # logs
    print(f'{username} said: {user_message} in {channel}')

    # ban words
    if checkWords(user_message) == 1:
        await message.delete()
        await message.channel.send("ne mi go spomnuvaj...")

    await client.process_commands(message)


client.run(BOT_TOKEN)
