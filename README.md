# Discord Voice Channel Monitor Bot

This Discord bot monitors a specific user in voice channels and automatically moves them to an AFK channel when they are deafened.

## Bot Descriptions

### Move to AFK Bot (`MoveToAfkBot.py`)
A monitoring bot that keeps track of specific users in voice channels. It automatically moves targeted users to a designated "Shadow Realm" channel when they are self-deafened. The bot checks user status every second and requires proper permissions to move members between channels.

### Soundboard Bot (`soundboardBot.py`)
A versatile soundboard bot that allows users to play various sound effects in voice channels. It features an interactive button interface for easy sound selection, voice channel controls, and supports both MP3 and OGG audio files. Users can join/leave voice channels and play sounds with simple commands or through the interactive menu.

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg (Required for sound playback):
   - Create a folder at `C:\ffmpeg`
   - Inside that folder, create another folder called `bin`
   - Download FFmpeg from the official website
   - Extract the downloaded zip file
   - Open the extracted folder (named something like `ffmpeg-master-latest-win64-gpl`)
   - Go inside the `bin` folder
   - Copy all files (ffmpeg.exe, ffplay.exe, etc.) to `C:\ffmpeg\bin`
   - Add FFmpeg to your system PATH:
     1. Open Windows Search and type "Environment Variables"
     2. Click "Edit the system environment variables"
     3. Click "Environment Variables" button
     4. Under "System Variables", find and select "Path"
     5. Click "Edit"
     6. Click "New"
     7. Add `C:\ffmpeg\bin`
     8. Click "OK" on all windows
     9. Restart your terminal/command prompt

3. Create a `.env` file in the project root and add your Discord bot token:
```
DISCORD_TOKEN=your_bot_token_here
```

4. Edit the `MoveToAfkBot.py` or `soundboardBot.py` file and replace `TARGET_USER_ID` with the Discord user ID you want to monitor.

5. Create a voice channel named "AFK" in your Discord server.

6. Add sound files to the `sounds` folder:
   - Create a folder named `sounds` in the project root if it doesn't exist
   - Add your MP3 or OGG sound files to this folder
   - The bot will automatically detect and make available any sound files in this folder

7. Run the bot:
```bash
python MoveToAfkBot.py
or
python soundboardBot.py
```

## Features

- Monitors a specific user in all voice channels
- Automatically moves the user to the AFK channel when they are deafened
- Checks status every 5 seconds
- Requires proper bot permissions (Move Members)

## Required Bot Permissions

- View Channels
- Connect
- Move Members

## Getting Your Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the token and paste it in your `.env` file

## Getting User ID

1. Enable Developer Mode in Discord (User Settings > App Settings > Advanced > Developer Mode)
2. Right-click the user you want to monitor
3. Click "Copy ID"
4. Paste the ID in the `TARGET_USER_ID` variable in `MoveToAfkBot.py` or `soundboardBot.py`