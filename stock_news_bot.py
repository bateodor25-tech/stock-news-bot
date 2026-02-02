import os
import time
import requests
import json
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockNewsBot:
    def __init__(self):
        # API Keys from environment variables
        self.finnhub_api_key = os.getenv('FINNHUB_API_KEY')
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Your watchlist
        self.stocks = ['MSFT', 'ORCL', 'META', 'AMZN', 'ALAB', 'NBIS', 'LAES', 'BBAI']
        
        # Keywords for industry monitoring
        self.keywords = [
            'artificial intelligence', 'AI', 'machine learning', 'deep learning',
            'neural network', 'LLM', 'generative AI', 'ChatGPT', 'OpenAI',
            'semiconductor', 'chip', 'GPU', 'NVIDIA', 'processor', 'AI accelerator',
            'data center', 'cloud computing', 'AI infrastructure', 'TPU',
            'space', 'satellite', 'rocket', 'SpaceX', 'aerospace',
            'robotics', 'autonomous', 'automation', 'robot'
        ]
        
        # Track sent articles to avoid duplicates
        self.sent_articles = set()
        self.load_sent_articles()
        
    def load_sent_articles(self):
        """Load previously sent articles from file"""
        try:
            if os.path.exists('sent_articles.json'):
                with open('sent_articles.json', 'r') as f:
                    data = json.load(f)
                    self.sent_articles = set(data)
                logger.info(f"Loaded {len(self.sent_articles)} previously sent articles")
        except Exception as e:
            logger.error(f"Error loading sent articles: {e}")
    
    def save_sent_articles(self):
        """Save sent articles to file"""
        try:
            # Keep only last 1000 articles to prevent file from growing too large
            articles_list = list(self.sent_articles)[-1000:]
            with open('sent_articles.json', 'w') as f:
                json.dump(articles_list, f)
        except Exception as e:
            logger.error(f"Error saving sent articles: {e}")
    
    def fetch_stock_news(self, symbol):
        """Fetch news for a specific stock from Finnhub"""
        try:
            url = f"https://finnhub.io/api/v1/company-news"
            # Get news from last 24 hours
            to_date = datetime.now().strftime('%Y-%m-%d')
            from_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            params = {
                'symbol': symbol,
                'from': from_date,
                'to': to_date,
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []
    
    def fetch_general_news(self):
        """Fetch general market news from Finnhub"""
        try:
            url = f"https://finnhub.io/api/v1/news"
            params = {
                'category': 'technology',
                'token': self.finnhub_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching general news: {e}")
            return []
    
    def is_relevant(self, article):
        """Check if article is relevant based on keywords"""
        text = (article.get('headline', '') + ' ' + article.get('summary', '')).lower()
        return any(keyword.lower() in text for keyword in self.keywords)
    
    def send_telegram_message(self, message):
        """Send message via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': False
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def format_message(self, article, stock=None):
        """Format article as Telegram message"""
        headline = article.get('headline', 'No headline')
        summary = article.get('summary', '')
        url = article.get('url', '')
        source = article.get('source', 'Unknown')
        datetime_unix = article.get('datetime', 0)
        
        # Convert Unix timestamp to readable date
        date_str = datetime.fromtimestamp(datetime_unix).strftime('%Y-%m-%d %H:%M UTC')
        
        # Build message
        message = f"🚨 <b>{'Stock: ' + stock if stock else 'Market News'}</b>\n\n"
        message += f"<b>{headline}</b>\n\n"
        
        if summary and len(summary) > 0:
            # Limit summary length
            summary_short = summary[:300] + '...' if len(summary) > 300 else summary
            message += f"{summary_short}\n\n"
        
        message += f"📰 Source: {source}\n"
        message += f"🕐 {date_str}\n\n"
        message += f"🔗 <a href='{url}'>Read more</a>"
        
        return message
    
    def process_articles(self, articles, stock=None):
        """Process and send new articles"""
        new_articles_count = 0
        
        for article in articles:
            article_id = article.get('id') or article.get('url')
            
            if not article_id or article_id in self.sent_articles:
                continue
            
            # For general news, check if it's relevant
            if not stock and not self.is_relevant(article):
                continue
            
            # Send the article
            message = self.format_message(article, stock)
            if self.send_telegram_message(message):
                self.sent_articles.add(article_id)
                new_articles_count += 1
                logger.info(f"Sent article: {article.get('headline', 'Unknown')[:50]}...")
                time.sleep(1)  # Small delay between messages
        
        return new_articles_count
    
    def run_once(self):
        """Run one cycle of news checking"""
        logger.info("Starting news check cycle...")
        total_new_articles = 0
        
        # Check news for each stock
        for stock in self.stocks:
            logger.info(f"Checking news for {stock}...")
            articles = self.fetch_stock_news(stock)
            count = self.process_articles(articles, stock)
            total_new_articles += count
            time.sleep(1)  # Rate limiting between API calls
        
        # Check general technology news for relevant keywords
        logger.info("Checking general technology news...")
        general_articles = self.fetch_general_news()
        count = self.process_articles(general_articles)
        total_new_articles += count
        
        # Save the updated list of sent articles
        self.save_sent_articles()
        
        logger.info(f"Cycle complete. Sent {total_new_articles} new articles.")
        return total_new_articles
    
    def run(self, interval_minutes=5):
        """Run the bot continuously"""
        logger.info("🤖 Stock News Bot Started!")
        logger.info(f"Monitoring stocks: {', '.join(self.stocks)}")
        logger.info(f"Check interval: {interval_minutes} minutes")
        
        # Send startup message
        startup_msg = "🤖 <b>Stock News Bot Started!</b>\n\n"
        startup_msg += f"📊 Monitoring: {', '.join(self.stocks)}\n"
        startup_msg += f"🔍 Keywords: AI, semiconductors, space, robotics, tech\n"
        startup_msg += f"⏱ Check interval: {interval_minutes} minutes"
        self.send_telegram_message(startup_msg)
        
        while True:
            try:
                self.run_once()
                logger.info(f"Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    bot = StockNewsBot()
    bot.run(interval_minutes=5)
