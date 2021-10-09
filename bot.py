import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp

#set the bot variable
bot = commands.Bot(command_prefix = '')

#Gets a list of scam domains
async def getlinks():

    async with aiohttp.ClientSession() as session:

        banned_links = 'https://api.hyperphish.com/gimme-domains'
        async with session.get(banned_links) as resp:
            links = await resp.json()
            return links

#Deletes a message:
async def del_message(msg):
    try:
        await msg.delete()
    except discord.HTTPException(response, message):
        print(f'Failed deleting message with ID : {message.id} for the second time')
    except discord.NotFound(response, message):
        print(f'The message with ID : {message.id} was already deleted')
    else:
        print('Second attempt to delete message with ID: {msg.id} was succesful')

@bot.event
async def on_ready():
    print('Fetching scam links list...')
    bot.banned_links = await getlinks()
    print("Bot is ready!")

#Checks if message has a malicious link
@bot.event
async def on_message(message):
    if any(i in message.content for i in bot.banned_links):
        #Deletes the message and print a console message if it fails (recommended  to keep enabled)
        try:
            await message.delete()
        except discord.Forbidden(response, msg):
            print(f"I don't have the proper permissions to delete the message with ID : {msg.id}")
        except discord.NotFound(response, msg):
            print(f'The message with ID : {msg.id} was already deleted by someone else')
        except discord.HTTPException(response, msg):
            print(f'An error occured while tried deleting the messagewith ID : {msg.id}. I will retry 1 time')
            await del_message(message)
        else:
            print(f'The message with ID : {message.id} was succesfully deleted')

        #Kicks the member from your server (remove # to enable)
        #await message.author.kick(reason="Malicious link")

        #Bans the member from your server (remove # to enable)
        #await message.author.ban(reason='Malicious link', delete_message_days=1)

#load the bot token from the "token" file
with open('token') as f:
    bot_token = f.read()

#run the bot
bot.run(bot_token)