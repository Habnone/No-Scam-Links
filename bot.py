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
    except discord.HTTPException:
        print('Failed deleting message')

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
        except discord.Forbidden:
            print("I don't have the proper permissions to delete the message")
        except discord.NotFound:
            print('This message was already deleted by someone else')
        except discord.HTTPException:
            print('An error occured while tried deleting that message. I will retry 1 time')
            await del_message(message)

        #Kicks the member from your server (remove # to enable)
        #await message.author.kick(reason="malicious link")

        #Bans the member from your server (remove # to enable)
        #await message.author.ban(reason='malicious link', delete_message_days=1)

bot.run('BOT TOKEN HERE')
