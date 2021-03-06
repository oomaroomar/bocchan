import os
import json
from discord.ext import commands
from discord.ext.tasks import loop
from discord import File, utils
from utils import printJSON, NotEnoughSongsError
from spotify import SpotifyIndex
from dotenv import load_dotenv
from temp_monitor import get_tempgraph_path, monkaS_temp
import requests


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
sp = SpotifyIndex()

moderators = None


@bot.command('catJAM')
async def cat_jam(ctx, *args):
    await ctx.message.delete()
    header = ''
    for arg in args:
        header = header + ' ' + arg
    await ctx.send(f'{header}', file=File('./media/catJAM.gif'))


@bot.command('FerretLOL', aliases=["<:FerretLOL:800680344319295488>"])
async def random_ferret(ctx):
    if '<' not in ctx.message.content:
        await ctx.message.delete()
    r = requests.get('https://polecat.me/api/ferret').text
    rf = json.loads(r)['url']
    await ctx.send(rf)


@bot.command(name='songsuggest', aliases=['ss', 'suggest'])
async def songSuggest(ctx, dUser='everyone', count=1):
    print(
        'in song suggest with arguments: \n ctx: {ctx} \n dUser: {dUser} \n count: {count}')
    if count > 15:
        count = 15
        await ctx.send('You can only ask for 15 songs at a time')
    if dUser == 'lofi':
        dUser = 'ChilledCow'
    if dUser == 'everyone':
        try:
            response = sp.get_track_from_collective_playlist(count)
            await ctx.send(f'Here are some tracks from your friends\'s playlists')
            for track in response:
                await ctx.send(track)
            return
        except NotEnoughSongsError as neserr:
            await ctx.send(neserr.message)
    try:
        response = sp.get_track_from_user_playlist(dUser, count)
        await ctx.send(f'Here are some tracks from {dUser}\'s playlist')
        for track in response:
            await ctx.send(track)
        return
    except IndexError as ierr:
        await ctx.send(f'{dUser} doesn\' have {count} tracks in their playlist')
        return
    except TypeError as terr:
        await ctx.send(f'{dUser} doesn\'t have a playlist')
        return


@bot.command(name='mylist', aliases=['ml', 'myplaylist', 'playlist', 'mp'],
             help='Displays your playlist if called with no arguments. Sets it if provided a valid spotify playlist')
async def myList(ctx, *args):
    # Get users playlist
    if(len(args) > 1):
        await ctx.send(f'You provided {len(args) - 1} too many arguments')
        return
    if(len(args) < 1):
        response = sp.get_playlist(ctx.author.name)
        if response == None:
            await ctx.send('You haven\'t set yourself a playlist. To do so type ``.mylist playlistURI`` where ``playlistURI`` is the uri of your playlist')
            return
        await ctx.send(response)
        print(ctx.author)
        return
    # Set users playlist
    try:
        response = sp.add_playlist(ctx.author.name, args[0])
        await ctx.send(response)
    except Exception as err:
        await ctx.send(f'Playlist of uri {args[0]} doesn\'t exist')


@bot.event
async def on_ready():
    global moderators
    print(
        f'{bot.user} has connected to Discord!\n \n'
        'Connected to following guilds:'
    )
    for guild in bot.guilds:
        print(f'{guild.name}(id: {guild.id})')
        print(f'Spotify playlists: {sp.get_playlists()}')
        moderators = utils.get(guild.roles, id=288748781841809409)


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')


@loop()
async def temp_logger():
    # Not sure what this does. Probably gives other functions priority over it.
    channel = bot.get_channel(789164708133339157)  # XDD
    while True:
        log, worrysome = await get_tempgraph_path()
        if worrysome:
            await channel.send(f'{moderators.mention} temps over {monkaS_temp}', file=File(log))
        else:
            await channel.send(file=File(log))


@temp_logger.before_loop
async def temp_logger_before():
    await bot.wait_until_ready()


temp_logger.start()

bot.run(DISCORD_TOKEN)
