import discord
from data import db_session
from discord.ext import commands
import random
from discord.utils import get

bot = commands.Bot(command_prefix='.')


class COM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='randint')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name='work')
    @commands.has_permissions(administrator=True)
    async def work(self, ctx):
        await ctx.send('Бот работает!')

    @commands.command(name='Hi')
    async def Hi(self, message):
        await message.send('Hi')

    @commands.command(name='clear')
    async def clear(self, message, amount=20):
        await message.channel.purge(limit=amount)

    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()


# @commands.command()
# @commands.has_permissions(administrator=True)
# async def kick(self):  Код для кика участиков сервера

# @commands.command()
# @commands.has_permissions(administrator=True)
# async def ban(self):  Код для бана участиков сервера


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name='Real Life', type=3))  # статус


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    txt = message.content.lower()
    if 'привет' in txt:
        await message.channel.send('Ку')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет, {member.name}!'
    )


def main():
    token = 'ODMwNzQ3MTY0MDY1NTI5ODg2.YHLLlg.Q7cIJvLoL44m3OK8drZ4Xqu5ajE'
    bot.add_cog(COM(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
