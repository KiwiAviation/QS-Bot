### Main code for Quasar Systems Bot

import discord
from discord.ext import commands
import json

# Get token from hidden json
with open('config.json', 'r') as file:
    tokenData = file.read()
tokenObj = json.loads(tokenData)
token = str(tokenObj['token'])

# Set intents
intents = discord.Intents.default()
intents.members = True

# Set description
description = '''Simple Bot for Quasar Systems. Made by KiwiAviation using discord.py'''

# Create bot object
bot = commands.Bot(command_prefix ='.', description=description, intents = intents, help_command=None, activity=discord.Game(name='.help'))

# Create list of cogs
initial_extensions = [
    'cogs.basic_commands',
    'cogs.qs_commands',
]

# Load cogs
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------')

@bot.command()
async def help(ctx):
    """Help command. Shows descriptions for all commands."""
    helpEmbed = discord.Embed(title= 'Help Menu', description= '''
*List of commands*:
**ping** - Get my current ping
**support** - DM support information
**source** - get a link to my source code

*DM only commands*
**feedback** - Give anonymous feedback to the leaders of QS
''',colour=(discord.Colour.from_rgb(222, 0, 243)))

    await ctx.send(content=None, embed=helpEmbed)

# Run the bot
bot.run(token)