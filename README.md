# Stock News Telegram Bot

A free, real-time stock news monitoring bot that sends you Telegram messages about news for your watchlist.

## Features
- ✅ Monitors specific stocks: MSFT, ORCL, META, AMZN, ALAB, NBIS, LAES, BBAI
- ✅ Tracks AI, semiconductors, space, robotics, and tech infrastructure news
- ✅ Checks every 5 minutes for new articles
- ✅ Sends instant Telegram notifications
- ✅ Avoids duplicate messages
- ✅ 100% free to run

## Setup Instructions

### Step 1: Get Your API Keys

#### A. Finnhub API Key (News Source)
1. Go to https://finnhub.io
2. Click "Get free API key"
3. Sign up with your email
4. Copy your API key from the dashboard

#### B. Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow prompts to name your bot
4. Copy the bot token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### C. Your Telegram Chat ID
1. Search for `@userinfobot` on Telegram
2. Start a chat and send `/start`
3. Copy your ID (a number like `123456789`)

### Step 2: Local Testing (Optional)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your keys
cp .env.example .env
# Edit .env and add your actual API keys

# Run the bot locally
python stock_news_bot.py
```

### Step 3: Deploy to Render.com (Free 24/7 Hosting)

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub (recommended)

2. **Push Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/stock-news-bot.git
   git push -u origin main
   ```

3. **Create Web Service on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name**: stock-news-bot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python stock_news_bot.py`
     - **Instance Type**: Free

4. **Add Environment Variables**
   - In Render dashboard, go to "Environment"
   - Add three variables:
     - `FINNHUB_API_KEY` = your_finnhub_key
     - `TELEGRAM_BOT_TOKEN` = your_bot_token
     - `TELEGRAM_CHAT_ID` = your_chat_id

5. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your bot is now running 24/7!

## How It Works

1. **Every 5 minutes**, the bot:
   - Checks Finnhub for news on your 8 stocks
   - Checks general tech news for AI/semiconductor/space/robotics keywords
   
2. **When new relevant news is found**:
   - Formats it nicely with headline, summary, source, and link
   - Sends it to your Telegram
   - Marks it as "sent" to avoid duplicates

3. **Smart filtering**:
   - Stock-specific news is always sent
   - General news only sent if it matches your keywords

## Customization

### Change Check Frequency
In `stock_news_bot.py`, modify the last line:
```python
bot.run(interval_minutes=5)  # Change 5 to any number
```

### Add/Remove Stocks
In `stock_news_bot.py`, update the list:
```python
self.stocks = ['MSFT', 'ORCL', 'META', 'AMZN', 'ALAB', 'NBIS', 'LAES', 'BBAI']
```

### Modify Keywords
In `stock_news_bot.py`, edit:
```python
self.keywords = [
    'artificial intelligence', 'AI', # Add your own keywords here
]
```

## Troubleshooting

**No messages received?**
- Check bot logs on Render dashboard
- Verify API keys are correct
- Make sure you started your bot on Telegram (send `/start` to it)

**Too many/few messages?**
- Adjust keywords to be more/less specific
- Change check interval (lower = more frequent)

**Bot stopped working?**
- Free tier on Render sleeps after 15 min of inactivity
- Add a health check endpoint or upgrade to paid tier ($7/mo for always-on)

## Costs

- Finnhub: FREE (60 API calls/min)
- Telegram: FREE (unlimited messages)
- Render.com: FREE (with sleep after inactivity) or $7/month for 24/7

## License

MIT - Use freely!
