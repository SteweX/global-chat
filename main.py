import discord
import json

from discord.ext import commands

with open('./settings.json') as f:
	data = json.load(f)

bot = commands.Bot(command_prefix=data['bot_prefix'], intents=discord.Intents.all())

@bot.event
async def on_ready():
	bot.load_extension(f"cogs.GlobalChat")
	print("Bot Has been runned")

bot.run(data['bot_token'])