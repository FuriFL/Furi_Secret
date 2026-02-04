import discord
import os
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ======================
# TIERS DATA (รวม U, EX, S, A, B, C) — อย่าให้ตัวละครหายแม้แต่ตัวเดียว
# KEY: lower-case shorthand หรือคำที่คุณอยากพิมพ์หา
# value: dict { "full": ชื่อเต็ม, "tier": ระดับ, optional "amount": จำนวน }
# ======================
TIERS = {
    # ===== U =====
    "asgore": {"full": "Acerola | King of Monsters", "tier": "U"},

    # ===== EX =====
    "solemn": {"full": "Cross | Butterflies' Funeral", "tier": "EX"},

    # ===== S =====
    "cross": {"full": "Cross", "tier": "S"},
    "uf": {"full": "Undying Flame", "tier": "S"},
    "vst": {"full": "Valentine Summer Time", "tier": "S"},
    "ewu rgb": {"full": "Eternal Wing | RGB | UNLEASHED", "tier": "S"},
    "mkvol": {"full": "Midknight Vessel of Life", "tier": "S"},
    "mkvolts": {"full": "Midknight Vessel of Life | Taped Shut", "tier": "S"},
    "mimivol": {"full": "Midknight Vessel of Life | Mimicry", "tier": "S"},

    # ===== A =====
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
    "spin candy": {"full": "Spin | Candy", "tier": "A"},

    # ===== B =====
    "ta": {"full": "True Anubis", "tier": "B"},
    "cd pumpkin": {"full": "Crazy Diamond | Pumpkin", "tier": "B"},
    "spoon": {"full": "Stop Sign | Comically Large Spoon", "tier": "B"},
    "easter egg": {"full": "Easter Egg", "tier": "B"},
    "sibuna": {"full": "Anubis | Sibuna", "tier": "B"},
    "bunny suit": {"full": "Summer Time | Bunny Suit", "tier": "B"},
    "ar": {"full": "Anubis Requiem", "tier": "B"},
    "astolfosp": {"full": "Astolfo | Sailor Paladin", "tier": "B"},
    "astolfo": {"full": "Astolfo (Saber)", "tier": "B"},
    "astolfots": {"full": "Astolfo | Taped Shut", "tier": "B"},
    "cirno": {"full": "Hie Hie | The Strongest Fairy", "tier": "B"},
    "eggwand": {"full": "Stop Sign | Egg Wand", "tier": "B"},
    "deku": {"full": "Deku", "tier": "B"},
    "frieren": {"full": "Frieren", "tier": "B"},
    "stw devil": {"full": "Shadow The World | Devil", "tier": "B"},
    "sandeh": {"full": "Sandevistan : Holiday 2077", "tier": "B"},
    "sandhs": {"full": "Sandevistan : Holiday Skeleton 2077", "tier": "B"},
    "infernal bard": {"full": "Stop Sign | Infernal Bard", "tier": "B"},
    "mih": {"full": "Made In Heaven", "tier": "B"},
    "gigamesh": {"full": "Gilgamesh (Archer)", "tier": "B"},
    "cidgo": {"full": "Cid Kagenou | Galactic Overlord", "tier": "B"},
    "bandits slayer": {"full": "Cid Kagenou | Stylish Bandits Slayer", "tier": "B"},
    "wsmm": {"full": "White Snake | Marshmallow", "tier": "B"},
    "wts": {"full": "Winter Time | Santa", "tier": "B"},
    "hina": {"full": "Sorasaki Hina", "tier": "B"},
    "egg keeper": {"full": "Egg Keeper", "tier": "B"},
    "kokushibo": {"full": "Moon Breathing | Hybrid Demon", "tier": "B"},
    "nokotan": {"full": "Nokotan", "tier": "B"},
    "cid": {"full": "Cid Kagenou", "tier": "B"},
    "roland": {"full": "The Black Silence", "tier": "B"},
    "akaza": {"full": "Akaza", "tier": "B"},
    "carrot": {"full": "Carrot (Electro)", "tier": "B"},
    "sende evo": {"full": "Sandevistan : Cyber Skeleton", "tier": "B"},
    "sande": {"full": "Sandevistan", "tier": "B"},
    "wou": {"full": "Wonder of U", "tier": "B"},
    "kaiju no.8": {"full": "Kaiju No.8", "tier": "B"},
    "sp shadow": {"full": "Star Platinum | Shadow Master", "tier": "B"},
    "lunatic red eyes": {"full": "Emperor | Lunatic Red Eyes", "tier": "B"},
    "gojo1/2": {"full": "Gojo Satoru | 1/2", "tier": "B"},
    "holy wreath": {"full": "Standless | Holy Wreath", "tier": "B"},
    "st witch": {"full": "Summer Time | Witch", "tier": "B"},
    "alucard": {"full": "Alucard", "tier": "B"},
    "stw easter": {"full": "Shadow The World | Easter", "tier": "B"},
    "lightsaber": {"full": "Anubis | Lightsaber", "tier": "B"},
    "stop scythe": {"full": "Stop Sign | Stop Scythe", "tier": "B"},
    "lei heng captain rampage": {"full": "Lei Heng | Captain Rampage", "tier": "B"},
    "death certificate": {"full": "Death Certificate", "tier": "B"},
    "stdd": {"full": "Star Platinum : Dragon Dance", "tier": "B"},
    "ger azael": {"full": "Gold Experience Requiem | Azael", "tier": "B"},
    "mita": {"full": "Shadow The World | Mita", "tier": "B"},
    "twf": {"full": "The World : Frozen", "tier": "B"},
    "cdc": {"full": "Crazy Diamond | Crystallized", "tier": "B"},

    # ===== C =====
    "fingers": {"full": "Sukuna's Cursed Finger", "tier": "C", "amount": 5},
    "rusted sword": {"full": "Rusted Sword", "tier": "C"},
    "okarun egg": {"full": "Okarun | Egg of All-devouring Darkness", "tier": "C"},
    "getothm": {"full": "Suguru Geto | The Hunt Master", "tier": "C"},
    "gojo": {"full": "Gojo Satoru", "tier": "C"},
    "hog": {"full": "Hogyoku Fragment", "tier": "C"},
    "sukuna": {"full": "Ryomen Sukuna", "tier": "C"},
    "geto": {"full": "Suguru Geto", "tier": "C"},
    "toji": {"full": "Toji Fushiguro", "tier": "C"},
    "candy cane": {"full": "Stop Sign | Candy Cane", "tier": "C"},
    "oa's grace": {"full": "OA's Grace", "tier": "C"},
    "anubis spook": {"full": "Anubis | Spook", "tier": "C"},
    "hamon frost": {"full": "Hamon | Frost", "tier": "C"},
    "hohe": {"full": "Herrscher of Human Ego", "tier": "C"},
    "c-moon": {"full": "C-Moon", "tier": "C"},
    "baiken": {"full": "Baiken", "tier": "C"},
    "sanji sakurian": {"full": "Sanji (Sakurian)", "tier": "C"},
    "okarun": {"full": "Okarun", "tier": "C"},
    "ichigo": {"full": "Kurosaki Ichigo", "tier": "C"},
    "the red mist": {"full": "The Red Mist", "tier": "C"},
    "sanji": {"full": "Sanji", "tier": "C"},
    "garou sakurian": {"full": "Garou | Water Stream Rock Smashing Fist (Sakurian)", "tier": "C"},
    "arasaka": {"full": "Arasaka Suitcase", "tier": "C"},
    "ew rgb": {"full": "Eternal Wing | RGB", "tier": "C"},
    "yuta": {"full": "Okkotsu Yuta", "tier": "C"},
    "sakuya": {"full": "Sakuya Izayoi", "tier": "C"},
    "yuji": {"full": "Itadori Yuji", "tier": "C"},
    "lei heng": {"full": "Lei Heng", "tier": "C"},
    "stop sign regret": {"full": "Stop Sign | Regret", "tier": "C"},
    "bag of presents": {"full": "Bag of Present", "tier": "C", "amount": 5},
    "ger": {"full": "Gold Experience Requiem", "tier": "C"},
    "padoru": {"full": "Padoru", "tier": "C"},
    "headhunter": {"full": "Emperor | Headhunter", "tier": "C"},
    "stop sign bisento": {"full": "Stop Sign | Bisento", "tier": "C"},
}

# ============
# helpers
# ============
def normalize(s: str) -> str:
    """lower, strip spaces, collapse spaces, remove surrounding punctuation"""
    if s is None:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    # remove leading/trailing punctuation
    s = s.strip(" '\"`.,:;-()[]{}")
    return s


def find_entry_by_query(q: str):
    """
    Try to find an entry in TIERS by:
    - exact key match
    - full name match
    - normalized match (ignore case & extra spaces & surrounding punctuation)
    - partial containment match
    Returns tuple (key, data) or (None, None)
    """
    q_norm = normalize(q)

    # 1) direct key match (exact)
    if q_norm in TIERS:
        return q_norm, TIERS[q_norm]

    # 2) try match full names or keys with normalization
    for key, data in TIERS.items():
        # check normalized key
        if normalize(key) == q_norm:
            return key, data
        # check normalized full name
        if normalize(data.get("full", "")) == q_norm:
            return key, data

    # 3) partial containment (if user typed a smaller phrase)
    # e.g., user types "vergil" and full is "True Anubis | Vergil" -> match
    for key, data in TIERS.items():
        full_norm = normalize(data.get("full", ""))
        if q_norm in full_norm or full_norm in q_norm:
            return key, data

    return None, None


# ============
# events
# ============
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="@Furi find <name>  |  @Furi tl"
        )
    )
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # only react when bot is mentioned
    if client.user not in message.mentions:
        return

    # original content without mention
    raw = message.content.replace(client.user.mention, "").strip()

    if not raw:
        await message.channel.send("❗ Usage: `@Bot find <name>` or `@Bot tl` (tierlist)")
        return

    # normalize leading spaces and collapse multiple spaces
    raw = re.sub(r"\s+", " ", raw).strip()

    # If user asked for tierlist (backwards compatible)
    if raw.lower() in ["tierlist", "tl"]:
        # send tierlist image (must exist in project root)
        try:
            await message.channel.send(file=discord.File("tierlist.png"))
        except Exception:
            await message.channel.send("💔 Error sending tierlist image.")
        return

    # New command format: expect "find <name>"
    parts = raw.split(" ", 1)
    if parts[0].lower() != "find":
        await message.channel.send("😡 Please use `@Bot find <name>` to search for a spec/stand, or `@Bot tl` for the tierlist image.")
        return

    if len(parts) < 2 or not parts[1].strip():
        await message.channel.send("😡 Please provide a name after `find`. Example: `@Bot find ewu`")
        return

    query_raw = parts[1].strip()  # keep original casing for display
    # search using normalized matching
    key, data = find_entry_by_query(query_raw)

    if key and data:
        # display the user's typed short form as the prefix (title-cased), but prefer a nicer short name
        display_name = query_raw
        # if the matched key is different, prefer showing the key (which is the shorthand)
        if key and key != normalize(query_raw):
            # try to present the shorthand nicely
            display_name = key.title()
        # If user typed the full name, use their typed form (query_raw) as displayed name
        # include amount if present
        amount_text = f" x{data['amount']}" if data.get("amount") else ""
        await message.channel.send(f"**{display_name}** **[{data['full']}]** is on **{data['tier']}** Tier!{amount_text}")
    else:
        await message.channel.send(f"💔 Sorry, I don't know **{query_raw}**TT")


# ============
# run
# ============
client.run(os.getenv("TOKEN"))
