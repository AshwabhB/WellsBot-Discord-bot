import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True  

bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_USER_ID = 300797820170928139
TARGET_USER_ID2 = 9631088648725586020

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} guilds')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id not in (TARGET_USER_ID, TARGET_USER_ID2):
        return

    if before.self_deaf != after.self_deaf:
        print(f"\nDeafen state change for {member.name}")
        print(f"Before: self_deaf={before.self_deaf}")
        print(f"After: self_deaf={after.self_deaf}")

        if after.self_deaf:
            print(f"User {member.name} is self-deafened, attempting to move...")
            afk_channel = discord.utils.get(member.guild.channels, name='Shadow Realm')
            if not afk_channel:
                print("Shadow Realm channel not found!")
                return
            print(f"Found Shadow Realm channel: {afk_channel.name}")

            try:
                await member.move_to(afk_channel)
                print(f"Successfully moved {member.name} to Shadow Realm")
            except discord.Forbidden as e:
                print(f"Permission error: {e}")
                print("Bot doesn't have permission to move members")
            except Exception as e:
                print(f"Error moving user: {e}")
        else:
            print(f"User {member.name} is no longer self-deafened")

    if before.self_mute != after.self_mute:
        print(f"\nMute state change for {member.name}")
        print(f"Before: self_mute={before.self_mute}")
        print(f"After: self_mute={after.self_mute}")

bot.run(os.getenv('DISCORD_TOKEN')) 