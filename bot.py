import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp
import sys
from datetime import datetime

#set the bot variable
bot = commands.Bot(command_prefix = '')

async def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

#Gets a list of scam domains every 5 minutes
@tasks.loop(seconds=300.0)
async def getlinks():
    print(f'{await get_current_time()} | Fetching scam links list...')
    
    async with aiohttp.ClientSession() as session:

        banned_links = 'https://api.hyperphish.com/gimme-domains'
        async with session.get(banned_links) as resp:
            links = await resp.json()
            print(f'{await get_current_time()} | Got scam links data. Dumping them into a variable...')
            bot.banned_links = links
            print(f'{await get_current_time()} | Dumbing done')

#Deletes a message:
async def del_message(msg):
    try:
        await msg.delete()
    except discord.HTTPException(response, message):
        print(f'{await get_current_time()} | Failed deleting message with ID : {message.id} for the second time')
    except discord.NotFound(response, message):
        print(f'{await get_current_time()} | The message with ID : {message.id} was already deleted')
    else:
        print(f'{await get_current_time()} | Second attempt to delete message with ID: {msg.id} was succesful')

@bot.event
async def on_ready():
    getlinks.start()
    #bot.banned_links = await getlinks()
    print(f"{await get_current_time()} | Bot is ready!")

# Checks if message has a malicious link
@bot.event
async def on_message(message):
    if any(i in message.content for i in bot.banned_links):
        #Deletes the message and print a console message if it fails (recommended  to keep enabled)
        try:
            await message.delete()
        except discord.Forbidden(response, msg):
            print(f"{await get_current_time()} | I don't have the proper permissions to delete the message with ID : {msg.id}")
        except discord.NotFound(response, msg):
            print(f'{await get_current_time()} | The message with ID : {msg.id} was already deleted by someone else')
        except discord.HTTPException(response, msg):
            print(f'{await get_current_time()} | An error occured while tried deleting the message with ID : {msg.id}. I will retry 1 time')
            await del_message(message)
        else:
            print(f'{await get_current_time()} | The message with ID : {message.id} was succesfully deleted')

        #Kicks the member from your server (remove # to enable)
        #await message.author.kick(reason="Malicious link")

        #Bans the member from your server (remove # to enable)
        #await message.author.ban(reason='Malicious link', delete_message_days=1)

# load the bot token from the "token" file
with open('token') as f:
    if f.read() == 'ENTER BOT TOKEN HERE':
        sys.exit('No token found in file "token"')
    else:
        f.seek(0)
        bot_token = f.read()


# run the bot
bot.run(bot_token)