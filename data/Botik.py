import discord
import requests
from discord.ext import commands
import youtube_dl
import os

from discord.utils import get

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

bot = commands.Bot(command_prefix='.')


class COM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.song_data = []

    @commands.command(name='work')  # команда для отладки(готово)
    @commands.has_permissions(administrator=True)
    async def work(self, ctx):
        await ctx.send('Бот работает!')

    @commands.command(name='Hi')
    async def Hi(self, ctx):
        await ctx.send('Hi')

    @commands.command(name='clear')  # очистка чата(готово)
    async def clear(self, ctx, amount=20):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):  # исключение(готово)
        await ctx.channel.purge(limit=1)
        try:
            await user.kick(reason=reason)
            await ctx.send(embed=discord.Embed(title='Исключение', description=f"""Кикнут: {user.mention} \n
                Кикнулл: {ctx.author.mention} \n
                Причина: {reason}""", color=0x969696))
        except Exception:
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):  # бан(готово)
        await ctx.channel.purge(limit=1)
        try:
            await user.ban(reason=reason)
            await ctx.send(embed=discord.Embed(title='Бан', description=f"""Забанен: {user.mention} \n
                Забанил: {ctx.author.mention} \n
                Причина: {reason}""", color=0x969696))
        except Exception:
            return

    @commands.command()
    async def join(self, ctx):  # прсоединение к войс чату(готово)
        await ctx.channel.purge(limit=1)
        try:
            channel = ctx.message.author.voice.channel
            if channel:
                self.vc = await channel.connect()
        except Exception:
            return

    @commands.command()
    async def pause(self, ctx):  # пауза войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            if self.vc.is_playing:
                self.vc.pause()
                await ctx.send(embed=discord.Embed(title='Pause', description=f'write <<.resume>>', color=0x969696))
            else:
                await ctx.send("Currently no audio is playing.")
        except Exception:
            return

    @commands.command()
    async def resume(self, ctx):  # пауза войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            self.vc.resume()
        except Exception:
            return

    async def youtube(self, ctx, *, search):  # поиск видео на youtube(готово)
        API_KEY = 'AIzaSyCrbB2zI6dpRZTdNqWpbzDwVUP0Jyjz0tU'
        print(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q='
              f'{"%20".join(search.split())}&type=video&key={API_KEY}')
        req = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q='
                           f'{"%20".join(search.split())}&type=video&key={API_KEY}')
        req = req.json()
        id = f"https://www.youtube.com/watch?v={req['items'][0]['id']['videoId']}"
        await ctx.send(id)
        await self.play(ctx, id)

    @commands.command()
    async def play(self, ctx, *, search):  # проигрывание музыки(готово)
        API_KEY = 'AIzaSyCrbB2zI6dpRZTdNqWpbzDwVUP0Jyjz0tU'
        print(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q='
              f'{"%20".join(search.split())}&type=video&key={API_KEY}')
        req = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&q='
                           f'{"%20".join(search.split())}&type=video&key={API_KEY}')
        req = req.json()
        url = f"https://www.youtube.com/watch?v={req['items'][0]['id']['videoId']}"
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send(embed=discord.Embed(title='ERROR', description="ERROR: Music playing", color=0x969696))
            return

        await ctx.send(embed=discord.Embed(description="Getting everything ready now", color=0x969696))

        voice = get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(etx)s',
            'quiet': False
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
        sound = discord.FFmpegPCMAudio('song.mp3')
        voice.play(sound)
        await ctx.channel.purge(limit=2)
        await ctx.send(embed=discord.Embed(title='Music', description=f'Now playing: {name}', color=0x969696))
        await ctx.send(url)

    @commands.command()
    async def stop(self, ctx):  # стоп войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            self.vc.stop()
        except Exception:
            return

    @commands.command()
    async def leave(self, ctx):  # отсоединение от войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
        except Exception:
            return


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Real Life', type=3))  # статус в Discord


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(832632474017464340)
    await channel.send(emb=discord.Embed(description=f'Пользователь {member.name}, присоединился к нам!'))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    txt = message.content.lower()
    if 'привет' in txt:
        await message.channel.send('Ку')


def main():
    token = 'ODMwNzQ3MTY0MDY1NTI5ODg2.YHLLlg.EfK7NNTzRuo0dKg5Ey36Hbh4w8g'
    bot.add_cog(COM(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
