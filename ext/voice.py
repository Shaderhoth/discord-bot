import discord
import youtube_dl
from discord.ext import commands
import aiohttp
import os
import asyncio
from ext.database import database
import random
import functools


class voice:
    def __init__(self, client):
        self.client = client
        
#---------------------------------------------YOUTUBE---------------------------------------------------------------------------------
    @commands.command()
    async def ytdl(self, ctx, url, Cext="mp3"):
        msg = await ctx.send("Nep is trying her hardest to get your file. https://i.kym-cdn.com/photos/images/original/001/283/141/58e.gif")
        name = random.getrandbits(64)
        if Cext == "mp4":
            Cext = "mp4"
            process = await asyncio.create_subprocess_shell("youtube-dl --prefer-ffmpeg --no-playlist --default-search \"ytsearch\" -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio' --merge-output-format mp4 --add-metadata -o {}.mp4 \"{}\"".format(name, url), stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        else:
            Cext = "mp3"
            args = "youtube-dl -v --no-playlist --default-search \"ytsearch\" --format \"bestaudio[ext=m4a]\" --extract-audio --audio-format mp3 -o {name}{ext} \"{url}\"".format(name=name,url=url, ext=r".%(ext)s")
            process = await asyncio.create_subprocess_shell(args, stdout=asyncio.subprocess.PIPE)
            await process.communicate()
        with open(f"{name}.{Cext}", "rb") as f:
            await database.sendFile(self, ctx, f)
        os.remove(f"{name}.{Cext}")
        await msg.delete()

 


def setup(client):
    discord.opus.load_opus("vendor/lib/libopus.so.0")
    if discord.opus.is_loaded():
        print("Opus loaded!")
    client.add_cog(voice(client))
