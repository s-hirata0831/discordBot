import discord
import json
from discord.ext import commands
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

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command()
async def change_nicknames(ctx):
    """data.jsonを参照してサーバーのニックネームを変更する"""
    guild = ctx.guild  # コマンドが実行されたサーバー
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
                await ctx.send(f"{member.name} のニックネームを {new_nickname} に変更しました。")
            except discord.Forbidden:
                await ctx.send(f"{member.name} のニックネームを変更できませんでした（権限不足）。")
        else:
            await ctx.send(f"DiscordID: {discord_id} のメンバーが見つかりませんでした。")

# ボットの起動
bot.run(TOKEN)
