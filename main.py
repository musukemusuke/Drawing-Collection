import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

class DrawingBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Cogsの読み込み
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.sync()
        asyncio.create_task(self.shutdown_timer())
        print("Bot setup completed, waiting for ready event...")

    async def shutdown_timer(self):
        # GitHub Actionsの制限(6時間)に余裕を持って、2時間45分(9900秒)で終了させる
        # これによりワークフローが「タイムアウト失敗」にならず正常終了します
        await asyncio.sleep(9900)
        print("Shutdown timer reached. Closing bot...")
        await self.close()

bot = DrawingBot()

# on_readyイベント内でサーバー情報を出力（ギルド情報が完全に取得された後に実行される）
@bot.event
async def on_ready():
    print(f"✅ ログイン成功: {bot.user} ({bot.user.id})")
    print(f"📊 参加サーバー数: {len(bot.guilds)} サーバー")
    
    # 参加している全サーバーの名前とID、メンバー一覧を表示（GitHub Actionsログで確認可能）
    print("\n=== 参加サーバー一覧 ===")
    for i, guild in enumerate(bot.guilds, 1):
        print(f"{i}. {guild.name} (ID: {guild.id}) - メンバー数: {guild.member_count}")
        # ボット以外の人間メンバーとbotメンバーを分けて一覧表示
        human_members = [member.name for member in guild.members if not member.bot]
        bot_members = [member.name for member in guild.members if member.bot]
        
        if human_members:
            print(f"   人間メンバー: {', '.join(human_members)}")
        else:
            print("   人間メンバー: いません")
            
        if bot_members:
            print(f"   Botメンバー: {', '.join(bot_members)}")
        else:
            print("   Botメンバー: いません")
    print("======================\n")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable is not set.")
        print("Please ensure you have added it to GitHub Secrets or your .env file.")
        exit(1)
    
    bot.run(token)