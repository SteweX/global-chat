import aiohttp
import discord
import json
import re

from discord.ext import commands

class GlobalChat(commands.Cog):

	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, msg):
		try:
			if not msg.author.bot or msg.author.id == 835926382336540692:
				async with aiohttp.ClientSession() as session:
					with open('./settings.json') as json_file:
						data = json.load(json_file)['bridges']
					for bridge in data:
						if str(msg.channel.id) in data[bridge]['channels']:
							message = msg.content
							results = re.findall('<@[0-9]*>|<@![0-9]*>', message)
							for result in results:
								try:
									user = self.bot.get_user(int(re.search(r'\d+', result).group(0)))
								except Exception as e:
									print(f"ОШИБКА ПОЛУЧЕНИЯ ЮЗЕРА:\n{e}")
								else:
									if user:
										message = re.sub(result, f'`@{user.name}#{user.discriminator}`', message)
									else:
										message = re.sub(result, '`@Guest#0000`', message)
							message = re.sub('@everyone|@here', '-', message)
							for channel in data[bridge]['channels']:
								if int(channel) == msg.channel.id:
									continue
								if msg.author.bot:
									webhook = discord.Webhook.from_url(data[bridge]['channels'][channel]['webhook'], adapter=discord.AsyncWebhookAdapter(session))
									await webhook.send(content=message, embeds=msg.embeds, username=f"{msg.author.name}", avatar_url=str(msg.author.avatar_url))
								else:
									webhook = discord.Webhook.from_url(data[bridge]['channels'][channel]['webhook'], adapter=discord.AsyncWebhookAdapter(session))
									await webhook.send(content=message, username=f"[{msg.guild.name}] {msg.author.name}", avatar_url=str(msg.author.avatar_url))
		except Exception as e:
			print(f"ОШИБКА ИВЕНТА on_message:\n{e}")

def setup(bot):
	bot.add_cog(GlobalChat(bot))