### Cog with commands specifically used for QS discord.

import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class QSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.react_message_id = 608312261668241428 # test: 720375316064763965
        self.target_channel1_id = 644768028457697280 # test: 720375276583780414
        self.target_channel2_id = 675346796515557420 # test: 720680732556656660
        self.target_emoji = '💼'
           
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        # Check if message is sent in relevant channel
        if message.channel == self.bot.get_channel(self.target_channel1_id):
            # Make sure message is not from bot
            if message.author != self.bot.user:
                # Save message in designated channel
                await self.bot.get_channel(self.target_channel2_id).send(f'Sent by **{message.author}**, {message.author.id}\n{message.content}')
                
                # Send receipt
                receipt = await self.bot.get_channel(self.target_channel1_id).send("Your message has been succesfully logged. Please wait for a manager to review your application! *All previous messages will delete in 60 seconds*")
                await message.author.send("Your #recruit application has been succesfully saved. Please wait for a manager to review your application! *Your message in #recruit will be deleted to reduce clutter*")

                # Check for purge, make sure messages are the one we want to delete
                def should_del(m):
                    return m.author == member or m.author == self.bot.user

                # Delete last 3 messages
                await asyncio.sleep(60.0)
                await self.bot.get_channel(self.target_channel1_id).purge(limit=3,check=should_del,after=datetime(2021, 3, 1, 0, 0),oldest_first=False)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.react_message_id:

            if payload.emoji.name != self.target_emoji:
                print('Wrong emoji')
                return
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                print('Guild not found')
                return
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                print('Member not found')
                return

            # Ping in #recruit here
            await guild.get_channel(self.target_channel1_id).send(f'Thank you for expressing intrest in our faction {member.mention}!\nPlease follow the above instructions to complete the joining process.')
            

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.react_message_id:
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                return

            # Delete @ message

     
def setup(bot):
    bot.add_cog(QSCog(bot))