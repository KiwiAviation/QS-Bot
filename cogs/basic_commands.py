### Basic cog with ping, support, and source commands

import discord
from discord.ext import commands

class BasicCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.content == "yo":
            await message.channel.send("yo")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'My ping is: **{self.bot.latency:.4f}ms**')

    @commands.command()
    async def support(self, ctx):
        await ctx.author.send('For bot support, please contact `KiwiAviation#0645`')

    @commands.command()
    async def source(self, ctx):
        await ctx.send("Check out my source code!\nhttps://github.com/KiwiAviation/QS-Bot")

def setup(bot):
    bot.add_cog(BasicCommandsCog(bot))