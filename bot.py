import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp

#Command prefix
client = commands.Bot(command_prefix = '!')

#Gets a list of scam domains
async def getlinks():

    async with aiohttp.ClientSession() as session:

        banned_links = 'https://api.hyperphish.com/gimme-domains'
        async with session.get(banned_links) as resp:
            links = await resp.json()
            return links

@client.event
async def on_ready():
    print("Bot is ready!")
    client.banned_links = await getlinks()

#Checks if message has a malicious link
@client.event
async def on_message(message):
    if any(i in message.content for i in client.banned_links):
        #Deletes the message (recommended  to keep enabled)
        await message.delete()

        #Kicks the member from your server (remove # to enable)
        #await message.author.kick(reason="malicious link")

        #Bans the member from your server (remove # to enable)
        #await message.author.ban(reason='malicious link', delete_message_days=1)

client.run('BOT TOKEN HERE')
