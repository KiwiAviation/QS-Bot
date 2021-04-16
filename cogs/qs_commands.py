### Cog with commands specifically used for QS discord.

import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class QSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # recruit msg ids
        self.react_message_id = 720375316064763965 # test: 720375316064763965, real: 608312261668241428
        self.recruit_channel_id = 720375276583780414 # test: 720375276583780414, real: 644768028457697280
        self.saved_channel_id = 720680732556656660 # test: 720680732556656660, real: 675346796515557420
        
        # acceptence msg ids
        self.employee_channel_id = 832725613503709224 # test: 832725613503709224, real: 608038955421794305
        
        # emojis
        self.recruit_target_emoji = '\U0001f4bc' # :briefcase:
        self.saved_target_emoji = '\U00002705' # :white_check_mark:

        # feedback channel ids
        self.feedback_channel_id = 818892761474138112 # test: 818890198690562088, real: 818892761474138112
           
    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        # Check if message is sent in relevant channel
        if message.channel == self.bot.get_channel(self.recruit_channel_id):
            # Make sure message is not from bot
            if message.author != self.bot.user:
                # Save message in designated channel
                self.saved_msg = await self.bot.get_channel(self.saved_channel_id).send(
                    f"Sent by **{message.author}**, {message.author.id}\n{message.content}")
                await self.saved_msg.add_reaction(self.saved_target_emoji)
                
                # Send receipt
                receipt = await self.bot.get_channel(self.recruit_channel_id).send(
                    "Your message has been succesfully logged. Please wait for a manager to review your "
                    "application! *All previous messages will delete in 60 seconds*")
                
                # DM message saved conformation
                await message.author.send(
                    f"Your {self.bot.get_channel(644768028457697280).mention} application has been "
                    "succesfully saved. Please wait for a manager to review your application! *Your "
                    "message in #recruit will be deleted to reduce clutter*")

                # Check for purge, make sure messages are the one we want to delete
                def should_del(m):
                    return m.author == member or m.author == self.bot.user

                # Delete last 3 messages
                await asyncio.sleep(60.0)
                await self.bot.get_channel(self.recruit_channel_id).purge(
                    limit=3,check=should_del,after=datetime(2021, 3, 1, 0, 0),oldest_first=False)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.react_message_id: # Message in #roles

            if payload.emoji.name != self.recruit_target_emoji:
                return
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                return

            # Ping in #recruit here
            self.ping_message = await guild.get_channel(self.recruit_channel_id).send(
                f"Thank you for expressing interest in our faction {member.mention}!\nPlease follow the "
                "above instructions to complete the joining process.")

        elif payload.message_id == self.saved_msg.id: # Message in #saved-recruit
            
            if payload.emoji.name != self.saved_target_emoji:
                return
            
            guild = self.bot.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return
            
            member = guild.get_member(payload.user_id)
            if member is None:
                # Makes sure the member still exists and is valid
                return
            elif member.id == self.bot.user.id:
                # Makes sure message is not from QSBot
                return

            #await guild.get_channel(self.employee_channel_id).send(f'Your recruit application has been accepted! Welcome to the company {}! Choose division roles in {}, and learn more about the game and our company in {} and {}!')
            

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
            if self.ping_message:
                await self.ping_message.delete()

    @commands.command()
    async def feedback(self, ctx):
        def check(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        if ctx.guild != None:
            await ctx.send("Feedback is a DM only command")
        else:
            await ctx.send(
                "Your next message will be recorded as your feedback. Type 'cancel' if you wish to cancel "
                "your feedback. Feedback is anonymous and will be stored in a private feedback channel")

            try:
                msg = await self.bot.wait_for('message', timeout=300.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out. If you still wish to give feedback, resend the feedback command")
            else:
                if msg.content.lower() == "cancel" or msg.content.lower() == "'cancel'":
                    await ctx.send("Feedback succesfully canceled")
                else:
                    # record feedback in channel
                    await self.bot.get_channel(self.feedback_channel_id).send(
                        f"**Anonymous Feedback**\n{msg.content}")

                    # Send submitter feedback confirmation message
                    await ctx.send(
                        "Feedback succesfully logged. Thanks for helping to improve Quasar Systems!")

     
def setup(bot):
    bot.add_cog(QSCog(bot))