### Cog with commands specifically used for QS discord.

import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class QSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # guild id
        self.server_id = 599242121857204224 # test: 720130817120010240 real: 599242121857204224
        
        # recruit msg ids
        self.react_message_id = 608312261668241428 # test: 720375316064763965, real: 608312261668241428
        self.recruit_channel_id = 644768028457697280 # test: 720375276583780414, real: 644768028457697280
        self.saved_channel_id = 675346796515557420 # test: 720680732556656660, real: 675346796515557420
        
        # acceptence msg ids
        self.employeeChat_channel_id = 608038955421794305 # test: 832725613503709224, real: 608038955421794305
        self.employeeRoles_channel_id = 654158920746663948 # test: 720130817120010243 real: 654158920746663948
        self.newPlayerInfo_channel_id = 732340588434948126 # test: 727620147514441849 real: 732340588434948126
        self.ourCompany_channel_id = 666104050051448853 # test: 818890198690562088 real: 666104050051448853
        
        # role ids
        self.leader_role_id = 599247628408193043 # test: 833012981532983336 real: 599247628408193043
        self.recruit_role_id = 605596516677320724 
        self.employee_role_id = 644766752907198464
        self.novice_role_id = 724045356635258920

        # emojis
        self.recruit_target_emoji = '\U0001f4bc' # :briefcase:
        self.saved_target_emoji = '\U00002705' # :white_check_mark:

        # feedback channel ids
        self.feedback_channel_id = 818892761474138112 # test: 818890198690562088, real: 818892761474138112
           
        # Other objects
        self.saved_msg_user = (0,0) # [0] is message object, [1] is applicant object
        self.ping_message = None

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        # Check if message is sent in relevant channel
        if message.channel == self.bot.get_channel(self.recruit_channel_id):
            # Make sure message is not from bot
            if message.author != self.bot.user:
                # Save message in designated channel
                self.saved_msg_user = (await self.bot.get_channel(self.saved_channel_id).send(
                    f"Sent by **{message.author}**, {message.author.id}\n{message.content}"), 
                    message.author)
                await self.saved_msg_user[0].add_reaction(self.saved_target_emoji)
                
                # Send receipt
                receipt = await self.bot.get_channel(self.recruit_channel_id).send(
                    "Your message has been succesfully logged. Please wait for a manager to review your "
                    "application! *All previous messages will delete in 60 seconds*")
                
                # DM message saved conformation
                await message.author.send(
                    f"Your {self.bot.get_channel(self.recruit_channel_id).mention} application has been "
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

        elif payload.message_id == self.saved_msg_user[0].id: # Message in #saved-recruit
            
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
            elif member.top_role.id != self.leader_role_id:
                # Makes sure user has top role
                return

            # send acceptence message
            await guild.get_channel(self.employeeChat_channel_id).send(
                f"Your recruit application has been accepted! Welcome to the company "
                f"{self.saved_msg_user[1].mention}! Choose division roles in "
                f"{self.bot.get_channel(self.employeeRoles_channel_id).mention}, and learn more about the "
                f"game and our company in {self.bot.get_channel(self.newPlayerInfo_channel_id).mention} and "
                f"{self.bot.get_channel(self.ourCompany_channel_id).mention}!")
            
            # remove recruit role
            async self.saved_msg_user[1].remove_roles(
                self.bot.get_guild(self.server_id).get_role(self.recruit_role_id)
            )

            # add employee and novice role
            async self.saved_msg_user[1].add_roles(
                self.bot.get_guild(self.server_id).get_role(self.employee_role_id),
                self.bot.get_guild(self.server_id).get_role(self.novice_role_id)
            )
            

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
            if self.ping_message != None:
                try:
                    await self.ping_message.delete()
                except discord.errors.NotFound:
                    pass

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