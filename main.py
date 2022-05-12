import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
import requests
from datetime import datetime
from random import choices
import config

intents = discord.Intents(messages=True,
                          guilds=True,
                          reactions=True,
                          members=True,
                          presences=True)
client = commands.Bot(command_prefix='a.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="a.help"))
    print("Bot is ready! Logged on as", client.user)


@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = '>Welcome {0.mention} to {1.name}!'.format(member, guild)
        await guild.system_channel.send(to_send)


@client.event
async def on_member_remove(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = "> Goodbye {0.mention}. We won't miss you !".format(member)
        await guild.system_channel.send(to_send)


@client.command()
async def users(ctx):
    guild = client.get_guild(config.guild_id)
    await ctx.send(f"> No. of users = {guild.member_count}")


@client.command()
async def catvibe(ctx):
    await ctx.send("https://www.youtube.com/watch?v=NUYvbT6vTPs")


@client.command()
async def coffindance(ctx):
    await ctx.send("https://www.youtube.com/watch?v=j9V78UbdzWI")


@client.command(aliases=['youtube'])
async def yt(ctx, *args):
    word = " ".join(args)
    if (word != ""):
        videosSearch = VideosSearch(word, limit=2)
        await ctx.send(videosSearch.result()["result"][0]["link"])
    else:
        await ctx.send("Enter Song name to search!")


@client.command(aliases=['weather'])
async def w(ctx, *args):
    city = " ".join(args)
    if (city != ""):
        res = requests.get(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city +
            '&APPID=' + config.ow_api_key + '&units=metric').json()
        if (res['cod'] == 200):
            s = f">>> **Location**\n{city} {res['sys']['country']}\n\n**Weather**\n{res['weather'][0]['description']}\n\n**Temperature**\n{res['main']['temp']}°C\n\n"
            s += f"**Atmospheric Pressure**\n{res['main']['pressure']}Pa\n\n**Humidity**\n{res['main']['humidity']}%\n\n**Wind speed**\n{res['wind']['speed']}m/s\n\n**Wind direction**\n{res['wind']['deg']}\n\n"
            s += f"**Sun Rise**\n{datetime.utcfromtimestamp(int(res['sys']['sunrise'])).strftime('%H:%M:%S')}\n\n**Sun Set**\n{datetime.utcfromtimestamp(int(res['sys']['sunset'])).strftime('%H:%M:%S')}\n\n**Visibility**\n{res['visibility']}"

            await ctx.send(s)
        else:
            await ctx.send("City not found!")
    else:
        await ctx.send("Enter City to fetch data!")


@client.command()
async def ping(ctx):
    await ctx.send(
        f'>>> Pong!\nYour latency to the server is {int(client.latency*100)}ms'
    )


@client.command(aliases=['8ball'])
async def _8ball(ctx, *args):
    question = " ".join(args)
    answers = [
        'As I see it, yes.', 'Ask again later.', 'Better not tell you now.',
        'Cannot predict now.', 'Concentrate and ask again.',
        'Don’t count on it.', 'It is certain.', 'It is decidedly so.',
        'Most likely.', 'My reply is no.', 'My sources say no.',
        'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.',
        'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.',
        'Yes – definitely.', 'You may rely on it.'
    ]
    await ctx.send(f">>> **Q.: {question}**\nA.: {choices(answers)[0]}")


"""
@client.command(aliases = ['del'])
async def purge(ctx,amt = 5):
    await ctx.channel.purge(limit= amt)"""
"""
@client.command()
async def spam(ctx,*args):
    theSpam = " ".join(args)
    for i in range(0,100):
        await ctx.send(theSpam)"""

client.run(config.bot_token)
