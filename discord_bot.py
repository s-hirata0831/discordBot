import discord
import json
from discord.ext import commands, tasks
import asyncio
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ボットのトークンを入力
TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.members = True  # メンバー情報を取得するために必要
bot = commands.Bot(command_prefix='!', intents=intents)

# data.jsonの読み込み関数
def load_data():
    with open('data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def change_nicknames_periodically():
    """10秒ごとにニックネームを変更するタスク"""
    await bot.wait_until_ready()  # Botが完全に起動するのを待つ
    while not bot.is_closed():  # Botが動作中である限りループする
        guilds = bot.guilds  # Botが参加しているすべてのサーバー
        for guild in guilds:
            data = load_data()
            for entry in data:
                discord_id = entry["DiscordIDを入力\n(例：hiraterm)"]
                new_nickname = entry["名前を入力\n(例：舞鶴太郎)"]

                # メンバーを探す
                member = discord.utils.get(guild.members, name=discord_id)
                if member:
                    try:
                        # ニックネームを変更
                        await member.edit(nick=new_nickname)
                        print(f"{member.name} のニックネームを {new_nickname} に変更しました。")
                    except discord.Forbidden:
                        print(f"{member.name} のニックネームを変更できませんでした（権限不足）。")
                else:
                    print(f"DiscordID: {discord_id} のメンバーが見つかりませんでした。")
        await asyncio.sleep(10)  # 10秒待機

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    bot.loop.create_task(change_nicknames_periodically())  # タスクを起動

# ボットの起動
bot.run(TOKEN)
