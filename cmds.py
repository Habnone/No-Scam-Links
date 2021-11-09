from discord.ext import commands
from datetime import datetime

def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

class cmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(f'{get_current_time()} | Loaded the main cog')
    
    @commands.command
    async def info(self, ctx):
        await ctx.reply('This is a placeholder command')

def setup(bot):
    bot.add_cog(cmds(bot))