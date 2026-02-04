import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

TIERS = {
    # U
    "asgore": {"full": "Acerola | King of Monsters", "tier": "U"},

    # EX
    "solemn": {"full": "Cross | Butterflies' Funeral", "tier": "EX"},

    # S
    "cross": {"full": "Cross", "tier": "S"},
    "uf": {"full": "Undying Flame", "tier": "S"},
    "vst": {"full": "Valentine Summer Time", "tier": "S"},
    "ewu rgb": {"full": "Eternal Wing | RGB | UNLEASHED", "tier": "S"},
    "mkvol": {"full": "Midknight Vessel of Life", "tier": "S"},
    "mkvolts": {"full": "Midknight Vessel of Life | Taped Shut", "tier": "S"},
    "mimivol": {"full": "Midknight Vessel of Life | Mimicry", "tier": "S"},

    # A
    "wh": {"full": "Wild Hunt", "tier": "A"},
    "soc": {"full": "Soul of Cinder", "tier": "A"},
    "nerd": {"full": "Standless | Nerd", "tier": "A"},
    "coco": {"full": "Rainy Time | Coco", "tier": "A"},
    "tuna": {"full": "Anubis Requiem | Tuna", "tier": "A"},
    "ewu": {"full": "Eternal Wing | Unleashed", "tier": "A"},
    "5th sinner": {"full": "Lei Heng | The 5th Sinner", "tier": "A"},
    "fxchara": {"full": "X!Chara : Frostbite", "tier": "A"},
    "duf": {"full": "Dullahan | Unyielding Frost", "tier": "A"},
    "se": {"full": "Singularity Essence", "tier": "A"},
    "mkb": {"full": "Midknight", "tier": "A"},
    "hxchara": {"full": "X!Chara | Hallowed", "tier": "A"},
    "dull": {"full": "Remembrance of Dullahan", "tier": "A"},
    "x!chara": {"full": "X!Chara", "tier": "A"},
    "agnes": {"full": "Okarun | Agnes Tachyon", "tier": "A"},
    "rukia ws": {"full": "Rukia Kuchiki : Winter Season", "tier": "A"},
    "goldship requiem": {"full": "Gold Ship Experience Requiem", "tier": "A"},
    "goldship experience": {"full": "Goldship Experience", "tier": "A"},
    "spin ce": {"full": "Spin | Singularity Essence", "tier": "A"},
    "aizen evo": {"full": "Aizen Sosuke (Hogyoku Fusion)", "tier": "A"},
    "aizen": {"full": "Aizen Sosuke", "tier": "A"},
    "ronin ce": {"full": "Ronin | Crimson Eclipse", "tier": "A"},
    "ronin awk": {"full": "Ronin (Successor of Niten Ichiryu)", "tier": "A"},
    "pk": {"full": "Pilgrim Knight", "tier": "A"},
    "starrk": {"full": "Coyote Starrk", "tier": "A"},
    "satono": {"full": "Satono Crazy Diamond", "tier": "A"},
    "kamen rider": {"full": "Black Silence | Kamen Rider Gaim", "tier": "A"},
    "will of fate": {"full": "Will of Fate", "tier": "A"},
    "bonnie": {"full": "Kaiju No.8 | Kaiju of 1987", "tier": "A"},
    "friren ru": {"full": "Frieren | Red Usurper", "tier": "A"},
    "acerola": {"full": "Acerola", "tier": "A"},
    "vergil": {"full": "True Anubis | Vergil", "tier": "A"},
    "fist of chaos": {"full": "Cyber Skeleton | Fist of Chaos", "tier": "A"},
    "faceless one": {"full": "Metallica | Faceless One", "tier": "A"},
    "anubis mm": {"full": "Anubis | Masquerade Meltdown", "tier": "A"},
    "wouap": {"full": "Wonder of U | Altered Palette", "tier": "A"},
    "gura": {"full": "Rainy Time | Gawr Gura", "tier": "A"},
    "isaac": {"full": "Nikyu Nikyu no mi | Isaac", "tier": "A"},
    "izutsumi": {"full": "Eggxeed | Izutsumi", "tier": "A"},
    "eggxeed": {"full": "Eggxeed", "tier": "A"},
    "troll mask": {"full": "Troll Mask", "tier": "A"},
    "st genderbend": {"full": "Summer Time | Genderbend", "tier": "A"},
    "golden egg": {"full": "Golden Egg", "tier": "A"},
    "spin candy": {"full": "Spin | Candy", "tier": "A"}
}

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="@Furi tierlist"
        )
    )
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user in message.mentions:
        query = message.content.lower().replace(client.user.mention, "").strip()

        # tierlist / tl
        if query in ["tierlist", "tl"]:
            await message.channel.send(file=discord.File("tierlist.png"))
            return

        # character tier
        if query in TIERS:
            data = TIERS[query]
            await message.channel.send(
                f"**{query.title()}** **[{data['full']}]** is on **{data['tier']}** Tier!"
            )
        else:
            await message.channel.send(
                f"❌ Sorry I don't know what is **{query}**"
            )

client.run(os.getenv("TOKEN"))
