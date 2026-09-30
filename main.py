import os
import discord
from discord.ext import commands
import google.generativeai as genai

# 1. ตั้งค่า Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_INSTRUCTION = """
คุณคือระบบสร้างสคริปต์ Roblox Lua อัตโนมัติสำหรับ Delta Executor
ข้อกำหนดในการตอบกลับ:
1. ต้องตอบกลับเป็นโค้ด Lua บรรทัดเดียว (One-liner) เท่านั้น
2. โค้ดต้องเริ่มต้นด้วย 'local'
3. ต้องใช้ Rayfield UI ในการสร้างเมนู (ใช้ชื่อเมนู "Santi's Hub")
4. ห้ามใส่คำอธิบาย ห้ามใส่ข้อความทักทาย ห้ามใส่ Markdown Code Block ให้ส่งเฉพาะตัวโค้ดเพียวๆ
"""

# 2. ตั้งค่า Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'ระบบหลังบ้าน Santi\'s Hub ({bot.user}) พร้อมทำงานแล้วสัด!')

@bot.command(name="gen")
async def generate_script(ctx, *, prompt: str):
    async with ctx.typing():
        try:
            full_prompt = f"{SYSTEM_INSTRUCTION}\nคำสั่งจากผู้ใช้: {prompt}"
            response = model.generate_content(full_prompt)
            script_code = response.text.strip()

            embed = discord.Embed(
                title="⚡ Santi's Hub - AI Generated Script",
                description=f"**คำสั่ง:** {prompt}\nคัดลอกโค้ดด้านล่างไปวางใน Delta ได้เลยสัด!",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            await ctx.send(f"```{script_code}```")
        except Exception as e:
            await ctx.send(f"เกิดข้อผิดพลาดในการสร้างสคริปต์สัด: {e}")

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(BOT_TOKEN)
