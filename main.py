import discord
from discord.ext import commands

TARGET_GUILD_ID = 1473379988190400595  # เซิร์ฟ B (ที่มี role อยู่)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def give(ctx, member: discord.Member, role_id: int):

    target_guild = bot.get_guild(TARGET_GUILD_ID)
    if not target_guild:
        await ctx.send("ไม่พบเซิร์ฟปลายทาง")
        return

    target_member = target_guild.get_member(member.id)
    if not target_member:
        await ctx.send("ผู้ใช้นี้ไม่ได้อยู่ในเซิร์ฟปลายทาง")
        return

    role = target_guild.get_role(role_id)
    if not role:
        await ctx.send("ไม่พบ role นี้ในเซิร์ฟปลายทาง")
        return

    try:
        await target_member.add_roles(role)
        await ctx.send(f"ให้ role เรียบร้อยแล้วในเซิร์ฟ B")
    except discord.Forbidden:
        await ctx.send("บอทไม่มีสิทธิ์ให้ role นี้")
    except Exception as e:
        await ctx.send("เกิดข้อผิดพลาด")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


bot.run(TOKEN)
