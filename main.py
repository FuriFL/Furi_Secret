import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TIERS = {
    # U
    "asgore": "U",

    # EX
    "solemn": "EX",

    # S
    "cross": "S",
    "uf": "S",
    "vst": "S",
    "ewu rgb": "S",
    "mkvol": "S",
    "mkvolts": "S",
    "mimivol": "S",

    # A
    "wh": "A",
    "soc": "A",
    "nerd": "A",
    "coco": "A",
    "tuna": "A",
    "ewu": "A",
    "5th sinner": "A",
    "fxchara": "A",
    "duf": "A",
    "se": "A",
    "mkb": "A",
    "hxchara": "A",
    "dull": "A",
    "x!chara": "A",
    "agnes": "A",
    "rukia ws": "A",
    "goldship requiem": "A",
    "goldship experience": "A",
    "spin ce": "A",
    "aizen evo": "A",
    "aizen": "A",
    "ronin ce": "A",
    "ronin awk": "A",
    "pk": "A",
    "starrk": "A",
    "satono": "A",
    "kamen rider": "A",
    "will of fate": "A",
    "bonnie": "A",
    "friren ru": "A",
    "acerola": "A",
    "vergil": "A",
    "fist of chaos": "A",
    "faceless one": "A",
    "anubis mm": "A",
    "wouap": "A",
    "gura": "A",
    "isaac": "A",
    "izutsumi": "A",
    "eggxeed": "A",
    "troll mask": "A",
    "st genderbend": "A",
    "golden egg": "A",
    "spin candy": "A"
}

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user in message.mentions:
        content = message.content.lower()

        # ตัด mention บอทออก เหลือแต่คำสั่ง
        query = content.replace(client.user.mention, "").strip()

        # คำสั่ง tierlist / tl
        if query in ["tierlist", "tl"]:
            await message.channel.send(
                file=discord.File("tierlist.png")
            )
            return

        # คำสั่งถาม tier ตัวละคร
        if query in TIERS:
            tier = TIERS[query]
            await message.channel.send(
                f"**{query}** is on **{tier} tier!**"
            )
        else:
            await message.channel.send(
                f"❌ sorry I don't know what is **{query}**"
            )

client.run(os.getenv("TOKEN"))
