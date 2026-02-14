import discord
import os
import re
import asyncio
import shutil
print("FFMPEG:", shutil.which("ffmpeg"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# --- Take-control global state ---
TAKE_CONTROL = False
TAKE_CONTROL_ALLOWED = {
    "joinvc",
    "send",
    "sendimg",
    "sendvideo",
    "leave",
    "dc",
    "disconnect",
}

# ตั้งค่านี้เพื่อเปลี่ยน tolerance ได้ (ค่า 0.10 = 10%)
TOLERANCE = 0.10

# ============
# Pixel sound settings (adjust as needed)
# ============
PIXEL_SOUND = "./PIXEL_SOUND.wav"  # path to your pixel blip sound
PIXEL_SPEED = 0.7  # default interval between blips (seconds)

# ======================
# TIERS DATA ... (UNCHANGED)
# ======================
TIERS = {
    # ===== U =====
    "asgore": {"full": "Acerola | King of Monsters", "tier": "U", "value": 200000},

    # ===== EX =====
    "solemn": {"full": "Cross | Butterflies' Funeral", "tier": "EX", "value": 20000},

    # ===== S =====
    "cross": {"full": "Cross", "tier": "S", "value": 10000, "allias": ["xsans", "cross sans", "crosssans", "x-sans", "x!sans", "x sans", "x! sans"]},
    "uf": {"full": "Undying Flame", "tier": "S", "value": 7300},
    "vst": {"full": "Valentine Summer Time", "tier": "S", "value": 7000},
    "ewu rgb": {"full": "Eternal Wing | RGB | UNLEASHED", "tier": "S", "value": 6520, "allias": ["ew:u rgb", "ewurgb", "ew u rgb"]},
    "mkvol": {"full": "Midknight Vessel of Life", "tier": "S", "value": 5000, "allias": ["mk vol", "vol"]},
    "mkvolts": {"full": "Midknight Vessel of Life | Taped Shut", "tier": "S", "value": 5500, "allias": ["mk volts", "volts", "taped shut"]},
    "mimivol": {"full": "Midknight Vessel of Life | Mimicry", "tier": "S", "value": 4000, "allias": ["mimi", "mkvol mimicry"]},

    # ===== A =====
    "wh": {"full": "Wild Hunt", "tier": "A", "value": 3500, "allias": ["wildhunt"]},
    "soc": {"full": "Soul of Cinder", "tier": "A", "value": 3250},
    "nerd": {"full": "Standless | Nerd", "tier": "A", "value": 1700},
    "coco": {"full": "Rainy Time | Coco", "tier": "A", "value": 1700, "allias":["rainy time coco"]},
    "tuna": {"full": "Anubis Requiem | Tuna", "tier": "A", "value": 3500},
    "ewu": {"full": "Eternal Wing | Unleashed", "tier": "A", "value": 1630, "allias": ["ew:u", "ew u"]},
    "5th sinner": {"full": "Lei Heng | The 5th Sinner", "tier": "A", "value": 1380},
    "fx!chara": {"full": "X!Chara : Frostbite", "tier": "A", "value": 1380, "allias": ["fxchara", "x!chara frostbite", "xcharaf", "x!charaf", "x!chara f", "xchara f"]},
    "duf": {"full": "Dullahan | Unyielding Frost", "tier": "A", "value": 1135},
    "se": {"full": "Singularity Essence", "tier": "A", "value": 1300},
    "mkb": {"full": "Midknight", "tier": "A", "value": 1135, "allias": ["mk", "seele"]},
    "hx!chara": {"full": "X!Chara | Hallowed", "tier": "A", "value": 1000, "allias": ["hxchara", "x!chara hallowed", "xchara hallowed"]},
    "dull": {"full": "Remembrance of Dullahan", "tier": "A", "value": 945},
    "x!chara": {"full": "X!Chara", "tier": "A", "value": 920, "allias": ["xchara", "x chara"]},
    "agnes": {"full": "Okarun | Agnes Tachyon", "tier": "A", "value": 870},
    "rukia ws": {"full": "Rukia Kuchiki : Winter Season", "tier": "A", "value": 870, "allias": ["rukiaws"]},
    "rukia": {"full": "Rukia Kuchiki", "tier": "A", "value": 835},
    "goldship requiem": {"full": "Gold Ship Experience Requiem", "tier": "A", "value": 845, "allias": ["gold ship req", "goldship req"]},
    "goldship experience": {"full": "Goldship Experience", "tier": "A", "value": 835},
    "spin ce": {"full": "Spin | Singularity Essence", "tier": "A", "value": 960},
    "aizen evo": {"full": "Aizen Sosuke (Hogyoku Fusion)", "tier": "A", "value": 835},
    "aizen": {"full": "Aizen Sosuke", "tier": "A", "value": 650},
    "ronin ce": {"full": "Ronin | Crimson Eclipse", "tier": "A", "value": 835},
    "ronin awk": {"full": "Ronin (Successor of Niten Ichiryu)", "tier": "A", "value": 850},
    "pk": {"full": "Pilgrim Knight", "tier": "A", "value": 780},
    "starrk": {"full": "Coyote Starrk", "tier": "A", "value": 750},
    "satono": {"full": "Satono Crazy Diamond", "tier": "A", "value": 750},
    "kamen rider": {"full": "Black Silence | Kamen Rider Gaim", "tier": "A", "value": 750},
    "will of fate": {"full": "Will of Fate", "tier": "A", "value": 1300},
    "bonnie": {"full": "Kaiju No.8 | Kaiju of 1987", "tier": "A", "value": 850},
    "friren ru": {"full": "Frieren | Red Usurper", "tier": "A", "value": 750},
    "acerola": {"full": "Acerola", "tier": "A", "value": 850},
    "vergil": {"full": "True Anubis | Vergil", "tier": "A", "value": 790},
    "fist of chaos": {"full": "Cyber Skeleton | Fist of Chaos", "tier": "A", "value": 750},
    "faceless one": {"full": "Metallica | Faceless One", "tier": "A", "value": 730},
    "anubis mm": {"full": "Anubis | Masquerade Meltdown", "tier": "A", "value": 730},
    "wouap": {"full": "Wonder of U | Altered Palette", "tier": "A", "value": 750},
    "gura": {"full": "Rainy Time | Gawr Gura", "tier": "A", "value": 810},
    "isaac": {"full": "Nikyu Nikyu no mi | Isaac", "tier": "A", "value": 750},
    "izutsumi": {"full": "Eggxeed | Izutsumi", "tier": "A", "value": 850},
    "eggxeed": {"full": "Eggxeed", "tier": "A", "value": 800},
    "troll mask": {"full": "Troll Mask", "tier": "A", "value": 650},
    "st genderbend": {"full": "Summer Time | Genderbend", "tier": "A", "value": 650},
    "golden egg": {"full": "Golden Egg", "tier": "A", "value": 650},
    "spin candy": {"full": "Spin | Candy", "tier": "A", "value": 600},

    #B
    "ta": {"full": "True Anubis", "tier": "B", "value": 800},
    "cd pumpkin": {"full": "Crazy Diamond | Pumpkin", "tier": "B", "value": 410},
    "spoon": {"full": "Stop Sign | Comically Large Spoon", "tier": "B", "value": 760},
    "easter egg": {"full": "Easter Egg", "tier": "B", "value": 500},
    "sibuna": {"full": "Anubis | Sibuna", "tier": "B", "value": 760},
    "bunny suit": {"full": "Summer Time | Bunny Suit", "tier": "B", "value": 760},
    "ar": {"full": "Anubis Requiem", "tier": "B", "value": 400},
    "astolfosp": {"full": "Astolfo | Sailor Paladin", "tier": "B", "value": 650},
    "astolfo": {"full": "Astolfo (Saber)", "tier": "B", "value": 600},
    "astolfots": {"full": "Astolfo | Taped Shut", "tier": "B", "value": 550},
    "cirno": {"full": "Hie Hie | The Strongest Fairy", "tier": "B", "value": 660},
    "eggwand": {"full": "Stop Sign | Egg Wand", "tier": "B", "value": 660},
    "deku": {"full": "Deku", "tier": "B", "value": 700},
    "frieren": {"full": "Frieren", "tier": "B", "value": 660},
    "stw devil": {"full": "Shadow The World | Devil", "tier": "B", "value": 610},
    "sandeh": {"full": "Sandevistan : Holiday 2077", "tier": "B", "value": 780},
    "sandhs": {"full": "Sandevistan : Holiday Skeleton 2077", "tier": "B", "value": 760},
    "infernal bard": {"full": "Stop Sign | Infernal Bard", "tier": "B", "value": 700},
    "mih": {"full": "Made In Heaven", "tier": "B", "value": 680},
    "gigamesh": {"full": "Gilgamesh (Archer)", "tier": "B", "value": 650},
    "cidgo": {"full": "Cid Kagenou | Galactic Overlord", "tier": "B", "value": 490},
    "bandits slayer": {"full": "Cid Kagenou | Stylish Bandits Slayer", "tier": "B", "value": 450},
    "wsmm": {"full": "White Snake | Marshmallow", "tier": "B", "value": 625},
    "wts": {"full": "Winter Time | Santa", "tier": "B", "value": 620},
    "hina": {"full": "Sorasaki Hina", "tier": "B", "value": 610},
    "egg keeper": {"full": "Egg Keeper", "tier": "B", "value": 610},
    "kokushibo": {"full": "Moon Breathing | Hybrid Demon", "tier": "B", "value": 510},
    "nokotan": {"full": "Nokotan", "tier": "B", "value": 630},
    "cid": {"full": "Cid Kagenou", "tier": "B", "value": 410},
    "roland": {"full": "The Black Silence", "tier": "B", "value": 400},
    "akaza": {"full": "Akaza", "tier": "B", "value": 400},
    "carrot": {"full": "Carrot (Electro)", "tier": "B", "value": 610},
    "sende evo": {"full": "Sandevistan : Cyber Skeleton", "tier": "B", "value": 510},
    "sande": {"full": "Sandevistan", "tier": "B", "value": 460},
    "wou": {"full": "Wonder of U", "tier": "B", "value": 410},
    "kaiju no.8": {"full": "Kaiju No.8", "tier": "B", "value": 410},
    "sp shadow": {"full": "Star Platinum | Shadow Master", "tier": "B", "value": 410},
    "lunatic red eyes": {"full": "Emperor | Lunatic Red Eyes", "tier": "B", "value": 550},
    "gojo 1/2": {"full": "Gojo Satoru | 1/2", "tier": "B", "value": 610},
    "holy wreath": {"full": "Standless | Holy Wreath", "tier": "B", "value": 550},
    "st witch": {"full": "Summer Time | Witch", "tier": "B", "value": 475},
    "alucard": {"full": "Alucard", "tier": "B", "value": 600},
    "stw easter": {"full": "Shadow The World | Easter", "tier": "B", "value": 410},
    "lightsaber": {"full": "Anubis | Lightsaber", "tier": "B", "value": 600},
    "stop scythe": {"full": "Stop Sign | Stop Scythe", "tier": "B", "value": 410},
    "lei heng captain rampage": {"full": "Lei Heng | Captain Rampage", "tier": "B", "value": 410},
    "death certificate": {"full": "Death Certificate", "tier": "B", "value": 410},
    "stdd": {"full": "Star Platinum : Dragon Dance", "tier": "B"},
    "ger azael": {"full": "Gold Experience Requiem | Azael", "tier": "B", "value": 410},
    "mita": {"full": "Shadow The World | Mita", "tier": "B", "value": 410},
    "twf": {"full": "The World : Frozen", "tier": "B", "value": 410},
    "cdc": {"full": "Crazy Diamond | Crystallized", "tier": "B", "value": 410},
    "Sancho": {"full": "Sancho", "tier": "B", "Value": 400},

    #C
    "5 fingers": {"full": "5 Sukuna's Cursed Fingers", "tier": "C", "value": 150},
    "rusted sword": {"full": "Rusted Sword", "tier": "C", "value": 345},
    "okarun egg": {"full": "Okarun | Egg of All-devouring Darkness", "tier": "C", "value": 400},
    "getothm": {"full": "Suguru Geto | The Hunt Master", "tier": "C", "value": 365},
    "gojo": {"full": "Gojo Satoru", "tier": "C", "value": 380},
    "hog": {"full": "Hogyoku Fragment", "tier": "C", "value": 70},
    "sukuna": {"full": "Ryomen Sukuna", "tier": "C", "value": 380},
    "geto": {"full": "Suguru Geto", "tier": "C", "value": 320},
    "toji": {"full": "Toji Fushiguro", "tier": "C", "value": 365},
    "stop sign candy cane": {"full": "Stop Sign | Candy Cane", "tier": "C", "value": 360},
    "oa's grace": {"full": "OA's Grace", "tier": "C", "value": 340},
    "anubis spook": {"full": "Anubis | Spook", "tier": "C", "value": 400},
    "hamon frost": {"full": "Hamon | Frost", "tier": "C", "value": 370},
    "hohe": {"full": "Herrscher of Human Ego", "tier": "C", "value": 360},
    "cmoon": {"full": "C-Moon", "tier": "C", "value": 340},
    "baiken": {"full": "Baiken", "tier": "C", "value": 340},
    "sanji sakurian": {"full": "Sanji (Sakurian)", "tier": "C", "value": 380},
    "okarun": {"full": "Okarun", "tier": "C", "value": 320},
    "ichigo": {"full": "Kurosaki Ichigo", "tier": "C", "value": 265},
    "the red mist": {"full": "The Red Mist", "tier": "C", "value": 265},
    "sanji": {"full": "Sanji", "tier": "C", "value": 100},
    "garou sakurian": {"full": "Garou | Water Stream Rock Smashing Fist (Sakurian)", "tier": "C", "value": 150},
    "arasaka": {"full": "Arasaka Suitcase", "tier": "C", "value": 120},
    "ew rgb": {"full": "Eternal Wing | RGB", "tier": "C", "value": 125},
    "yuta": {"full": "Okkotsu Yuta", "tier": "C", "value": 50},
    "sakuya": {"full": "Sakuya Izayoi", "tier": "C", "value": 50},
    "yuji": {"full": "Itadori Yuji", "tier": "C", "value": 60},
    "lei heng": {"full": "Lei Heng", "tier": "C", "value": 220},
    "stop sign regret": {"full": "Stop Sign | Regret", "tier": "C", "value": 100},
    "bag of presents": {"full": "Bag of Present", "tier": "C", "amount": 5, "value": 140},
    "ger": {"full": "Gold Experience Requiem", "tier": "C", "value": 60},
    "padoru": {"full": "Padoru", "tier": "C", "value": 73},
    "emperor headhunter": {"full": "Emperor | Headhunter", "tier": "C", "value": 53},
    "stop sign bisento": {"full": "Stop Sign | Bisento", "tier": "C", "value": 45},

    #D
    "hamon": {"full": "Hamon | Akaza", "tier": "D", "value": 40},
    "tw": {"full": "The World", "tier": "D", "value": 35},
    "nikyu": {"full": "Nikyu Nikyu no mi Fruit", "tier": "D", "value": 73},
    "dio's diary": {"full": "Dio's Diary", "tier": "D", "value": 50},
    "cyberware": {"full": "Cyberware", "tier": "D", "value": 37},
    "garou": {"full": "Garou | Water Stream Rock Smashing Fist", "tier": "D", "value": 50},
    "mochi awk": {"full": "Mochi Mochi no mi | Conqueror", "tier": "D", "value": 50},
    "hie": {"full": "Hie Hie no mi Fruit", "tier": "D", "value": 30},
    "shinra": {"full": "Shinra Kusakabe", "tier": "D","value": 30},
    "ew": {"full": "Eternal Wing", "tier": "D", "value": 30},
    "hof": {"full": "Herrscher of Flamescion", "tier": "D", "value": 30},
    "kujo's hat": {"full": "Kujo's Hat", "tier": "D", "value": 23},
    "silver egg": {"full": "Silver Egg", "tier": "D", "value": 20},

    # (ตัวอย่างพิเศษ — สามารถลบหรือแก้ได้ตามต้องการ)
    "bronya": {"full": "Furi's Wife", "tier": "SPECIAL", "value": 999999},
    "bronya zaychik": {"full": "Furi's Wife", "SPECIAL": "SSR", "value": 999999},
    "bronya rand": {"full": "Furi's Wife", "SPECIAL": "SSR", "value": 999999},
    "silver wolf": {"full": "Furi's Wife", "SPECIAL": "SSR", "value": 999999},
    "silverwolf": {"full": "Furi's Wife", "SPECIAL": "SSR", "value": 999999},
    "Furi": {"full": "Furidamu", "tier": "Bronya's Wife", "value": 171108},
}

# ============
# Update log data (example)
# ============
UPDATE_LOG = {
    "version": "1.6",
    "title": "FuriBOT update version 1.6!",
    "changes": [
        "Added a new command to check the update log! `@FuriBOT update`",
        "Adjusted balance values for some specs!",
        "Improved and expanded search keywords for S-tier specs!",
        "Adjust the wording and style to be softer so it can be used in large servers without any issues!",
    ],
    "date": "02/06/2026",
}

def build_update_message(log: dict) -> str:
    version = log.get("version", "?")
    changes = log.get("changes", [])
    date = log.get("date", "Unknown")

    line = "🌸═════════════🌸"

    out = []
    out.append(line)
    out.append(f"💮  **Update version {version}!** 💮")
    out.append(line)
    out.append("")
    out.append("✨ What’s new~ ✨")
    out.append("૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ा")
    out.append("")

    if changes:
        for c in changes:
            out.append(f"💮 {c}")
            out.append("")  # เว้นบรรทัดให้โล่ง น่ารักขึ้น
    else:
        out.append("💮 There's nothing new yet~")
        out.append("")

    out.append(line)
    out.append(f"      📅 Date: **{date}**")
    out.append(line)

    return "\n".join(out)
    
# ============
# helpers
# ============
def normalize(s: str) -> str:
    """Lowercase, trim spaces, collapse spaces, remove surrounding punctuation"""
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip(" '\"`.,:;-()[]{}")


def _get_alias_list(data):
    """Return list of aliases from a tier entry (supports many spellings)."""
    for k in ("alias", "aliases", "allias", "alliases"):
        v = data.get(k)
        if not v:
            continue
        if isinstance(v, str):
            return [v]
        if isinstance(v, (list, tuple)):
            return list(v)
    return []


def find_entry_by_query(q: str):
    """
    Improved matching:
    - exact key match (TIERS key)
    - normalized key / full-name match
    - exact alias match (supports alias / aliases / allias fields)
    - fallback: token-overlap scoring (choose best match by shared tokens)
    Returns tuple (key, data) or (None, None)
    """
    q_norm = normalize(q)
    q_tokens = set(q_norm.split()) if q_norm else set()

    # 1) direct key match (exact)
    if q_norm in TIERS:
        return q_norm, TIERS[q_norm]

    # 2) try match normalized keys, full names, aliases (exact)
    for key, data in TIERS.items():
        if normalize(key) == q_norm:
            return key, data
        if normalize(data.get("full", "")) == q_norm:
            return key, data
        for a in _get_alias_list(data):
            if normalize(a) == q_norm:
                return key, data

    # 3) token-overlap scoring fallback (helps when user puts spaces or partial words)
    best = None
    best_score = 0
    best_fraction = 0.0
    for key, data in TIERS.items():
        candidates = [data.get("full", ""), key] + _get_alias_list(data)
        for name in candidates:
            name_norm = normalize(name)
            if not name_norm:
                continue
            name_tokens = set(name_norm.split())
            if not name_tokens:
                continue
            inter = q_tokens & name_tokens
            score = len(inter)
            if score == 0:
                continue
            fraction = score / len(name_tokens)
            if (score > best_score) or (score == best_score and fraction > best_fraction):
                best = (key, data)
                best_score = score
                best_fraction = fraction

    if best:
        return best[0], best[1]

    # 4) last-resort partial containment (like "vergil" in "True Anubis | Vergil")
    for key, data in TIERS.items():
        full_norm = normalize(data.get("full", ""))
        if q_norm in full_norm or full_norm in q_norm:
            return key, data

    return None, None


def get_toplist_by_tier(tier: str):
    """Return list of entries in given tier sorted by value desc"""
    t_norm = tier.strip().upper()
    items = []
    for key, data in TIERS.items():
        t = data.get("tier", data.get("SPECIAL", "")).upper()
        if t == t_norm:
            items.append({
                "key": key,
                "full": data.get("full", key),
                "value": data.get("value", 0)
            })
    items.sort(key=lambda x: (x["value"] if x["value"] is not None else 0), reverse=True)
    return items


# ============
# value / calc helpers (ใช้ TIERS เป็นแหล่งข้อมูล)
# ============
def parse_multiplier_and_key(raw_item: str):
    item = raw_item.strip()
    m = re.search(r"^(.*?)[\s]*[x×]\s*(\d+)\s*$", item, flags=re.IGNORECASE)
    if m:
        name = m.group(1).strip()
        count = int(m.group(2))
        return normalize(name), count, name
    return normalize(item), 1, item


def calc_value(item_list):
    total = 0
    unknown = []
    details = []

    for raw in item_list:
        if not raw or not raw.strip():
            continue
        key_norm, mult, original = parse_multiplier_and_key(raw)
        key, data = find_entry_by_query(key_norm)
        if not data:
            unknown.append(original)
            continue

        base_value = data.get("value", 0) or 0
        amount_defined = data.get("amount")
        if amount_defined and mult == 1:
            mult = amount_defined

        item_total = base_value * mult
        total += item_total

        if mult != 1:
            details.append(f"{data['full']} x{mult} (+{base_value} each → +{item_total})")
        else:
            details.append(f"{data['full']} (+{base_value})")

    return total, unknown, details


def wfl_command(raw_text: str):
    text = raw_text.strip()
    low = text.lower()

    if "my " not in low or " for " not in low:
        return "❌ Format: `my item1+item2 for itemA+itemB`"

    try:
        start_my = low.index("my ")
        start_for = low.rindex(" for ")
        my_part = text[start_my + 3:start_for].strip()
        other_part = text[start_for + 5:].strip()
    except Exception:
        return "❌ Invalid format (ต้องมี `my` และ `for`)"

    if not my_part or not other_part:
        return "❌ กรุณาใส่รายการหลัง `my` และ `for`"

    my_items = [i.strip() for i in my_part.split("+") if i.strip()]
    other_items = [i.strip() for i in other_part.split("+") if i.strip()]

    my_value, my_unknown, my_details = calc_value(my_items)
    other_value, other_unknown, other_details = calc_value(other_items)

    if my_unknown or other_unknown:
        return (
            "⚠️ Unknown items detected:\n"
            f"My: {', '.join(my_unknown) if my_unknown else 'None'}\n"
            f"Other: {', '.join(other_unknown) if other_unknown else 'None'}"
        )

    if my_value == 0 and other_value == 0:
        result = "F ⚖️"
    else:
        diff = abs(my_value - other_value)
        tolerance_value = max(my_value, other_value) * TOLERANCE
        if diff <= tolerance_value:
            result = "F ⚖️"
        elif my_value > other_value:
            result = "L 😡"
        else:
            result = "W 🥰"

    out_lines = []
    out_lines.append(f"**Your value:** {my_value}")
    for d in my_details:
        out_lines.append(f"• {d}")
    out_lines.append("")
    out_lines.append(f"**Other value:** {other_value}")
    for d in other_details:
        out_lines.append(f"• {d}")
    out_lines.append("")
    out_lines.append(f"**Result:** {result}")

    return "\n".join(out_lines)


# --- helper สำหรับสร้าง list ของทุกเทียร์/ตัวละคร ---
def build_full_tier_messages():
    preferred_order = ["U", "EX", "S", "A", "B", "C", "D", "SSR", "SPECIAL", "UNKNOWN"]
    groups = {}
    for key, data in TIERS.items():
        tier = data.get("tier", data.get("SPECIAL", "UNKNOWN"))
        full = data.get("full", key)
        amount = data.get("amount")
        value = data.get("value", "N/A")
        extra_amount = f" x{amount}" if amount else ""
        display = f"{full} — Tier: {tier} — Value: {value}{extra_amount}  (key: {key})"
        groups.setdefault(tier, []).append(display)

    messages = []
    for t in preferred_order:
        items = groups.get(t, [])
        if not items:
            continue
        header = f"======== {t} Tier ========\n"
        body = "\n".join(items)
        messages.append(header + body)

    for t, items in groups.items():
        if t in preferred_order:
            continue
        header = f"======== {t} Tier ========\n"
        body = "\n".join(items)
        messages.append(header + body)

    return messages


# --- helper สำหรับส่งข้อความยาวเป็นชิ้น ๆ ---
async def send_long_message(channel, text):
    if len(text) <= 1900:
        await channel.send(text)
        return

    lines = text.split("\n")
    chunk = []
    size = 0
    for ln in lines:
        ln_with_n = ln + "\n"
        if size + len(ln_with_n) > 1900 and chunk:
            await channel.send("".join(chunk))
            chunk = []
            size = 0
        chunk.append(ln_with_n)
        size += len(ln_with_n)
    if chunk:
        await channel.send("".join(chunk))

# ============
# New helper: play pixel-style sound according to text
# ============
async def play_text_sound(
    vc: discord.VoiceClient,
    text: str,
    sound_path: str = PIXEL_SOUND,
    speed: float = 0.04
):

    if not vc or not vc.is_connected():
        return

    if vc.is_playing():
        vc.stop()

    max_chars = 300
    play_text = text[:max_chars]

    async def start_loop():
        source = discord.FFmpegPCMAudio(
            sound_path,
            before_options="-stream_loop -1",
            options="-loglevel quiet"
        )
        vc.play(source)

    async def stop_loop():
        if vc.is_playing():
            vc.stop()

    for ch in play_text:

        # เว้นวรรค = หยุดสั้น ๆ
        if ch == " ":
            await stop_loop()
            await asyncio.sleep(speed * 1.8)
            await start_loop()
            continue

        # ขึ้นบรรทัดใหม่
        if ch == "\n":
            await stop_loop()
            await asyncio.sleep(speed * 3)
            await start_loop()
            continue

        # จบประโยค
        if ch in [".", "!", "?", "…"]:
            await stop_loop()
            await asyncio.sleep(speed * 4)
            await start_loop()
            continue

        # ถ้ายังไม่เล่น ให้เริ่ม
        if not vc.is_playing():
            await start_loop()

        await asyncio.sleep(speed)

    # ทำให้ไม่ตัดห้วน
    await asyncio.sleep(0.45)
    await stop_loop()

# ============
# events
# ============
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="I love Bronya so much"
        )
    )
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # CONFIG: เปลี่ยนให้เป็น set ของ channel ids ที่ต้องการให้ auto-reply ทำงาน (หรือ leave empty เพื่อไม่จำกัด)
    AUTO_REPLY_CHANNELS = {1468374226850287619}  # ตัวอย่าง: ใส่ channel ID ที่อนุญาต
    OWNER_ID = 1471586942352359621               # ใส่ user ID ของคุณ (ถ้าไม่ใช้ ให้ตั้งเป็น None)

    content = message.content or ""
    content = content.strip()

    # ไม่สนใจข้อความเปล่า (ก็ยังตรวจ attachments เฉพาะคำสั่ง sendimg/sendvideo)
    if not content and not message.attachments:
        return

    # ตรวจว่าถูก mention ไหม
    is_mentioned = client.user in message.mentions

    # We will process commands if either:
    #  - message is in AUTO_REPLY_CHANNELS  (so users can type plain keywords there)
    #  - or bot is mentioned (normal commands via mention)
    can_process = (message.channel.id in AUTO_REPLY_CHANNELS) or is_mentioned

    if not can_process:
        return

    # Prepare command text:
    # If mentioned, strip mention forms; else use content as-is for auto-reply mode.
    raw = content
    if is_mentioned:
        try:
            raw = raw.replace(client.user.mention, "")
            # also remove <@123...> or <@!123...>
            raw = re.sub(rf"<@!?\s*{client.user.id}\s*>", "", raw)
        except Exception:
            raw = re.sub(rf"<@!?\d+>", "", raw)
    raw = raw.strip()
    raw = re.sub(r"\s+", " ", raw).strip()

    # If nothing left after removing mention, send hint (mention mode)
    if is_mentioned and not raw:
        await message.channel.send("🌸 Heyya! I'm here trying to use `@FuriBOT help` to see all command!")
        return

    # ---------- enforce take-control mode ----------
    global TAKE_CONTROL
    if TAKE_CONTROL:
        verb = raw.split()[0].lower() if raw else ""
        # allow owner to disable it (owner can still use takecontrol)
        if not (raw.lower().startswith("takecontrol") and OWNER_ID and message.author.id == OWNER_ID):
            if verb not in TAKE_CONTROL_ALLOWED:
                # silent block (do nothing)
                return

    # Normalize lower command for parsing
    cmd = raw.lower().strip()
    parts = cmd.split()

    # ===== TAKECONTROL =====
    if cmd.startswith("takecontrol"):
        if OWNER_ID and message.author.id != OWNER_ID:
            await message.channel.send("🔒 Only owner can use takecontrol.")
            return

        p = raw.split()
        if len(p) < 2:
            await message.channel.send("Usage: `@FuriBOT takecontrol <on|off>`")
            return

        if p[1].lower() in ["on", "enable", "true", "1"]:
            TAKE_CONTROL = True
            await message.channel.send("🔐 Take control ENABLED.")
        elif p[1].lower() in ["off", "disable", "false", "0"]:
            TAKE_CONTROL = False
            await message.channel.send("🔓 Take control DISABLED.")
        else:
            await message.channel.send("Use `on` or `off`.")
        return

    # ===== HELP COMMAND =====
    if cmd in ["help", "commands", "cmd", "h"]:
        await message.channel.send(
            "🌸 **HELP | FuriBOT** 🌸\n\n"
            "════════════════════\n"
            "📜 **ALL COMMANDS**\n"
            "════════════════════\n\n"
            "💮 **tierlist**\n"
            "→ `tierlist all` shows full list; `tierlist` (image not implemented) \n\n"
            "💮 **list <tier>** or **list all**\n"
            "→ Show specs in a tier or all (text)\n\n"
            "💮 **toplist <tier> [N]**\n"
            "→ Show top N specs in that tier\n\n"
            "💮 **find <name>**\n"
            "→ Find spec Tier & Value\n\n"
            "💮 **my <items> for <items>**\n"
            "→ Check W / F / L by value (e.g. `my ew rgb for ewux4`)\n\n"
            "💮 **check / update / changelog**\n"
            "→ Show latest update log\n\n"
            "════════════════════"
        )
        return

    # ===== REMOTE SEND (cross-server text) =====
    DEFAULT_REMOTE_CHANNEL_ID = 1468374226850287619  # แก้เป็นค่า default ของคุณ
    if cmd.startswith("send "):
        # owner-only
        if OWNER_ID and message.author.id != OWNER_ID:
            await message.channel.send("🔒 Permission denied. Only the owner can use `send`.")
            return

        parts_raw = raw.split(" ", 2)
        if len(parts_raw) == 1 or (len(parts_raw) == 2 and not parts_raw[1].strip()):
            await message.channel.send("❌ Usage: `@FuriBOT send [<channel_id>] <message>`")
            return

        target_channel_id = None
        message_text = None

        if len(parts_raw) >= 3 and re.fullmatch(r"\d{17,19}", parts_raw[1]):
            try:
                target_channel_id = int(parts_raw[1])
                message_text = parts_raw[2].strip()
            except Exception:
                target_channel_id = None
        elif len(parts_raw) >= 3 and parts_raw[1].startswith("<#") and parts_raw[1].endswith(">"):
            m = re.search(r"\d+", parts_raw[1])
            if m:
                target_channel_id = int(m.group(0))
                message_text = parts_raw[2].strip()
        else:
            target_channel_id = DEFAULT_REMOTE_CHANNEL_ID
            message_text = raw[len("send "):].strip()

        if not message_text:
            await message.channel.send("❌ No message provided to send.")
            return

        channel = client.get_channel(target_channel_id)
        if channel is None:
            await message.channel.send("❌ Target channel not found or bot is not in that channel's server.")
            return

        try:
            await channel.send(message_text)
            try:
                vc = channel.guild.voice_client
                if vc and vc.is_connected():
                    await play_text_sound(vc, message_text)
            except Exception:
                pass
        except Exception as e:
            await message.channel.send(f"💔 Failed to send message: {e}")
            return

        await message.channel.send("✅ Message forwarded successfully!")
        return

    # ===== JOIN VOICE CROSS-SERVER =====
    if cmd.startswith("joinvc"):
        if OWNER_ID and message.author.id != OWNER_ID:
            await message.channel.send("🔒 Permission denied. Only the owner can use `joinvc`.")
            return

        p = raw.split()
        if len(p) < 2:
            await message.channel.send("❌ Usage: `@FuriBOT joinvc <voice_channel_id>`")
            return

        voice_channel_id = None
        if re.fullmatch(r"\d{17,19}", p[1]):
            voice_channel_id = int(p[1])
        elif p[1].startswith("<#") and p[1].endswith(">"):
            m = re.search(r"\d+", p[1])
            if m:
                voice_channel_id = int(m.group(0))
        else:
            await message.channel.send("❌ Invalid channel id. Use numeric channel id or <#channel_mention>.")
            return

        channel = client.get_channel(voice_channel_id)
        if channel is None:
            await message.channel.send("❌ Voice channel not found or bot is not in that channel's server.")
            return

        if not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
            await message.channel.send("❌ The provided ID is not a voice channel.")
            return

        try:
            await channel.connect()
            await message.channel.send(f"🎧 Joined voice channel **{channel.name}**")
        except discord.ClientException:
            await message.channel.send("⚠️ Bot is already connected to a voice channel.")
        except Exception as e:
            await message.channel.send(f"💔 Failed to join voice: {e}")
        return

    # ===== LEAVE / DISCONNECT (supports optional channel/guild id to leave across servers) =====
    if cmd.startswith("leave") or cmd.startswith("disconnect") or cmd.startswith("dc"):
        p = raw.split()
        target_guild = None
        if len(p) >= 2 and re.fullmatch(r"\d{17,19}", p[1]):
            cid = int(p[1])
            ch = client.get_channel(cid)
            if ch:
                target_guild = ch.guild
            else:
                g = client.get_guild(cid)
                if g:
                    target_guild = g
        else:
            target_guild = message.guild

        if not target_guild:
            await message.channel.send("❌ Server/channel not found or bot not in that server.")
            return

        vc = target_guild.voice_client
        if vc and vc.is_connected():
            try:
                await vc.disconnect()
                await message.channel.send("👋 Left the voice channel.")
            except Exception as e:
                await message.channel.send(f"💔 Failed to leave voice: {e}")
        else:
            await message.channel.send("❌ I'm not in a voice channel in that server.")
        return

    # ===== SEND IMAGE CROSS-SERVER =====
    if cmd.startswith("sendimg"):
        if OWNER_ID and message.author.id != OWNER_ID:
            await message.channel.send("🔒 Permission denied. Only the owner can use `sendimg`.")
            return

        parts_raw = raw.split(" ", 2)
        if len(parts_raw) < 2:
            await message.channel.send("❌ Usage: `@FuriBOT sendimg <channel_id>` (attach image files)")
            return

        target_channel_id = None
        if re.fullmatch(r"\d{17,19}", parts_raw[1]):
            target_channel_id = int(parts_raw[1])
        elif parts_raw[1].startswith("<#") and parts_raw[1].endswith(">"):
            m = re.search(r"\d+", parts_raw[1])
            if m:
                target_channel_id = int(m.group(0))
        else:
            await message.channel.send("❌ Invalid channel id. Use numeric channel id or <#channel_mention>.")
            return

        target_channel = client.get_channel(target_channel_id)
        if target_channel is None:
            await message.channel.send("❌ Target channel not found or bot is not in that channel's server.")
            return

        if not message.attachments:
            await message.channel.send("🖼️ Please attach at least one image to relay.")
            return

        MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB default limit (adjust if your server boost allows larger)
        sent = 0
        skipped = []
        failed = []

        for att in message.attachments:
            is_image = False
            if att.content_type:
                is_image = att.content_type.startswith("image")
            else:
                fn = att.filename.lower()
                is_image = any(fn.endswith(ext) for ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"))

            if not is_image:
                skipped.append(att.filename)
                continue

            if att.size is not None and att.size > MAX_FILE_SIZE:
                try:
                    await target_channel.send(f"🟣 Image from **Furi** (file too large to attach): {att.url}")
                    sent += 1
                except Exception as e:
                    failed.append((att.filename, str(e)))
                continue

            try:
                file = await att.to_file()
                await target_channel.send(content=f"🟣 Image from **Furi**", file=file)
                sent += 1
            except Exception as e:
                failed.append((att.filename, str(e)))

        rep_lines = []
        rep_lines.append(f"✅ Sent: {sent}")
        if skipped:
            rep_lines.append(f"⚠️ Skipped (not images): {', '.join(skipped)}")
        if failed:
            rep_lines.append("💔 Failed:")
            for fn, err in failed:
                rep_lines.append(f"- {fn}: {err}")

        await send_long_message(message.channel, "\n".join(rep_lines))
        return

    # ===== SEND VIDEO CROSS-SERVER =====
    if cmd.startswith("sendvideo"):
        if OWNER_ID and message.author.id != OWNER_ID:
            await message.channel.send("🔒 Permission denied. Only the owner can use `sendvideo`.")
            return

        parts_raw = raw.split(" ", 2)
        if len(parts_raw) < 2:
            await message.channel.send("❌ Usage: `@FuriBOT sendvideo <channel_id>` (attach video files)")
            return

        target_channel_id = None
        if re.fullmatch(r"\d{17,19}", parts_raw[1]):
            target_channel_id = int(parts_raw[1])
        elif parts_raw[1].startswith("<#") and parts_raw[1].endswith(">"):
            m = re.search(r"\d+", parts_raw[1])
            if m:
                target_channel_id = int(m.group(0))
        else:
            await message.channel.send("❌ Invalid channel id. Use numeric channel id or <#channel_mention>.")
            return

        target_channel = client.get_channel(target_channel_id)
        if target_channel is None:
            await message.channel.send("❌ Target channel not found or bot is not in that channel's server.")
            return

        if not message.attachments:
            await message.channel.send("🎥 Please attach at least one video to relay.")
            return

        MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB default limit
        sent = 0
        skipped = []
        failed = []

        for att in message.attachments:
            is_video = False
            if att.content_type:
                is_video = att.content_type.startswith("video")
            else:
                fn = att.filename.lower()
                is_video = any(fn.endswith(ext) for ext in (".mp4", ".mov", ".webm", ".mkv", ".avi"))

            if not is_video:
                skipped.append(att.filename)
                continue

            if att.size is not None and att.size > MAX_FILE_SIZE:
                try:
                    await target_channel.send(f"🟣 Video from **Furi** (file too large to attach): {att.url}")
                    sent += 1
                except Exception as e:
                    failed.append((att.filename, str(e)))
                continue

            try:
                file = await att.to_file()
                await target_channel.send(content=f"🟣 Video from **Furi**", file=file)
                sent += 1
            except Exception as e:
                failed.append((att.filename, str(e)))

        rep_lines = []
        rep_lines.append(f"✅ Sent videos: {sent}")
        if skipped:
            rep_lines.append(f"⚠️ Skipped (not videos): {', '.join(skipped)}")
        if failed:
            rep_lines.append("💔 Failed:")
            for fn, err in failed:
                rep_lines.append(f"- {fn}: {err}")

        await send_long_message(message.channel, "\n".join(rep_lines))
        return

    # ===== UPDATE LOG =====
    if cmd in ["check", "update", "changelog"]:
        text = build_update_message(UPDATE_LOG)
        await send_long_message(message.channel, text)
        return

    # ===== TIERLIST / LIST / TOPLIST / WFL / FIND handling (works in AUTO_REPLY or mention) =====

    # 1) tierlist commands
    if cmd.startswith("tierlist"):
        p = raw.split()
        # if "tierlist all" -> send text list of all tiers
        if len(p) >= 2 and p[1].lower() == "all":
            msgs = build_full_tier_messages()
            for m in msgs:
                await send_long_message(message.channel, m)
            return
        else:
            # original code mentions image; here we provide textual fallback hint
            await message.channel.send("🌸 (tierlist image not configured) Try `@FuriBOT tierlist all` or `@FuriBOT help`.")
            return

    # 2) list <tier> or list all
    if cmd.startswith("list"):
        p = raw.split()
        if len(p) >= 2:
            if p[1].lower() in ["all", "everything"]:
                msgs = build_full_tier_messages()
                for m in msgs:
                    await send_long_message(message.channel, m)
                return
            else:
                tier = p[1].upper()
                items = get_toplist_by_tier(tier)
                if not items:
                    await message.channel.send(f"⚠️ No specs found for tier **{tier}**")
                    return
                lines = [f"{i}. • {it['full']} | Value: {it['value']}" for i, it in enumerate(items, start=1)]
                await send_long_message(message.channel, f"💮 LIST | Tier {tier} 💮\n\n" + "\n".join(lines))
                return
        else:
            await message.channel.send("❌ Usage: `@FuriBOT list <tier>` or `@FuriBOT list all`")
            return

    # 3) toplist <tier> [N]
    if parts and parts[0] == "toplist" and len(parts) >= 2:
        tier = parts[1].upper()
        items = get_toplist_by_tier(tier)
        if not items:
            await message.channel.send(f"⚠️ No specs found for tier **{tier}**")
            return

        n = 10
        if len(parts) >= 3 and parts[2].isdigit():
            n = max(1, int(parts[2]))

        lines = [f"{i}. • {it['full']} | Value: {it['value']}" for i, it in enumerate(items[:n], start=1)]
        await send_long_message(message.channel, f"💮 TOPLIST | Tier {tier} 💮\n\n" + "\n".join(lines))
        return

    # 4) my ... for ...
    low_content = raw.lower()
    if low_content.startswith("my ") and " for " in low_content:
        reply = wfl_command(raw)
        await message.channel.send(reply)
        return

    # 5) direct find (พิมพ์ชื่อเฉย ๆ) in AUTO_REPLY mode: if channel is auto-reply zone and text is short
    # Also support explicit "find <name>" when mentioned
    if cmd.startswith("find "):
        query_raw = raw.split(" ", 1)[1].strip()
        key, data = find_entry_by_query(query_raw)
        if data:
            full_name = data.get("full", key)
            tier_val = data.get("tier", data.get("SPECIAL", "UNKNOWN"))
            value_text = data.get("value", "N/A")
            await message.channel.send(f"**{full_name}** (key: {key}) is on **{tier_val}** Tier | Value: **{value_text}**")
        else:
            await message.channel.send(f"💔 Sorry, I don't know **{query_raw}**")
        return

    # If in AUTO_REPLY_CHANNELS and user just typed a single token (name), try direct find
    if message.channel.id in AUTO_REPLY_CHANNELS and len(parts) == 1:
        key, data = find_entry_by_query(raw)
        if data:
            full_name = data.get("full", key)
            tier_val = data.get("tier", data.get("SPECIAL", "UNKNOWN"))
            value_text = data.get("value", "N/A")
            await message.channel.send(f"**{full_name}** is on **{tier_val}** Tier | Value: **{value_text}**")
            return

    # Fallback - if bot was mentioned give help hint; otherwise stay quiet in auto-reply mode
    if is_mentioned:
        await message.channel.send("🌸 Need help? Try `@FuriBOT help` to see all commands!")
    else:
        # silent fallback for auto-reply (do nothing)
        return


# ============
# run
# ============
client.run(os.getenv("TOKEN"))
