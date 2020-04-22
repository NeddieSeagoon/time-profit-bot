import discord
from discord.ext import commands
from time import perf_counter
import datetime
import koios_discord_token as ktoken

from string import Template

#fucking why not go all in
class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

token = ktoken.token

bot = commands.Bot(command_prefix = '.')


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.command()
async def timer(ctx):
    '''Starts and stops a test timer.'''
    await ctx.send('Timer ready. Enter \'.start\' to start.')
    
    def start_check(m):
        return m.content == '.start' and m.channel == ctx.channel and m.author == ctx.author

    def stop_check(m):
        return m.content == '.stop' and m.channel == ctx.channel and m.author == ctx.author

    msg = await bot.wait_for('message', check = start_check)
    start_time = msg.created_at
    print('Start time: ' + str(start_time))
    await ctx.send('Timer started. Enter \'.stop\' to stop.')

    msg = await bot.wait_for('message', check = stop_check)

    stop_time = msg.created_at
    print('Stop time: ' + str(stop_time))
    timer_duration = (stop_time - start_time)
    timer_duration = strfdelta(timer_duration,'%H:%M:%S')
    await ctx.send('Timer stopped. Total time was: ' + timer_duration)

@bot.command()
async def pt(ctx, ):
    '''Takes wallet inputs and times mission to determine profit/time.'''

    #checks
    def wallet_check(m):
        return m.content.startswith('uec ') and m.channel == ctx.channel and m.author == ctx.author

    def generic_check(m):
        return m.content == '.' and m.channel == ctx.channel and m.author == ctx.author
    
    #get starting wallet
    await ctx.send('Please enter wallet amount as \'uec <amount>\'')
    msg = await bot.wait_for('message', check = wallet_check)
    wallet_start = msg.content
    await ctx.send('Starting wallet stored. Enter \'.\' to start timer.')

    msg = await bot.wait_for('message', check = generic_check)
    timer_start = msg.created_at







bot.run(token)
