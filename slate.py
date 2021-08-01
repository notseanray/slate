import os, discord, json, asyncio, importlib
from rcon import rcon
from discord.ext import commands

#modules, uncomment to disable certain features


#config file
config_file = open("config.json", "r")
config_data = json.load(config_file)

bot = commands.Bot(command_prefix='$')

print("Hello world c;")

@bot.event
async def on_ready():
    print(f'logged in as {bot.user.name}#{bot.user.discriminator}\n'
          f'User ID: {bot.user.id}\n'
          f'Discord Lib Version: {discord.__version__} | {discord.version_info.releaselevel}\n')
    if config_data['discord_status']:
        bot.change_presence(activity=discord.Game(name=config_data['discord_status']))

@bot.event
async def on_message(message):
    if str(message.channel.id) == config_data['chat_bridge_id']:
        #print(message.author.name + ": " + message.content)
        chat_message = 'tellraw @a {"text": "[' + message.author.name + '] ' + message.content + '"}'
        await rcon(chat_message, host=config_data['host'], port=int(config_data['smp_rcon_port']), passwd=config_data['rcon_password'])
        #print(chat_message)

log_file = open("latest.log", "r")
lines = log_file.readlines()
async def read_logfile():
    while True:
        last_line = log_file.readlines()
        if len(last_line) > 0:
            print(str(last_line))
        await asyncio.sleep(1)
asyncio.run(read_logfile())

try:
    bot.run(config_data['token'])
except:
    print("invalid token, please check config.json")
