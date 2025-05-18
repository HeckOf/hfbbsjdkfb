import discord
from discord.ext import commands
import http.client
import json
import asyncio

# Replace with your bot token and channel ID
TOKEN = 'MTM3MzY2OTc5ODczODkyMzYyMQ.Ga4XYX.gse55nq-sPa6N2pqUEY9oHKpFHDwzzO9t3lfWo'
CHANNEL_ID = 1373639955364188315

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

# Expanded Emoji mapping for Blox Fruits
fruit_emojis = {
    "Light": "💡",
    "Ghost": "👻",
    "Dough": "🍩",
    "Shadow": "👤",
    "Rocket": "🚀",
    "Spin": "🌀",
    "Spring": "🌱",
    "Flame": "🔥",
    "Rubber": "🧱",
    "Creation": "✨",
    "Rumble": "⚡",
    "Pain": "😫",
    "Bomb": "💣",
    "Chop": "🗡️",
    "Dark": "🌑",
    "Ice": "🧊",
    "Smoke": "💨",
    "Spike": "📌",
    "Falcon": "🦅",
    "Sand": " sand ",
    "Revive": "🔄️",
    "Diamond": "💎",
    "Gravity": " 🌌",
    "Quake": "震",
    "Buddha": "🧘",
    "Love": "❤️",
    "Spider": "🕷️",
    "Phoenix": "🐦",
    "Portal": "🚪",
    "Dragon": "🐉",
    "Leopard": "🐆",
    "Mammoth": "🐘",
    "Venom": "🧪",
    "Control": "🕹️",
    "Spirit": "👻",
    "T-Rex": "🦖",
    "Kitsune": "🦊",
    "Blade": "🔪",
    "Barrier": "🛡️",
    "Blizzard": "❄️",
    "Magma": "🌋",
    "Sound": "🎶",
    "Eagle": "🦅",
    "Yeti": "🥶",
    "Gas": "☁️",
}

async def get_blox_fruits_data():
    """Fetches Blox Fruits stock data."""
    conn = http.client.HTTPSConnection("blox-fruit-stock-fruit.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "15a88d5551mshd96d21803ad9c30p195d93jsn58b0a731dd54",
        'x-rapidapi-host': "blox-fruit-stock-fruit.p.rapidapi.com"
    }
    try:
        conn.request("GET", "/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        print(f"Error fetching Blox Fruits data: {e}")
        return None

def create_discord_message(stock_info):
    """Formats the Blox Fruits stock data for Discord."""
    if not stock_info:
        return "Failed to get Blox Fruits stock data."

    message = "Blox Fruits Stock Update:\n\n"
    normal_stock = stock_info.get("normalStock", [])
    mirage_stock = stock_info.get("mirageStock", [])

    normal_items = []
    mirage_items = []

    if normal_stock:
        normal_items = [f"{fruit} {fruit_emojis.get(fruit, '')} x1" for fruit in normal_stock]
    else:
        normal_items = ["No fruits in stock."]

    if mirage_stock:
        mirage_items = [f"{fruit} {fruit_emojis.get(fruit, '')} x1" for fruit in mirage_stock]
    else:
        mirage_items = ["No fruits in stock."]

    message += "**Normal Stock:** " + " | ".join(normal_items) + "\n\n"
    message += "**Mirage Stock:** " + " | ".join(mirage_items)
    return message

async def send_stock_update(old_stock_data=None):
    """Gets Blox Fruits stock and sends an update to the Discord channel."""
    stock_data = await get_blox_fruits_data()
    if stock_data:
        message = create_discord_message(stock_data)
        channel = bot.get_channel(CHANNEL_ID)  # Use bot.get_channel
        if channel:
            if old_stock_data:
                if stock_data != old_stock_data:
                  await channel.send(message)
            else:
                await channel.send(message)
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")
        return stock_data
    return old_stock_data

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Start the background task to send updates every 30 minutes
    asyncio.create_task(check_for_stock_changes())

async def check_for_stock_changes():
    old_stock_data = None
    while True:
        old_stock_data = await send_stock_update(old_stock_data)
        await asyncio.sleep(600)  # Check every 10 minutes (600 seconds)

# Example command (optional)
@bot.command(name='stock')
async def get_stock(ctx):
    """Responds to the !stock command with the current Blox Fruits stock."""
    stock_data = await get_blox_fruits_data()
    if stock_data:
        message = create_discord_message(stock_data)
        await ctx.send(message)
    else:
        await ctx.send("Failed to get Blox Fruits stock data.")

bot.run(TOKEN)
