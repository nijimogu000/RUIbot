import discord
from discord.ext import commands
import time
import random
import os

# ===== 設定 =====
COOLDOWN_SECONDS = 10
# =================

last_response_time = 0
last_response_text = None

responses = {
    "ヒモ": [
        "……はぁ。めんどくせー…",
        "……お前らは大変そうだな(笑)",
        "勝手にお前らがそう呼んでるだけだろ",
        "養ってるつもりはねぇよ",
        "金ないのに飼うとか……正気か？",
        "俺は違ぇ"
    ],
    "静流": [
        "静流のやつ、また酒で潰れやがって…",
        "放っといたら死ぬだろ",
        "アイツの名前は出すな",
        "……",
        "……話変えろ",
        "誰のカードで買ってると思ってんだ",
        "週1でバイトしただけでドヤ顔してくるからな"
        "別に世話してるつもりはねぇよ",
        "寝て起きたら金が減ってた……",
        "財布でも迎車でもねぇっつってんのに……結局やるの俺なんだよな"
    ]
}

both_responses = [
    "俺の金をバカスカ使いやがって",
    "ヒモ飼い扱いすんな",
    "名前出すな",
    "……話題変えろ"
]

def choose_response(candidates):
    global last_response_text
    filtered = [r for r in candidates if r != last_response_text]
    if not filtered:
        filtered = candidates
    choice = random.choice(filtered)
    last_response_text = choice
    return choice

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    global last_response_time

    if message.author.bot:
        return

    now = time.time()
    if now - last_response_time < COOLDOWN_SECONDS:
        return

    content = message.content

    response = None
    if "静流" in content and "ヒモ" in content:
        response = choose_response(both_responses)
    elif "静流" in content:
        response = choose_response(responses["静流"])
    elif "ヒモ" in content:
        response = choose_response(responses["ヒモ"])

    if response:
        last_response_time = now
        await message.channel.send(response)

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))

