# Quick Start Checklist ✅

Follow these steps in order to get your bot running in under 30 minutes!

## Part 1: Get Your API Credentials (15 minutes)

### ☐ Get Finnhub API Key
1. Go to https://finnhub.io
2. Click "Get free API key" 
3. Sign up with email
4. Copy API key from dashboard
5. **Save it somewhere safe!**

### ☐ Create Telegram Bot
1. Open Telegram app
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name: "My Stock News Bot"
5. Choose username: "mystocknews_bot" (must end in 'bot')
6. Copy the bot token (long string with numbers and letters)
7. **Save it somewhere safe!**

### ☐ Get Your Telegram Chat ID
1. In Telegram, search for `@userinfobot`
2. Send `/start`
3. Copy your ID (just the numbers)
4. **Save it somewhere safe!**

### ☐ Start Your Bot
1. Find your bot in Telegram (search for the username you created)
2. Send `/start` to it
3. This is important - your bot can only send you messages after you start it!

## Part 2: Deploy to Render.com (10 minutes)

### ☐ Create GitHub Account (if needed)
- Go to https://github.com
- Sign up for free

### ☐ Upload Code to GitHub
1. Download this project folder
2. Go to https://github.com/new
3. Name it: `stock-news-bot`
4. Click "uploading an existing file"
5. Drag all files from this folder
6. Click "Commit changes"

### ☐ Deploy on Render
1. Go to https://render.com
2. Sign up with your GitHub account
3. Click "New +" → "Web Service"
4. Select your `stock-news-bot` repository
5. Fill in:
   - Name: `stock-news-bot`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python stock_news_bot.py`
   - Instance Type: Free
6. Add environment variables:
   - `FINNHUB_API_KEY` = [your Finnhub key]
   - `TELEGRAM_BOT_TOKEN` = [your bot token]
   - `TELEGRAM_CHAT_ID` = [your chat ID]
7. Click "Create Web Service"
8. Wait 2-3 minutes

### ☐ Verify It Works
- Check your Telegram - you should get a startup message!
- Check Render logs to see the bot running

## Part 3: Keep It Running (5 minutes)

### ☐ Set Up Keep-Alive Ping
1. Go to https://uptimerobot.com
2. Sign up for free
3. Click "Add New Monitor"
4. Select "HTTP(s)"
5. Friendly Name: "Stock News Bot"
6. URL: Copy from Render (looks like https://stock-news-bot.onrender.com)
7. Monitoring Interval: 5 minutes
8. Click "Create Monitor"

**Done! Your bot is now running 24/7!** 🎉

## What to Expect

### First Hour
- You should receive the startup message immediately
- News may take a while depending on market activity
- Check Render logs to see the bot checking for news every 5 minutes

### First Day
- You'll start receiving relevant news articles
- If it's a quiet news day, you might only get a few
- If it's busy (earnings, major announcements), you could get 10-20+

### Ongoing
- The bot runs forever, checking every 5 minutes
- It will never send the same article twice
- It only sends when there's NEW relevant news

## Troubleshooting

**❌ No startup message?**
- Check Render logs for errors
- Verify environment variables are correct
- Make sure you sent `/start` to your bot on Telegram

**❌ No news after several hours?**
- This is normal if markets are closed or it's a slow news day
- Check logs to confirm bot is running
- The bot is working - just waiting for relevant news!

**❌ Bot stopped working?**
- Free tier may sleep after 15 min
- UptimeRobot should wake it up
- Check Render logs

**❌ Too many messages?**
- Edit `stock_news_bot.py` 
- Make keywords more specific
- Increase check interval from 5 to 15 minutes

## Quick Reference

**Your API Keys:**
- Finnhub: ___________________________
- Telegram Bot: ___________________________
- Telegram Chat: ___________________________

**Important URLs:**
- Render Dashboard: https://dashboard.render.com
- Finnhub Dashboard: https://finnhub.io/dashboard
- UptimeRobot: https://uptimerobot.com/dashboard

**Files to Customize:**
- `stock_news_bot.py` - main code (stocks, keywords, interval)
- Render environment variables - API keys

## Next Steps

1. ✅ Complete all checkboxes above
2. Wait for first news (be patient!)
3. Customize stocks/keywords if needed
4. Enjoy real-time stock news! 📈

---

**Need help?** Check the detailed guides:
- `README.md` - Full documentation
- `DEPLOYMENT.md` - Detailed deployment steps
