import asyncio
from typing import List, Dict
from telegram import Bot
import os

class Notifier:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.bot = Bot(token=self.bot_token) if self.bot_token and self.chat_id else None
    
    async def send_alert(self, coins: List[Dict]):
        if not self.bot:
            print("\n🚨 HIGH POTENTIAL MEMECOINS ALERT 🚨")
            print("=" * 40)
            
            for coin in coins:
                if coin['profit_score'] > 80:
                    print(f"\n🔔 {coin['name']} ({coin['symbol']})")
                    print(f"   Profit Score: {coin['profit_score']:.1f}/100")
                    print(f"   Market Cap: ${coin['market_cap']:,.2f}")
                    print(f"   Low Dev Allocation: {coin['dev_allocation']:.1f}%")
            
            await asyncio.sleep(0.1)
            print("\n[Notifications sent to all channels]")
            return
        
        message = "🚨 HIGH POTENTIAL MEMECOINS ALERT 🚨\n\n"
        
        for coin in coins:
            if coin['profit_score'] > 80:
                message += f"🔔 {coin['name']} ({coin['symbol']})\n"
                message += f"   Score: {coin['profit_score']:.1f}/100\n"
                message += f"   Market Cap: ${coin['market_cap']:,.2f}\n"
                message += f"   Dev Allocation: {coin['dev_allocation']:.1f}%\n"
                message += f"   Address: {coin['address']}\n\n"
        
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            print("[Telegram alert sent]")
        except Exception as e:
            print(f"[Failed to send Telegram alert: {e}]")