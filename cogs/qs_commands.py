### Cog with commands specifically used for QS discord.

import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class QSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.react_message_id = 720375316064763965
        self.target_channel1_id = 720375276583780414
        self.target_channel2_id = 720680732556656660
        self.emoji_role_pairs = {
            '💼' : 728365952449904741
        }
        
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        # Check if message is sent in relevant channel
        if message.channel == self.bot.get_channel(self.target_channel1_id):
            # Make sure message is not from bot
            if message.author != self.bot.user:
                # Save message in designated channel
                await self.bot.get_channel(self.target_channel2_id).send(f'Sent by **{message.author}**\n{message.content}')
                
                # Send receipt
                receipt = await self.bot.get_channel(self.target_channel1_id).send("Your message has been succesfully logged. Please wait for a manager to review your application! *All previous messages will delete in 60 seconds*")

                # Check for purge, make sure messages are the one we want to delete
                def should_del(m):
                    return m.author == member or m.author == self.bot.user

                # Delete last 3 messages
                await asyncio.sleep(60.0)
                await self.bot.get_channel(self.target_channel1_id).purge(limit=3,check=should_del,after=datetime(2021, 3, 1, 0, 0),oldest_first=False)

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
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                return

            # Ping in #recruit here
            await guild.get_channel(self.target_channel1_id).send(f'Welcome to the company {member.mention}!\nPlease follow the above instructions to complete the joining process.')
            

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