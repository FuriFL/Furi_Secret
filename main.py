import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # กันบอทตอบตัวเอง
    if message.author.bot:
        return

    # เช็กว่ามีการ @ บอทไหม
    if client.user in message.mentions:
        content = message.content.lower()

        if "tierlist" in content:
            await message.channel.send(
                file=discord.File("tierlist.png")
            )

client.run(os.getenv("TOKEN"))
