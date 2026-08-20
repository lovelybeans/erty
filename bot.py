import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Set up intents (Message content intent is required for prefix commands)
class MyBot(commands.Bot):
    def __init__(self):
        intent = discord.Intents.default()
        intent.message_content = True
        intent.members = True
        super().__init__(command_prefix="~", intents=intent)

    async def setup_hook(self) -> None:
        await self.tree.sync()

    async def on_ready(self) -> None:
        print(f"{self.user.name} running...")

        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name='Watching Ladybugs every move'))

client = MyBot()
cooldown = False

async def cool():
    global cooldown
    cooldown = True
    time.sleep(10)
    cooldown = False

@client.event
async def on_message(msg: discord.Message):
    if msg.author == client.user:
        return

    if msg.author.id == 485486238703288324 or "<@485486238703288324>" in msg.content:
        if cooldown: return
        await msg.reply('''"Um, 'You're sexy when you use those big words humina humina.'"''')
        await cool()
    elif 'lurla' in msg.content.lower() or 'leela' in msg.content.lower():
        await msg.reply("UGH! It is not that! It is Lola! I mean- Lila! Cerise! ...Iris!\n*Gasps, putting a hand to her forehead*\nOh no, my rare, stress-induced aphasia is acting up again because you're bullying me! You're being so mean! I'm telling Mr. Damocles!")

@client.event
async def on_member_join(member: discord.Member):
    chan = member.guild.get_channel(1538358140016271400)
    await chan.send(f'Uhhh... Welcome {member.mention}... I guess.')

client.run(os.getenv('BOT_TOKENL'))