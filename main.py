import discord
import os
import re

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ตั้งค่านี้เพื่อเปลี่ยน tolerance ได้ (ค่า 0.10 = 10%)
TOLERANCE = 0.10

# ======================
# TIERS DATA (รวม U, EX, S, A, B, C, D) — อย่าให้ตัวละครหายแม้แต่ตัวเดียว
# KEY: lower-case shorthand หรือคำที่คุณอยากพิมพ์หา
# value: dict { "full": ชื่อเต็ม, "tier": ระดับ, optional "amount": จำนวน, optional "value": numeric }
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
    "fingers": {"full": "Sukuna's Cursed Finger", "tier": "C", "amount": 5, "value": 150},
    "rusted sword": {"full": "Rusted Sword", "tier": "C", "value": 345},
    "okarun egg": {"full": "Okarun | Egg of All-devouring Darkness", "tier": "C", "value": 400},
    "getothm": {"full": "Suguru Geto | The Hunt Master", "tier": "C", "value": 365},
    "gojo": {"full": "Gojo Satoru", "tier": "C", "value": 380},
    "hog": {"full": "Hogyoku Fragment", "tier": "C", "value": 70},
    "sukuna": {"full": "Ryomen Sukuna", "tier": "C", "value": 380},
    "geto": {"full": "Suguru Geto", "tier": "C", "value": 320},
    "toji": {"full": "Toji Fushiguro", "tier": "C", "value": 365},
    "candy cane": {"full": "Stop Sign | Candy Cane", "tier": "C", "value": 360},
    "oa's grace": {"full": "OA's Grace", "tier": "C", "value": 340},
    "anubis spook": {"full": "Anubis | Spook", "tier": "C", "value": 400},
    "hamon frost": {"full": "Hamon | Frost", "tier": "C", "value": 370},
    "hohe": {"full": "Herrscher of Human Ego", "tier": "C", "value": 360},
    "c-moon": {"full": "C-Moon", "tier": "C", "value": 340},
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
    "headhunter": {"full": "Emperor | Headhunter", "tier": "C", "value": 53},
    "stop sign bisento": {"full": "Stop Sign | Bisento", "tier": "C", "value": 45},

    # ===== D =====
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
    "bronya": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "bronya zaychik": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "bronya rand": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "silver wolf": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "silverwolf": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
}

# ----------------------------
# custom textual tierlist (TIERLIST_CUSTOM)
# ----------------------------
TIERLIST_CUSTOM = {
    "U": """========**U Tier**========

Asgore (Acerola | King of Monsters)
""",
    "EX": """========**EX Tier**========

Solemn (Cross | Butterflies' Funeral)
""",
    "S": """========**S Tier**========

Cross
UF (Undying Flame)
VST (Valentine Summer Time)
EWU RGB (Eternal Wing | RGB | UNLEASHED)
MKVOL (Midknight Vessel of Life)
MKVOL TS (Midknight Vessel of Life | Taped Shut)
MIMIVOL (Midknight Vessel of Life | Mimicry)
""",
    "A": """========**A Tier**========

WH (Wild Hunt)
SOC (Soul of Cinder)
Nerd (Standless | Nerd)
Coco (Rainy Time | Coco)
Tuna (Anubis Requiem | Tuna)
EWU (Eternal Wing | Unleashed)
5th Sinner (Lei Heng | The 5th Sinner)
FXChara (X!Chara : Frostbite)
DUF (Dullahan | Unyielding Frost)
SE (Singularity Essence)
MKB (Midknight)
HXChara (X!Chara | Hallowed)
Dull (Remembrance of Dullahan)
X!Chara
Agnes (Okarun | Agnes Tachyon)
Rukia WS (Rukia Kuchiki : Winter Season)
SOTD (True Anubis : Son of the Dragon)
Rukia Kuchiki
Goldship Requiem (Gold Ship Experience Requiem)
Goldship (Goldship Experience)
Spin CE (Spin | Singularity Essence)
Aizen Evo (Aizen Sosuke | Hogyoku Fusion)
Aizen (Aizen Sosuke)
Ronin CE (Ronin | Crimson Eclipse)
Ronin Awk (Successor of Niten Ichiryu)
PK (Pilgrim Knight)
Starrk
Satono (Satono Crazy Diamond)
Kamen Rider (Black Silence | Kamen Rider Gaim)
Will of Fate
Bonnie (Kaiju No.8 | Kaiju of 1987)
Frieren RU (Frieren | Red Usurper)
Acerola
Vergil (True Anubis | Vergil)
Fist of Chaos (Cyber Skeleton | Fist of Chaos)
Faceless One (Metallica | Faceless One)
Anubis MM (Anubis | Masquerade Meltdown)
WOU AP (Wonder of U | Altered Palette)
Gura (Rainy Time | Gawr Gura)
Isaac (Nikyu Nikyu no mi | Isaac)
Izutsumi (Eggxeed | Izutsumi)
Eggxeed
Troll Mask
ST Genderbend (Summer Time | Genderbend)
Golden Egg
Spin Candy (Spin | Candy)
""",
    "B": """========**B Tier**========

TA (True Anubis)
Troll Mask (Vampirism | Troll Mask)
CD Pumpkin (Crazy Diamond | Pumpkin)
Spoon (Stop Sign | Comically Large Spoon)
Easter Egg
Sibuna (Anubis | Sibuna)
Bunny Suit (Summer Time | Bunny Suit)
AR (Anubis Requiem)
Astolfo SP (Astolfo | Sailor Paladin)
Astolfo (Saber)
Astolfo TS (Astolfo | Taped Shut)
Cirno (Hie Hie | The Strongest Fairy)
Egg Wand (Stop Sign | Egg Wand)
Deku
Frieren
STW Devil (Shadow The World | Devil)
SandeH (Sandevistan : Holiday 2077)
SandHS (Sandevistan : Holiday Skeleton 2077)
Infernal Bard (Stop Sign | Infernal Bard)
MIH (Made In Heaven)
Gilgamesh (Archer)
Cid GO (Cid Kagenou | Galactic Overlord)
Bandits Slayer (Cid Kagenou | Stylish Bandits Slayer)
WSMM (White Snake | Marshmallow)
WTS (Winter Time | Santa)
Hina (Sorasaki Hina)
Egg Keeper
Kokushibo (Moon Breathing | Hybrid Demon)
Nokotan
Cid (Cid Kagenou)
Roland (The Black Silence)
Akaza
Carrot (Electro)
Sande Evo (Sandevistan : Cyber Skeleton)
Sande (Sandevistan)
WOU (Wonder of U)
Kaiju No.8
SP Shadow (Star Platinum | Shadow Master)
Lunatic Red Eyes (Emperor | Lunatic Red Eyes)
Gojo 1/2 (Gojo Satoru | 1/2)
Holy Wreath (Standless | Holy Wreath)
ST Witch (Summer Time | Witch)
Alucard
STW Easter (Shadow The World | Easter)
Lightsaber (Anubis | Lightsaber)
Stop Scythe (Stop Sign | Stop Scythe)
Lei Heng Captain Rampage
Death Certificate
STDD (Star Platinum : Dragon Dance)
GER Azael (Gold Experience Requiem | Azael)
Mita (Shadow The World | Mita)
TWF (The World : Frozen)
CDC (Crazy Diamond | Crystallized)
""",
    "C": """========**C Tier**========

×5 Fingers (Sukuna's Cursed Finger)
Rusted Sword
Okarun Egg (Okarun | Egg of All-devouring Darkness)
Geto THM (Suguru Geto | The Hunt Master)
Gojo (Gojo Satoru)
HOG (Hogyoku Fragment)
Sukuna (Ryomen Sukuna)
Geto (Suguru Geto)
Toji (Toji Fushiguro)
Candy Cane (Stop Sign | Candy Cane)
OA's Grace
Anubis Spook (Anubis | Spook)
Hamon Frost
HoHE (Herrscher of Human Ego)
C-Moon
Baiken
Sanji (Sakurian)
Okarun
Ichigo (Kurosaki Ichigo)
The Red Mist
Sanji
Garou Sakurian
Arasaka (Arasaka Suitcase)
EWU RGB
Yuta (Okkotsu Yuta)
Sakuya (Sakuya Izayoi)
Yuki (Itadori Yuji)
Lei Heng
Stop Sign | Regret
×5 Bag of Presents (Bag of Present)
GER (Gold Experience Requiem)
Padoru
Headhunter (Emperor | Headhunter)
Stop Sign | Bisento
""",
    "D": """========**D Tier**========

Hamon | Akaza
TW (The World)
Nikyu (Nikyu Nikyu no mi Fruit)
Dio's Diary
Cyberware
Garou (Water Stream Rock Smashing Fist)
Mochi Awk (Mochi Mochi no mi | Conqueror)
Hie (Hie Hie no mi Fruit)
Shinra (Shinra Kusakabe)
EW (Eternal Wing)
HoF (Herrscher of Flamescion)
Kujo's Hat
Silver Egg
"""
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
        if normalize(key) == q_norm:
            return key, data
        if normalize(data.get("full", "")) == q_norm:
            return key, data

    # 3) partial containment
    for key, data in TIERS.items():
        full_norm = normalize(data.get("full", ""))
        if q_norm in full_norm or full_norm in q_norm:
            return key, data

    return None, None


# ============
# value / calc helpers (ใช้ TIERS เป็นแหล่งข้อมูล)
# ============
def parse_multiplier_and_key(raw_item: str):
    """
    รองรับรูปแบบเช่น:
      - "fingers x5"  or "fingers×5" or "fingers x 5"
    คืนค่า (normalized_key, multiplier, original_key_string)
    """
    item = raw_item.strip()
    m = re.search(r"^(.*?)[\s]*[x×]\s*(\d+)\s*$", item, flags=re.IGNORECASE)
    if m:
        name = m.group(1).strip()
        count = int(m.group(2))
        return normalize(name), count, name
    return normalize(item), 1, item


def calc_value(item_list):
    """
    คืนค่า (total_value:int, unknown_items:list[str], details:list[str])
    details เป็นรายการ "Full name (+value x count = total)" เพื่อแสดงในผลลัพธ์
    """
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

        base_value = data.get("value", 0)
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
    """
    raw_text ควรเป็นข้อความเต็มหลัง mention เช่น:
      "my ew+hie for kujo's hat+silver egg"
    คืน string ที่จะส่งกลับไปยังช่องแชท
    """
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

    # ===== ผล W / L / F ตาม tolerance =====
    if my_value == 0 and other_value == 0:
        result = "F ⚖️"
    else:
        diff = my_value - other_value
        tolerance_value = max(abs(my_value), abs(other_value)) * TOLERANCE
        if abs(diff) <= tolerance_value:
            result = "F ⚖️"
        elif diff > 0:
            result = "W 🥰"
        else:
            result = "L 😡"

    # สร้างข้อความผลลัพ    "egg keeper": {"full": "Egg Keeper", "tier": "B"},
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
    "fingers": {"full": "Sukuna's Cursed Finger", "tier": "C", "amount": 5, "value": 150},
    "rusted sword": {"full": "Rusted Sword", "tier": "C", "value": 345},
    "okarun egg": {"full": "Okarun | Egg of All-devouring Darkness", "tier": "C", "value": 400},
    "getothm": {"full": "Suguru Geto | The Hunt Master", "tier": "C", "value": 365},
    "gojo": {"full": "Gojo Satoru", "tier": "C", "value": 380},
    "hog": {"full": "Hogyoku Fragment", "tier": "C", "value": 70},
    "sukuna": {"full": "Ryomen Sukuna", "tier": "C", "value": 380},
    "geto": {"full": "Suguru Geto", "tier": "C", "value": 320},
    "toji": {"full": "Toji Fushiguro", "tier": "C", "value": 365},
    "candy cane": {"full": "Stop Sign | Candy Cane", "tier": "C", "value": 360},
    "oa's grace": {"full": "OA's Grace", "tier": "C", "value": 340},
    "anubis spook": {"full": "Anubis | Spook", "tier": "C", "value": 400},
    "hamon frost": {"full": "Hamon | Frost", "tier": "C", "value": 370},
    "hohe": {"full": "Herrscher of Human Ego", "tier": "C", "value": 360},
    "c-moon": {"full": "C-Moon", "tier": "C", "value": 340},
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
    "headhunter": {"full": "Emperor | Headhunter", "tier": "C", "value": 53},
    "stop sign bisento": {"full": "Stop Sign | Bisento", "tier": "C", "value": 45},

    # ===== D =====
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
    "bronya": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "bronya zaychik": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "bronya rand": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "silver wolf": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
    "silverwolf": {"full": "Furi's Wife", "tier": "SSR", "value": 999999},
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
# value / calc helpers (ใช้ TIERS เป็นแหล่งข้อมูล)
# ============
def parse_multiplier_and_key(raw_item: str):
    """
    รองรับรูปแบบเช่น:
      - "fingers x5"  or "fingers×5" or "fingers x 5"
      - "5x fingers" (รองรับได้ในอนาคต ถ้าต้องการ ปัจจุบันจะจับแบบหลังไม่บังคับ)
    คืนค่า (normalized_key, multiplier, original_key_string)
    """
    item = raw_item.strip()
    # pattern: name [x|×] number (ท้าย)
    m = re.search(r"^(.*?)[\s]*[x×]\s*(\d+)\s*$", item, flags=re.IGNORECASE)
    if m:
        name = m.group(1).strip()
        count = int(m.group(2))
        return normalize(name), count, name
    # no explicit multiplier
    return normalize(item), 1, item


def calc_value(item_list):
    """
    คืนค่า (total_value:int, unknown_items:list[str], details:list[str])
    details เป็นรายการ "Full name (+value x count = total)" เพื่อแสดงในผลลัพธ์
    """
    total = 0
    unknown = []
    details = []

    for raw in item_list:
        if not raw or not raw.strip():
            continue
        key_norm, mult, original = parse_multiplier_and_key(raw)
        key, data = find_entry_by_query(key_norm)
        if not data:
            # ยังไม่รู้ชื่อนี้
            unknown.append(original)
            continue

        base_value = data.get("value", 0)
        # ถ้าระบุ amount ใน object (เช่น fingers มี amount=5) ให้คูณด้วย amount ถ้ามีความหมาย
        amount_defined = data.get("amount")
        if amount_defined and mult == 1:
            # ถ้าผู้ใช้ไม่ได้บอก multiplier แต่มี field amount: ให้ใช้ amount เป็น multiplier
            mult = amount_defined

        item_total = base_value * mult
        total += item_total

        # details แสดงชัดเจน
        if mult != 1:
            details.append(f"{data['full']} x{mult} (+{base_value} each → +{item_total})")
        else:
            details.append(f"{data['full']} (+{base_value})")

    return total, unknown, details


def wfl_command(raw_text: str):
    """
    raw_text ควรเป็นదేశ్หลัง mention เช่น:
      "my ew+hie for kujo's hat+silver egg"
    คืน string ที่จะส่งกลับไปยังช่องแชท
    """
    text = raw_text.strip()
    low = text.lower()

    if "my " not in low or " for " not in low:
        return "❌ Format: `my item1+item2 for itemA+itemB`"

    # แยกส่วนอย่างปลอดภัย
    try:
        # หาตำแหน่ง "my " และ " for " แบบ case-insensitive
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

    # ===== ผล W / L / F ตาม tolerance =====
    if my_value == 0 and other_value == 0:
        result = "F ⚖️"
    else:
        diff = my_value - other_value
        # ใช้ความต่างสัมบูรณ์เทียบกับค่าสูงสุดเพื่อตัดสิน
        tolerance_value = max(abs(my_value), abs(other_value)) * TOLERANCE
        if abs(diff) <= tolerance_value:
            result = "F ⚖️"
        elif diff > 0:
            # ค่าเราเหนือกว่าเกิน tolerance -> Win
            result = "L 😡"
        else:
            # ค่าต่ำกว่า -> Lose
            result = "W 🥰"

    # สร้างข้อความผลลัพธ์สวย ๆ
    out_lines = []
    out_lines.append(f"**Your value:** {my_value}")
    for d in my_details:
        out_lines.append(f"• {d}")
    out_lines.append("")  # blank line
    out_lines.append(f"**Other value:** {other_value}")
    for d in other_details:
        out_lines.append(f"• {d}")
    out_lines.append("")  # blank line
    out_lines.append(f"**Result:** {result}")

    return "\n".join(out_lines)


# ============
# tierlist2 helper
# ============
def build_tier_messages():
    """
    สร้างข้อความแยกตาม Tier ตามลำดับที่ต้องการ แล้วคืน list ของข้อความ
    ไม่ทำให้ TIERS หาย หรือแก้ข้อมูลต้นฉบับ
    """
    # ลำดับที่ต้องการแสดง
    preferred_order = ["U", "EX", "S", "A", "B", "C", "D", "SSR"]

    # เก็บ unique full names ต่อ tier (รักษาความเรียงตาม TIERS dict)
    groups = {}
    for key, data in TIERS.items():
        tier = data.get("tier", "UNKNOWN")
        full = data.get("full", key)
        amount = data.get("amount")
        display = f"{full}" + (f" x{amount}" if amount else "")
        groups.setdefault(tier, [])
        if display not in groups[tier]:
            groups[tier].append(display)

    # สร้างข้อความตาม preferred order แล้วตามด้วย tier อื่นๆ ถ้ามี
    messages = []
    used = set()
    for t in preferred_order:
        items = groups.get(t, [])
        if not items:
            continue
        used.add(t)
        header = f"========**{t} Tier**========\n\n"
        body = "\n".join(items)
        messages.append(header + body)

    # any remaining tiers
    for t, items in groups.items():
        if t in used:
            continue
        header = f"========**{t} Tier**========\n\n"
        body = "\n".join(items)
        messages.append(header + body)

    return messages


async def send_long_message(channel, text):
    """
    ส่งข้อความโดยแยกเป็นชิ้นถ้ายาวเกิน 1900 ตัวอักษร (ปลอดภัยสำหรับ Discord)
    แยกโดยบรรทัดเพื่อความอ่านง่าย
    """
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
# events
# ============
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="@Furi find <name>  |  @Furi tl  |  @Furi my <items> for <items>"
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
        await message.channel.send("❗ Usage: `@Bot find <name>` or `@Bot tl` (tierlist) or `@Bot my <items> for <items>`")
        return

    # normalize leading spaces and collapse multiple spaces
    raw = re.sub(r"\s+", " ", raw).strip()

    # ===== WFL command (ต้องเริ่มด้วย my ) =====
    if raw.lower().startswith("my "):
        reply = wfl_command(raw)
        await message.channel.send(reply)
        return

    # If user asked for tierlist (backwards compatible)
    if raw.lower() in ["tierlist", "tl"]:
        # send tierlist image (must exist in project root)
        try:
            await message.channel.send(file=discord.File("tierlist.png"))
        except Exception:
