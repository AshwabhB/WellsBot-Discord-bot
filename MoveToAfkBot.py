import os
import discord
from discord.ext import commands, tasks
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
    check_voice_status.start()

@tasks.loop(seconds=1)
async def check_voice_status():
    for guild in bot.guilds:
        print(f"\nChecking guild: {guild.name}")
        
        afk_channel = discord.utils.get(guild.channels, name='Shadow Realm')
        if not afk_channel:
            print("AFK channel not found!")
            continue
        print(f"Found AFK channel: {afk_channel.name}")

        target_member = None
        for channel in guild.voice_channels:
            print(f"\nChecking channel: {channel.name}")
            print(f"Members in channel: {[m.name for m in channel.members]}")
            
            # member = next((m for m in channel.members if m.id == TARGET_USER_ID), None)
            member = next((m for m in channel.members if m.id in (TARGET_USER_ID, TARGET_USER_ID2)), None)

            if member:
                target_member = member
                print(f"Found target member: {member.name}")
                print(f"Voice state: self_deaf={member.voice.self_deaf}, self_mute={member.voice.self_mute}")
                break

        if target_member and target_member.voice:
            if target_member.voice.self_deaf:
                print(f"User {target_member.name} is self-deafened, attempting to move...")

                try:
                    await target_member.move_to(afk_channel)
                    print(f"Successfully moved {target_member.name} to AFK channel")
                except discord.Forbidden as e:
                    print(f"Permission error: {e}")
                    print("Bot doesn't have permission to move members")
                except Exception as e:
                    print(f"Error moving user: {e}")
            else:
                print(f"User {target_member.name} is not self-deafened")
        else:
            print("Target member not found in any voice channel")

bot.run(os.getenv('DISCORD_TOKEN')) 