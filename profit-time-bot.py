import discord
from discord.ext import commands
from time import perf_counter
import datetime
import koios_discord_token as ktoken
import regex as re

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
async def pt(ctx, round_trip = 'n'):
    '''Takes wallet inputs and times mission to determine profit/time.'''

    #checks
    def wallet_check(m):
        return m.content.startswith('uec ') and m.channel == ctx.channel and m.author == ctx.author

    def dot_check(m):
        return m.content == '.' and m.channel == ctx.channel and m.author == ctx.author
    
    #get starting wallet
    await ctx.send('Please enter wallet amount as \'uec <amount>\'')
    wallet_start_msg = await bot.wait_for('message', check = wallet_check)
    wallet_start = wallet_start_msg.content
    #strip non-numbers from message content
    wallet_start = re.sub("[^0-9]", "", wallet_start)


    await ctx.send('Starting wallet stored. Enter \'.\' to start timer.')

    #wait for command to start timer
    msg = await bot.wait_for('message', check = dot_check)
    #get timer start time
    timer_start = msg.created_at

    
    await ctx.send('Timer started. Enter \'.\' when mission objective is complete.')
    #get mission completion time
    obj_complete_msg = await bot.wait_for('message', check = dot_check)

    #round trip
    if round_trip == '-r':
        await ctx.send('Mission objective time logged. Enter \'.\' when back at start.')
        #get timer stop time
        end_rt_msg = await bot.wait_for('message', check = dot_check)
        timer_stop = end_rt_msg.created_at

    #one-way trip
    else:
        #set timer_stop to objective completion time
        timer_stop = obj_complete_msg.created_at

    
    duration = timer_stop - timer_start

    #get timedelta in seconds for profit-per-minute calculation
    duration_seconds = duration.total_seconds()

    #convert timedelta into pretty string
    duration = strfdelta(duration,'%H:%M:%S')

    await ctx.send('Timer stopped. Total time was: ' + str(duration) + '. Enter new wallet amount as \'uec <amount>\'')

    #get new wallet amount
    wallet_stop_msg = await bot.wait_for('message', check = wallet_check)
    wallet_stop = wallet_stop_msg.content

    #strip non-numbers from message contents
    wallet_stop = re.sub("[^0-9]", "", wallet_stop)

    profit = int(wallet_stop) - int(wallet_start)

    profit_per_minute = profit / (duration_seconds / 60)
    profit_per_minute = profit_per_minute // 1
    
    await ctx.send('Total profit was: ' + str(profit) + '. \n Profit per minute was: ' + str(profit_per_minute) + '.')
    

    







bot.run(token)
