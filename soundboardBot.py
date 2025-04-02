import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True 
bot = commands.Bot(command_prefix='!', intents=intents)


SOUNDS_DIR = 'sounds'
available_sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith(('.mp3', '.ogg'))]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Available sounds:')
    for sound in available_sounds:
        print(f'- {sound}')
    

    await setup(bot)

class SoundboardView(discord.ui.View):
    def __init__(self, cog, show_vc_controls=True):
        super().__init__(timeout=None)
        self.cog = cog
        

        if show_vc_controls:
            join_button = discord.ui.Button(
                label="Join VC",
                style=discord.ButtonStyle.green,
                emoji="✅",
                custom_id="join_vc"
            )
            join_button.callback = self.join_vc
            self.add_item(join_button)

            leave_button = discord.ui.Button(
                label="Leave VC",
                style=discord.ButtonStyle.red,
                emoji="❌",
                custom_id="leave_vc"
            )
            leave_button.callback = self.leave_vc
            self.add_item(leave_button)
        

        for i, sound in enumerate(available_sounds):
            button = discord.ui.Button(
                label=f"Sound {chr(65 + i)}",
                style=discord.ButtonStyle.primary,
                emoji="🎵", 
                custom_id=f"sound_{i}"
            )
            button.callback = lambda interaction, s=sound: self.cog.play_sound(interaction, s)
            self.add_item(button)

    async def join_vc(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
            return
        
        if interaction.guild.voice_client:
            await interaction.response.send_message("I'm already in a voice channel!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        await voice_channel.connect()
        await interaction.response.defer()
        response = await interaction.followup.send(f"Joined {voice_channel.name}")
        await asyncio.sleep(3)
        await response.delete()

    async def leave_vc(self, interaction: discord.Interaction):
        if not interaction.guild.voice_client:
            await interaction.response.send_message("I'm not in a voice channel!", ephemeral=True)
            return

        await interaction.guild.voice_client.disconnect()
        await interaction.response.defer()
        response = await interaction.followup.send("Left the voice channel")
        await asyncio.sleep(3)
        await response.delete()

class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_sound(self, interaction: discord.Interaction, sound_name: str):
        if not interaction.user.voice:
            await interaction.response.send_message("You need to be in a voice channel first!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        
        if not interaction.guild.voice_client:
            await voice_channel.connect()
            voice_client = interaction.guild.voice_client
        else:
            voice_client = interaction.guild.voice_client

        # Check if already playing
        if voice_client.is_playing():
            await interaction.response.send_message("A sound is already playing. Please wait for it to finish.", ephemeral=True)
            return

        sound_path = os.path.join(SOUNDS_DIR, sound_name)
        voice_client.play(discord.FFmpegPCMAudio(sound_path))
        await interaction.response.defer()
        response = await interaction.followup.send(f'Playing: {sound_name}')
        await asyncio.sleep(3)
        await response.delete()

    @commands.group(name='wb', invoke_without_command=True)
    async def wb(self, ctx):
        """Soundboard commands. Use !wb help to see all commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Please use a subcommand. Available commands:\n"
                         "`!wb join` - Join your voice channel\n"
                         "`!wb leave` - Leave the voice channel\n"
                         "`!wb soundboard` - Show available sounds\n"
                         "`!wb play <sound>` - Play a sound\n"
                         "`!wb start` - Start the soundboard with all controls")

    @wb.command(name='start')
    async def start(self, ctx):
        """Start the soundboard with all controls"""

        embed = discord.Embed(
            title="🎵 Soundboard Menu 🎵",
            description="Click the buttons to play sounds or control the bot!",
            color=discord.Color.blue()
        )


        for i, sound in enumerate(available_sounds):
            embed.add_field(
                name=f"Sound {chr(65 + i)}",
                value=sound,
                inline=False
            )


        view = SoundboardView(self, show_vc_controls=True)


        await ctx.send(embed=embed, view=view)

    @wb.command(name='join')
    async def join(self, ctx):
        """Join the user's voice channel"""
        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel first!")
            return
        
        if ctx.voice_client:
            await ctx.send("I'm already in a voice channel!")
            return

        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()
        await ctx.send(f"Joined {voice_channel.name}")

    @wb.command(name='leave')
    async def leave(self, ctx):
        """Leave the voice channel"""
        if not ctx.voice_client:
            await ctx.send("I'm not in a voice channel!")
            return

        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel")

    @wb.command(name='soundboard')
    async def soundboard(self, ctx):
        """Show interactive soundboard menu"""

        embed = discord.Embed(
            title="🎵 Soundboard Menu 🎵",
            description="Click the buttons to play sounds!",
            color=discord.Color.blue()
        )


        for i, sound in enumerate(available_sounds):
            embed.add_field(
                name=f"Sound {i+1}",
                value=sound,
                inline=False
            )


        view = SoundboardView(self, show_vc_controls=False)


        await ctx.send(embed=embed, view=view)

    @wb.command(name='play')
    async def play(self, ctx, sound_name: str):
        """Play a sound from the soundboard"""

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command!")
            return


        if sound_name not in available_sounds:
            await ctx.send(f"Sound '{sound_name}' not found! Use !wb soundboard to see available sounds.")
            return


        voice_channel = ctx.author.voice.channel
        

        if not ctx.voice_client:
            await voice_channel.connect()
            voice_client = ctx.voice_client
        else:
            voice_client = ctx.voice_client


        sound_path = os.path.join(SOUNDS_DIR, sound_name)
        voice_client.play(discord.FFmpegPCMAudio(sound_path))
        response = await ctx.send(f'Playing: {sound_name}')
        await asyncio.sleep(3)
        await response.delete()

    @wb.command(name='stop')
    async def stop(self, ctx):
        """Stop playing the current sound"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            response = await ctx.send('Stopped playing sound')
            await asyncio.sleep(3)
            await response.delete()
        else:
            response = await ctx.send('No sound is currently playing')
            await asyncio.sleep(3)
            await response.delete()

async def setup(bot):
    await bot.add_cog(Soundboard(bot))


bot.run(TOKEN) 