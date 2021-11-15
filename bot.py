import discord
from discord.ext import commands
import youtube_dl
import random
import os
import time
import threading
import numpy as np

class Player:
    def __init__(self):
        self.musicDirectory  = "C:\\Users\\zames\\Documents\\Python\\Bot Test\\MD\\"
        self.nowPlaying      = ""
        self.dirList         = [ ]
        self.queue           = [ ]
        self.dirList = os.listdir(self.musicDirectory)
        self.queue   = np.array(self.dirList)
        self.counter = 0
        self.stop    = 0
        self.voice   = 0
        self.ctx     = 0

    def play(self, error=None):
        self.counter += 1
        self.voice.play(discord.FFmpegPCMAudio(self.musicDirectory + self.queue[self.counter]), after = self.play)
        return
        
    def shuffle():        
        self.queue = np.asarray(self.dirList)
        random.shuffle(self.queue)

        
player = Player()

client = discord.Client()

client = commands.Bot(command_prefix="!")

@client.event
async def on_guild_join(guild):
    if guild.id != 704420524863913985:
        await guild.leave()

@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    region = str(ctx.guild.region)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
            title=name + " Server Information",
            description= description,
            color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID:", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount,inline=True)

    await   ctx.send(embed=embed)

@client.command()
async def update(ctx, playlist : str):
    if(os.path.isdir(player.musicDirectory + playlist)):
        if(os.path.isfile(player.musicDirectory + playlist + "\\playlist.txt")):
            fplst = open(player.musicDirectory + playlist + "\\playlist.txt", "r")
            ytadress = fplst.readline()
            await ctx.send(ytadress)
            ydl_opts = {
            'download_archive' : player.musicDirectory + playlist + '\songlist.txt',
            'outtmpl' : player.musicDirectory + playlist + '\%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([ytadress])
            await ctx.send("Playlist updated!")
        else:
            await ctx.send("Can't update playlist. Playlist file isn't exist!")
    else:
        await ctx.send("Can't update playlist. Playlist isn't exist!")
    
@client.command()
async def gachi(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    
    player.voice = voice
    player.ctx = ctx
    voice.play(discord.FFmpegPCMAudio(player.musicDirectory + player.queue[player.counter]), after = player.play)

@client.command()
async def shuffle(ctx):
    
    np.random.shuffle(player.queue)
    counter = 0
    await ctx.send("queue has been shuffled!")

@client.command()
async def queue(ctx):
    embed = discord.Embed(
            title= "Queue",
            description= "Playing",
            color=discord.Color.blue()
    )
    for i in range(1, 9):
        embed.add_field(name=i, value=player.queue[player.counter + i], inline=True)
    await   ctx.send(embed=embed)

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel")

@client.command()
async def pause(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
                await ctx.send("Currently no audio is playing.")

                
@client.command()
async def resume(ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio isn't paused.")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


client.run('ODk5NjQ5Njk2NjM1NzExNDk4.YW12Eg.qQeKRZGuruBrazdIqwOzDOC_HdA')
