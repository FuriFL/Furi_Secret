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
    "asgore": {"full": "Acerola | King of Monsters", "tier": "U", "value": 200000},

    # ===== EX =====
    "solemn": {"full": "Cross | Butterflies' Funeral", "tier": "EX", "value": 20000},

    # ===== S =====
    "cross": {"full": "Cross", "tier": "S", "value": 10000},
    "uf": {"full": "Undying Flame", "tier": "S", "value": 7300},
    "vst": {"full": "Valentine Summer Time", "tier": "S", "value": 7000},
    "ewu rgb": {"full": "Eternal Wing | RGB | UNLEASHED", "tier": "S", "value": 6520},
    "mkvol": {"full": "Midknight Vessel of Life", "tier": "S", "value": 4500},
    "mkvolts": {"full": "Midknight Vessel of Life | Taped Shut", "tier": "S", "value": 4000},
    "mimivol": {"full": "Midknight Vessel of Life | Mimicry", "tier": "S", "value": 3500},

    # ===== A =====
    "wh": {"full": "Wild Hunt", "tier": "A", "value": 3500},
    "soc": {"full": "Soul of Cinder", "tier": "A", "value": 3250},
    "nerd": {"full": "Standless | Nerd", "tier": "A", "value": 1700},
    "coco": {"full": "Rainy Time | Coco", "tier": "A", "value": 1700},
    "tuna": {"full": "Anubis Requiem | Tuna", "tier": "A", "value": 2000},
    "ewu": {"full": "Eternal Wing | Unleashed", "tier": "A", "value": 1630},
    "5th sinner": {"full": "Lei Heng | The 5th Sinner", "tier": "A", "value": 1570},
    "fx!chara": {"full": "X!Chara : Frostbite", "tier": "A", "value": 1300},
    "duf": {"full": "Dullahan | Unyielding Frost", "tier": "A", "value": 1135},
    "se": {"full": "Singularity Essence", "tier": "A", "value": 1300},
    "mkb": {"full": "Midknight", "tier": "A", "value": 1135},
    "hx!chara": {"full": "X!Chara | Hallowed", "tier": "A", "value": 1000},
    "dull": {"full": "Remembrance of Dullahan", "tier": "A", "value": 945},
    "x!chara": {"full": "X!Chara", "tier": "A", "value": 920},
    "agnes": {"full": "Okarun | Agnes Tachyon", "tier": "A", "value": 870},
    "rukia ws": {"full": "Rukia Kuchiki : Winter Season", "tier": "A", "value": 870},
    "rukia": {"full": "Rukia Kuchiki", "tier": "A", "value": 835},
    "goldship requiem": {"full": "Gold Ship Experience Requiem", "tier": "A", "value": 845},
    "goldship experience": {"full": "Goldship Experience", "tier": "A", "value": 835},
    "spin ce": {"full": "Spin | Singularity Essence", "tier": "A", "value": 960},
    "aizen evo": {"full": "Aizen Sosuke (Hogyoku Fusion)", "tier": "A", "value": 835},
    "aizen": {"full": "Aizen Sosuke", "tier": "A", "value": 650},
    "ronin ce": {"full": "Ronin | Crimson Eclipse", "tier": "A", "value": 835},
    "ronin awk": {"full": "Ronin (Successor of Niten Ichiryu)", "tier": "A", "value": 850},
    "pk": {"full": "Pilgrim Knight", "tier": "A", "value": 780},
    "starrk": {"full": "Coyote Starrk", "tier": "A", "value": 740},
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
    "ar": {"full": "Anubis Requiem", "tier": "B", "value": 800},
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
    raw_text ควรเป็นข้อความเต็มหลัง mention เช่น:
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
        diff = abs(my_value - other_value)
        tolerance_value = max(my_value, other_value) * TOLERANCE
        if diff <= tolerance_value:
            result = "F ⚖️"
        elif my_value > other_value:
            result = "L 😡"
        else:
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

# --- เพิ่ม helper สำหรับสร้าง list ของทุกเทียร์/ตัวละคร ---
def build_full_tier_messages():
    """
    คืนค่า list ของข้อความ (แต่ละรายการเป็นข้อความสำหรับส่ง)
    แบ่งตาม Tier (preferred order). ข้อความแต่ละชิ้นจะไม่เกิน 1900 ถ้าเป็นไปได้
    """
    preferred_order = ["U", "EX", "S", "A", "B", "C", "D", "SSR", "UNKNOWN"]
    groups = {}
    for key, data in TIERS.items():
        tier = data.get("tier", "UNKNOWN")
        full = data.get("full", key)
        amount = data.get("amount")
        value = data.get("value", "N/A")
        # รูปแบบที่จะแสดง: Full — Tier: X — Value: Y (xN ถ้ามี amount) (key: shorthand)
        extra_amount = f" x{amount}" if amount else ""
        display = f"{full} — Tier: {tier} — Value: {value}{extra_amount}  (key: {key})"
        groups.setdefault(tier, []).append(display)

    messages = []
    # สร้างข้อความตาม preferred order
    for t in preferred_order:
        items = groups.get(t, [])
        if not items:
            continue
        header = f"======== {t} Tier ========\n"
        body = "\n".join(items)
        messages.append(header + body)

    # ถ้ามี tier อื่น ๆ ที่ไม่ได้อยู่ใน preferred_order
    for t, items in groups.items():
        if t in preferred_order:
            continue
        header = f"======== {t} Tier ========\n"
        body = "\n".join(items)
        messages.append(header + body)

    return messages


# --- helper สำหรับส่งข้อความยาวเป็นชิ้น ๆ ---
async def send_long_message(channel, text):
    """
    ส่งข้อความโดยแยกเป็นชิ้น ถ้ายาวเกิน 1900 ตัวอักษร (ปลอดภัยกับ Discord)
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
            name="@FuriBOT find <name>  |  @FuriBOT tl  |  @FuriBOT my <items> for <items>"
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
        await message.channel.send("❗ Usage: `@FuriBOT find <name>` or `@FuriBOT tl` (tierlist) or `@FuriBOT my <items> for <items>`")
        return

    # ===== HELP COMMAND =====
    if raw.lower() in ["help", "commands", "cmd", "h"]:
        await message.channel.send(
            "🌸 **HELP | FuriBOT** 🌸\n\n"
            "════════════════════\n"
            "📜 **ALL COMMANDS**\n"
            "════════════════════\n\n"
            "💮 **@FuriBOT tierlist**\n"
            "→ Show tierlist image\n\n"
            "💮 **@FuriBOT tierlist all**\n"
            "→ Show all specs with Tier & Value\n\n"
            "💮 **@FuriBOT find <name>**\n"
            "→ Find spec Tier & Value\n"
            "Example: `@FuriBOT find vergil`\n\n"
            "💮 **@FuriBOT my <items> for <items>**\n"
            "→ Check W / F / L by value\n"
            "Example: `@FuriBOT my ew+hie for kujo's hat+silver egg`\n\n"
            "════════════════════\n"
            "⚠️ **Note**\n"
            "════════════════════\n"
            "Value points of specs are **NOT official**.\n"
            "Please don’t fully trust them • this list is still under development and balancing"
        )
        return
        
    # normalize leading spaces and collapse multiple spaces
    raw = re.sub(r"\s+", " ", raw).strip()

    # ===== WFL command (ต้องเริ่มด้วย my ) =====
    if raw.lower().startswith("my "):
        reply = wfl_command(raw)
        await message.channel.send(reply)
        return

    # ถ้า user พิมพ์ขอ list ทุกตัวพร้อม value
    if raw.lower() in ["tierlist all", "tl all", "tierlist all", "list all", "list all tiers"]:
        messages = build_full_tier_messages()
        for m in messages:
            await send_long_message(message.channel, m)
        return

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
        await message.channel.send("😡 Please use `@FuriBOT find <name>` to search for a spec/stand, `@FuriBOT tl` for the tierlist image, or `@FuriBOT my <items> for <items>` for W/F/L.")
        return

    if len(parts) < 2 or not parts[1].strip():
        await message.channel.send("😡 Please provide a name after `find`. Example: `@FuriBOT find ewu`")
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
        # include amount if present
        amount_text = f" x{data['amount']}" if data.get("amount") else ""
        await message.channel.send(f"**{display_name}** **[{data['full']}]** is on **{data['tier']}** Tier! | Value: **{data['value']}**")
    else:
        await message.channel.send(f"💔 Sorry, I don't know **{query_raw}**")
        


# ============
# run
# ============
client.run(os.getenv("TOKEN"))
