import discord
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
        global vc
        await ctx.channel.purge(limit=1)
        try:
            channel = ctx.message.author.voice.channel
            if channel:
                vc = await channel.connect()
        except Exception:
            return

    @commands.command()
    async def pause(self, ctx):  # пауза войс чата(готово)
        global vc
        await ctx.channel.purge(limit=1)
        try:
            if vc.is_playing:
                vc.pause()
            else:
                await ctx.send("Currently no audio is playing.")
        except Exception:
            return

    @commands.command()
    async def resume(self, ctx):  # пауза войс чата(готово)
        global vc
        await ctx.channel.purge(limit=1)
        try:
            vc.resume()
        except Exception:
            return

    # @commands.command()
    # async def youtube(self, ctx, *, search):  # поиск видео на youtube(не готово)
    #     req = requests.get(search)

    @commands.command()
    async def play(self, ctx, url: str):  # проигрывание музыки(готово)
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

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
        sound = discord.FFmpegPCMAudio("song.mp3")
        voice.play(sound)

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
    token = 'ODMwNzQ3MTY0MDY1NTI5ODg2.YHLLlg.WK8OKBV2LhF-wvosMU1u8oaqq2g'
    bot.add_cog(COM(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
