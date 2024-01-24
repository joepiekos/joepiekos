from flask import Flask, render_template
import random
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

def scrape_cricinfo_news():
    url = "https://www.espncricinfo.com/cricket-news"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_articles = []

        # Extract news articles from the HTML
        for article in soup.find_all('div', class_='news-list'):
            news_title = article.find('span', class_='headline').text.strip()
            news_link = article.find('a', class_='anchor-detail')['href']
            news_articles.append({'title': news_title, 'link': news_link})

        return news_articles

    return None

def send_email(news_articles):
    # Set up your email configuration
    smtp_server = 'your_smtp_server'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'
    recipient_email = 'recipient@example.com'

    # Create the email content
    subject = 'Daily Cricket News'
    body = '\n'.join([f"{article['title']} - {article['link']}" for article in news_articles])
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = recipient_email

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, recipient_email, msg.as_string())

@app.route('/', methods=['GET'])
def index():
    bethanMessage = "your mind is filled with thoughts of chip"
    return render_template('index.html', bethanMessage = bethanMessage)

@app.route('/get_daily_news', methods=['POST'])
def get_daily_news():
    # Scrape daily news articles
    news_articles = scrape_cricinfo_news()

    if news_articles:
        # Send the news articles via email
        send_email(news_articles)
        return render_template('index.html', message='Daily news articles sent to your email!')
    else:
        return render_template('index.html', message='Failed to fetch news articles.')

if __name__ == '__main__':
    app.run(debug=True)