### Cog with commands specifically used for QS discord.

import discord
from discord.ext import commands

class QSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.react_message_id = 720375316064763965
        self.emoji_role_pairs = {
            '💼' : 728365952449904741
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.react_message_id:
            try:
                role_id = self.emoji_role_pairs[payload.emoji.name]
            except KeyError as k:
                print('KeyError', k)
                return
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return

            role = guild.get_role(role_id)
            if role is None:
                # Make sure the role still exists and is valid.
                return

            # Ping in #recruit here

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.react_message_id:
            try:
                role_id = self.emoji_role_pairs[payload.emoji.name]
            except KeyError as k:
                print('KeyError', k)
                return
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return

            role = guild.get_role(role_id)
            if role is None:
                # Make sure the role still exists and is valid.
                return
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                return

            # Delete @ message

     
def setup(bot):
    bot.add_cog(QSCog(bot))