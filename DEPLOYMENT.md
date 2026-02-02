# Quick Deployment Guide for Render.com

## Why Render.com?
- ✅ Free tier available
- ✅ Easy deployment from GitHub
- ✅ Automatic restarts if bot crashes
- ✅ Simple environment variable management
- ⚠️ Free tier: bot sleeps after 15 min inactivity (we'll fix this)

## Step-by-Step Deployment

### 1. Prepare Your Code

```bash
# Clone or create the project
cd stock-news-bot

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"
```

### 2. Push to GitHub

```bash
# Create a new repository on GitHub.com
# Then run:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/stock-news-bot.git
git push -u origin main
```

### 3. Deploy on Render

1. Go to https://render.com and sign up (use GitHub login)

2. Click **"New +"** → **"Web Service"**

3. **Connect Repository**
   - Click "Connect account" to link GitHub
   - Select your `stock-news-bot` repository
   - Click "Connect"

4. **Configure Service**
   - **Name**: `stock-news-bot` (or any name you want)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python stock_news_bot.py`
   - **Instance Type**: `Free`

5. **Add Environment Variables**
   - Scroll to "Environment Variables" section
   - Click "Add Environment Variable" for each:
   
   ```
   Key: FINNHUB_API_KEY
   Value: [paste your Finnhub API key]
   
   Key: TELEGRAM_BOT_TOKEN
   Value: [paste your Telegram bot token]
   
   Key: TELEGRAM_CHAT_ID
   Value: [paste your Telegram chat ID]
   ```

6. **Deploy**
   - Click **"Create Web Service"**
   - Wait 2-3 minutes while Render builds and deploys
   - Watch the logs to see your bot start!

### 4. Verify It's Working

Within a few minutes, you should receive a Telegram message:
```
🤖 Stock News Bot Started!

📊 Monitoring: MSFT, ORCL, META, AMZN, ALAB, NBIS, LAES, BBAI
🔍 Keywords: AI, semiconductors, space, robotics, tech
⏱ Check interval: 5 minutes
```

## Keeping It Running 24/7 (Important!)

**Problem**: Render's free tier puts your service to sleep after 15 minutes of no HTTP requests.

**Solutions**:

### Option A: Upgrade to Paid ($7/month)
- Most reliable
- Always running
- No sleep issues
- Go to service settings → "Instance Type" → Select "Starter ($7/mo)"

### Option B: External Ping Service (Free)
Use a service to ping your bot every 10 minutes:

1. Add this to your `stock_news_bot.py` (after imports):
```python
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))
```

2. Update requirements.txt:
```
requests==2.31.0
python-dotenv==1.0.0
flask==3.0.0
```

3. Modify the `if __name__ == "__main__":` section:
```python
if __name__ == "__main__":
    # Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run bot
    bot = StockNewsBot()
    bot.run(interval_minutes=5)
```

4. Use a free service like UptimeRobot.com:
   - Sign up at https://uptimerobot.com
   - Add new monitor
   - Type: HTTP(s)
   - URL: Your Render app URL (e.g., https://stock-news-bot.onrender.com)
   - Interval: 5 minutes

### Option C: Use Different Free Host
- **Railway.app**: 500 hours/month free, no sleep
- **Fly.io**: Better free tier, more complex setup

## Monitoring Your Bot

### View Logs
- In Render dashboard, go to your service
- Click "Logs" tab
- See real-time output from your bot

### Manual Deploy
If you update your code:
```bash
git add .
git commit -m "Update configuration"
git push
```
Render will automatically redeploy!

### Restart Service
- In Render dashboard → "Manual Deploy" → "Clear build cache & deploy"

## Troubleshooting

**Bot not sending messages?**
1. Check logs for errors
2. Verify environment variables are set correctly
3. Make sure you've started your Telegram bot (send `/start` to it)

**Bot stopped after deployment?**
- Check if it went to sleep (free tier limitation)
- Implement Option B above

**API rate limits hit?**
- Finnhub free tier: 60 calls/min
- With 8 stocks + general news = ~9 calls per cycle
- Running every 5 min = well within limits ✅

**Want to test locally first?**
```bash
pip install -r requirements.txt
python test_config.py  # Test your API keys
python stock_news_bot.py  # Run locally
```

## Next Steps

1. ✅ Deploy to Render
2. ✅ Verify you receive startup message
3. ✅ Wait for first news (could be minutes or hours depending on news)
4. ✅ Set up UptimeRobot to prevent sleep (if using free tier)
5. ✅ Monitor logs for a day to ensure stability

## Support

If you have issues:
1. Check Render logs
2. Run `test_config.py` locally
3. Verify all API keys are correct
4. Check Finnhub and Telegram API status

Happy monitoring! 🚀📈
