import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_telegram():
    """Test if Telegram bot is properly configured"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("❌ Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env file")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': '✅ Test message from Stock News Bot!\n\nIf you see this, your bot is configured correctly!',
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        
        print("✅ Test message sent successfully!")
        print("📱 Check your Telegram to confirm you received it.")
        return True
        
    except Exception as e:
        print(f"❌ Error sending test message: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your bot token is correct")
        print("2. Make sure you've started a chat with your bot on Telegram")
        print("3. Make sure your chat ID is correct")
        return False

def test_finnhub():
    """Test if Finnhub API is properly configured"""
    api_key = os.getenv('FINNHUB_API_KEY')
    
    if not api_key:
        print("❌ Missing FINNHUB_API_KEY in .env file")
        return False
    
    try:
        url = "https://finnhub.io/api/v1/news"
        params = {
            'category': 'technology',
            'token': api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            print(f"✅ Finnhub API working! Retrieved {len(data)} articles.")
            print(f"   Sample headline: {data[0].get('headline', 'N/A')[:60]}...")
            return True
        else:
            print("⚠️  Finnhub API connected but no articles returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Finnhub API: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your API key is correct")
        print("2. Check if you've exceeded rate limits")
        return False

if __name__ == "__main__":
    print("🧪 Testing Stock News Bot Configuration...\n")
    
    print("=" * 50)
    print("Testing Finnhub API...")
    print("=" * 50)
    finnhub_ok = test_finnhub()
    
    print("\n" + "=" * 50)
    print("Testing Telegram Bot...")
    print("=" * 50)
    telegram_ok = test_telegram()
    
    print("\n" + "=" * 50)
    if finnhub_ok and telegram_ok:
        print("✅ ALL TESTS PASSED!")
        print("🚀 You're ready to run: python stock_news_bot.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("📝 Please fix the issues above before running the bot")
    print("=" * 50)
