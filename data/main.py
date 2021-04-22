import discord
import requests
from discord.ext import commands
import youtube_dl
import os
from discord.utils import get
from data.__all_models import *

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
COMMAND_LIST = ['kick', 'ban', 'help', 'join', 'stop', 'play', 'resume', 'leave', 'pause', 'Hi', 'clear']

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
with db:
    db.create_tables([Member])


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

    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(title='Help')
        em.add_field(name='Moderation', value='Kick, Ban, Clear')
        em.add_field(name='Play Music', value='Play, Stop, Pause, Resume, Join')

        await ctx.send(embed=em)

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
            await ctx.channel.send(embed=discord.Embed(title='ERROR', description=
            f'{ctx.message.author.mention}, Вы уже в голосовом чате'))
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
            await ctx.channel.send(embed=discord.Embed(title='ERROR', description=
            f'{ctx.message.author.mention}, Вы не находитесь в голосовом чате'))
            return

    @commands.command()
    async def resume(self, ctx):  # пауза войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            self.vc.resume()
        except Exception:
            await ctx.channel.send(embed=discord.Embed(title='ERROR', description=
            f'{ctx.message.author.mention}, Вы не находитесь в голосовом чате'))
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

        await ctx.send(embed=discord.Embed(description="Please Wait", color=0x969696))

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
            await ctx.channel.send('Музыка не играет')
            return

    @commands.command()
    async def leave(self, ctx):  # отсоединение от войс чата(готово)
        await ctx.channel.purge(limit=1)
        try:
            server = ctx.message.guild.voice_client
            await server.disconnect()
        except Exception:
            await ctx.channel.send(embed=discord.Embed(title='ERROR', description=
            f'{ctx.message.author.mention}, Вы не находитесь в голосовом чате'))
            return


@bot.event
async def on_ready():
    print(f'{bot.user} подключен к Discord!')
    for guild in bot.guilds:
        print(
            f'{bot.user} подключились к чату:\n'
            f'{guild.name}(id: {guild.id})'
        )
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Real Life', type=3))  # статус в Discord


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}!'
    )
    role = discord.utils.get(member.guild.roles, id=834000820295041024)
    await member.add_roles(role)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    txt = message.content.lower()
    if message.author == bot.user:
        return
    if 'привет' in txt:
        await message.channel.send('Ку')
        return
    with db:
        try:
            user = Member.select().where(Member.name == message.author)[0]
            n = user.lvl
            if int((n * 10) % 10) == 0:
                await message.channel.send(embed=discord.Embed(title='Достижение',
                                                               description=f'{message.author.mention}'
                                                                           f' достиг {int(n)} уровня'))
            user.delete_instance()
            Member.create(name=message.author, lvl=round(n + 0.1, 1))
        except Exception:
            Member.create(name=message.author, lvl=0.1)


def main():
    with open('Token.txt', 'rt') as f:
        token = f.read()
    bot.add_cog(COM(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
