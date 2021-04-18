import discord
from discord.ext import commands
import youtube_dl
import os
from asyncio import sleep

import sqlalchemy

from data import db_session
from data.member import Member

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'False'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

bot = commands.Bot(command_prefix='.')


# db_session.global_init("db/blogs.db.sqlite")


class COM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='work')
    @commands.has_permissions(administrator=True)
    async def work(self, ctx):
        await ctx.send('Бот работает!')

    @commands.command(name='Hi')
    async def Hi(self, ctx):
        await ctx.send('Hi')

    @commands.command(name='clear')
    async def clear(self, ctx, amount=20):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=discord.Embed(title='Исключение', description=f"""Кикнут: {user.mention} \n
                Кикнулл: {ctx.author.mention} \n
                Причина: {reason}""", color=0x969696))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await user.ban(reason=reason)
        await ctx.send(embed=discord.Embed(title='Бан', description=f"""Забанен: {user.mention} \n
                Забанил: {ctx.author.mention} \n
                Причина: {reason}""", color=0x969696))

    @commands.command()
    async def join(self, ctx, url: str):
        global vc
        channel = ctx.message.author.voice.channel
        await ctx.channel.purge(limit=1)
        if channel:
            vc = await channel.connect()

    # @commands.command()
    # async def play(self, ctx, url: str):
    #     global vc
    #     song = os.path.isfile('song.mp3')
    #     channel = ctx.message.author.voice.channel
    #     await ctx.channel.purge(limit=1)
    #     if channel:
    #         vc = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        server = ctx.message.guild.voice_client
        await server.disconnect()
        await ctx.channel.purge(limit=1)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Real Life', type=3))  # статус


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
    token = 'ODMwNzQ3MTY0MDY1NTI5ODg2.YHLLlg.Q7cIJvLoL44m3OK8drZ4Xqu5ajE'
    bot.add_cog(COM(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
