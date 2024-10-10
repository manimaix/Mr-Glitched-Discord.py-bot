import discord
from discord.ext import commands, tasks
import asyncio
import time

# Replace 'YOUR_BOT_TOKEN' with your bot's token
TOKEN = ''

# Intents setup (make sure to enable in Discord Developer Portal)
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix="$", intents=intents)

# Global variables
send_pings_enabled = True

# Cooldown dictionary to track the last time the bot was mentioned
cooldown = {}
allowed_channel_ids = [1240805113136681051,1291184003939958896]
category_id = 1240844403082268712  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')

async def countdown_timer(channel):
    total_seconds = 144  # 2 minutes and 44 seconds

    # Send an initial message and get the message object
    timer_message = await channel.send(f"{total_seconds // 60:02d}:{total_seconds % 60:02d} remaining")
    if send_pings_enabled:
        while total_seconds > 0:
            minutes, seconds = divmod(total_seconds, 60)
            timer_content = f"{minutes:02d}:{seconds:02d} remaining"
            await timer_message.edit(content=timer_content)
            await asyncio.sleep(1)
            total_seconds -= 1
        await timer_message.edit(content="@everyone Timer ended!")
    elif send_pings_enabled == False:
        await timer_message.edit(content="False Alarm, return back to your business.")
    
   

async def send_pings(channel):
    global send_pings_enabled
    if send_pings_enabled:
        for _ in range(30):  # Ping 30 times
            await channel.send("@everyone glitched biome detected!")
            await asyncio.sleep(0.1)  # Small delay to ensure messages are sent properly
            if not send_pings_enabled:
                break  # Exit the loop if send_pings_enabled becomes False
    else:
        send_pings_enabled = True  # Reset send_pings_enabled to True to resume pings
        return  # Exit the function if send_pings_enabled is False

async def send_marijester_links(channellink, messagelink, detected):
    channel = bot.get_channel(channellink)
    if channel:
        await channel.send(f"{detected} is Found!\n Detected in: {messagelink}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    # Check if the bot is mentioned
    if ((bot.user.mentioned_in(message)) or (message.author.bot and 'glitched' in message.content.lower())) and (message.channel.id in allowed_channel_ids or message.channel.category_id == category_id):
        current_time = time.time()
        if message.guild.id not in cooldown or (current_time - cooldown[message.guild.id]) > 600:  # 600 seconds = 10 minutes
            cooldown[message.guild.id] = current_time
            await send_pings(message.channel)
            await countdown_timer(message.channel)
        else:
            await message.channel.send(">>> I'm on cooldown. Try again later.")
    elif('glitchstop' in message.content.lower()) and (message.channel.id in allowed_channel_ids or message.channel.category_id == category_id):
        current_time = time.time()
        global send_pings_enabled
        send_pings_enabled = False
        await message.channel.send("Mass Pinging have stopped.")
        await asyncio.sleep(1)
        send_pings_enabled = True
    if message.author.bot and any(word in message.content.lower() for word in ['mari', 'jester']) and message.channel.category_id == category_id:
        message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        detected = []

        # Check for "Mari" and "Jester" in the message content
        if 'mari' in message.content.lower():
            detected.append('<@&1255540456352256010> ***Mari***')
        if 'jester' in message.content.lower():
            detected.append('<@&1255540361229631580> ***Jester***')

        # Join the detected names with " and " if both are present
        detected_str = " and ".join(detected)
        
        # Send the detected message link with the detected names
        await send_marijester_links(1288275351155249217, message_link, detected_str)


# Run the bot
bot.run(TOKEN)
