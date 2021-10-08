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

@bot.event
async def on_ready():
    print("Bot is ready!")
    bot.banned_links = await getlinks()

#Checks if message has a malicious link
@bot.event
async def on_message(message):
    if any(i in message.content for i in bot.banned_links):
        #Deletes the message (recommended  to keep enabled)
        await message.delete()

        #Kicks the member from your server (remove # to enable)
        #await message.author.kick(reason="malicious link")

        #Bans the member from your server (remove # to enable)
        #await message.author.ban(reason='malicious link', delete_message_days=1)

bot.run('BOT TOKEN HERE')
