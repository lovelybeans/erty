import discord
from discord import app_commands, ui
from discord.ext import commands
from colorama import Fore, Back, Style, init
import json
import sys

init(autoreset=True)

allowed_status = {
    "online": discord.Status.online,
    "idle": discord.Status.idle,
    "dnd": discord.Status.dnd,
    "do_not_disturb": discord.Status.dnd,
    "invisible": discord.Status.invisible
}


def error_msg(message: str):
    print(Fore.RED + Back.BLACK + message)
    print(Fore.RED + Back.BLACK + "PLEASE CLOSE THIS WINDOW AND RE-RUN THE PROGRAM ONCE THE ERROR HAS BEEN RESOLVED")
    while True:
        a = input()


try:
    with open('Config.json', 'r') as file:
        config = json.load(file)
except Exception as e:
    error_msg(f"ERROR: {e}")
    error_msg("RENAME YOUR CONFIG FILE TO " + '"Config.json" AND TRY AGAIN')

print(config)
if not 'token' in config:
    error_msg("token VALUE NOT FOUND IN CONFIG FILE")
if not 'owner_id' in config:
    error_msg("owner_id VALUE NOT FOUND IN CONFIG FILE")
if not 'status' in config:
    error_msg("status VALUE NOT FOUND IN CONFIG FILE")
if not 'activity' in config:
    error_msg("activity VALUE NOT FOUND IN CONFIG FILE")
if not 'commands' in config:
    error_msg("commands VALUE NOT FOUND IN CONFIG FILE")
if not 'log_chan' in config:
    error_msg("log_chan VALUE NOT FOUND IN CONFIG FILE")
if not 'guild_id' in config:
    error_msg("guild_id VALUE NOT FOUND IN CONFIG FILE")
else:
    en_commands = config['commands']

try:
    class BotClient(commands.Bot):
        def __init__(self):
            intent = discord.Intents.default()
            intent.message_content = True
            super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intent)

        async def setup_hook(self):

            await self.tree.sync()

        async def on_ready(self):
            print(f"{self.user.name} running...")
            print(Fore.YELLOW + "THIS APPLICATION IS STILL IN BETA, EXPECT BUGS/ERRORS")

            if not config['status'] in allowed_status:
                config['status'] = 'online'

            botstatus = allowed_status[config['status']]

            if config['activity']['enabled'] == True:
                activitys = config['activity']
                if activitys['type'].lower() == 'game':
                    activity = discord.Game(name=activitys['name'])
                elif activitys['type'].lower() == 'streaming':
                    activity = discord.Streaming(name=activitys['name'], url=activitys['surl'])
                elif activitys['type'].lower() == 'listening':
                    activity = discord.Activity(type=discord.ActivityType.listening, name=activitys['name'])
                elif activitys['type'].lower() == "watching":
                    activity = discord.Activity(type=discord.ActivityType.watching, name=activitys['name'])
                else:
                    print(activitys['type'])
                    activity = discord.Game(name=activitys['name'])
            else:
                activity = None

            await self.change_presence(status=botstatus, activity=activity)
            guild = await self.fetch_guild(config['guild_id'])
            chan = await guild.fetch_channel(config['log_chan'])
            await chan.send(f"{self.user.mention} running...")


    client = BotClient()


    def defcommand(name: str, desc: str, func):
        if not name in en_commands or en_commands[name] == True:
            client.tree.add_command(app_commands.Command(name=name, description=desc, callback=func))


    @app_commands.describe(user="The user to ban", reason="The reason for the ban.")
    async def ban(intr: discord.Interaction, user: discord.Member, reason: str = ""):
        await intr.response.defer(ephemeral=True)
        try:
            if intr.guild.id != config['guild_id']:
                guild = await client.get_guild(config['guild_id'])
                await guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to ban {user.mention} in {guild.name}.")
                await intr.followup.send(f"This is not the correct server.", ephemeral=True)
                return
            elif not intr.user.guild_permissions.ban_members:
                await intr.guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to ban {user.mention} but does not have the required permissions.")
                await intr.followup.send(f"You do not have ban permissions.", ephemeral=True)
                return
            else:
                await intr.guild.ban(user=user, reason=reason)
                await intr.response.send_message(f"Successfuly banned {user.mention}!", ephemeral=True)
                await intr.followup.send(config['log_chan']).send(f"{user.mention} was banned by {intr.user.mention}.")
        except Exception as e:
            error_msg(f'BOT ERROR: {e}')


    defcommand('ban', 'Ban a user from the server.', ban)


    @app_commands.describe(user_id="The user id of the user to unban")
    async def unban(intr: discord.Interaction, user_id: str):
        await intr.response.defer(ephemeral=True)
        try:
            if not int(user_id):
                await intr.followup.send(f"The user id is not a valid number.", ephemeral=True)
                return
            else:
                user = await client.fetch_user(int(user_id))
            if intr.guild.id != config['guild_id']:
                guild = await client.get_guild(config['guild_id'])
                await guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to unban {user.mention} in {guild.name}.")
                await intr.followup.send(f"This is not the correct server.", ephemeral=True)
                return
            elif not intr.user.guild_permissions.ban_members:
                await intr.guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to unban {user.mention} but does not have the required permissions.")
                await intr.followup.send(f"You do not have ban permissions.", ephemeral=True)
                return
            else:
                await intr.guild.unban(user=user)
                await intr.followup.send(f"Successfuly unbanned {user.mention}!", ephemeral=True)
                await intr.guild.get_channel(config['log_chan']).send(
                    f"{user.mention} was unbanned by {intr.user.mention}.")
        except Exception as e:
            error_msg(f'BOT ERROR: {e}')


    defcommand('unban', 'Unban a user from the server.', unban)


    @app_commands.describe(user="The user to kick.", reason="The reason for the kick.")
    async def kick(intr: discord.Interaction, user: discord.Member, reason: str):
        await intr.response.defer(ephemeral=True)
        try:
            if intr.guild.id != config['guild_id']:
                guild = await client.get_guild(config['guild_id'])
                await guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to kick {user.mention} in {guild.name}.")
                await intr.followup.send(f"This is not the correct server.", ephemeral=True)
                return
            elif not intr.user.guild_permissions.kick_members:
                await intr.guild.get_channel(config['log_chan']).send(
                    f"{intr.user.mention} tried to kick {user.mention} but does not have the required permissions.")
                await intr.followup.send(f"You do not have kick permissions.", ephemeral=True)
                return
            else:
                await intr.guild.kick(user=user, reason=reason)
                await intr.followup.send(f"Successfuly kicked {user.mention}!", ephemeral=True)
                await intr.guild.get_channel(config['log_chan']).send(
                    f"{user.mention} was kicked by {intr.user.mention}.")
        except Exception as e:
            error_msg(f'BOT ERROR: {e}')


    defcommand('kick', 'Kick a user from the server', kick)

    client.run(config['token'])

except Exception as e:
    error_msg(F"ERROR WITH BOT: {e}")