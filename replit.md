# Furi Bot

Python Discord bot using discord.py. The existing single-file structure and bot commands are preserved.

## Run on Replit

- Set the `TOKEN` secret to the Discord application's bot token. Never put it in source code.
- Use the **Run Discord bot** workflow (the Run button), which executes `python -u main.py` from the project root.
- Dependencies are listed in `requirements.txt`; the voice extra includes Discord's voice dependencies. FFmpeg is configured in `.replit`.
- Successful startup prints `Logged in as ...` in the Console after connecting to Discord.
- This is a background bot, not a website; there is no web preview or listening HTTP port.

## Discord configuration

- Enable **Message Content Intent** under the application's Bot settings in the Discord Developer Portal; the existing code requests this privileged intent.
- Invite the bot to your server with permissions to view channels, read message history, send messages, and attach files. Voice commands also need Connect and Speak.
- Mention the bot followed by `help` in Discord to see its commands.
- The existing `OWNER_ID` and `AUTO_REPLY_CHANNELS` values in `main.py` are repository-specific; change them if using a different owner or channel.
- Voice playback needs the included `PIXEL_SOUND.wav`. Keep it and `tierlist.png` in the project root.

Keep one bot process running per token to avoid duplicate responses. The workspace workflow runs while the workspace process remains active; setting up always-on publishing is separate from this import setup.
