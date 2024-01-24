from flask import Flask, render_template
import random
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app._static_folder = 'static'

def scrape_cricinfo_news():
    url = "https://www.espncricinfo.com/cricket-news"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        news_articles = []

        # Extract news articles from the HTML
        for article in soup.find_all('div', class_='ds-border-b ds-border-line ds-p-4'):
            news_title = article.find('h2', class_='ds-text-title-s ds-font-bold ds-text-typo').text.strip()
            news_link = article.find('a', class_='')['href']
            news_articles.append({'title': news_title, 'link': news_link})

        return news_articles

    return None

def send_email(news_articles):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'joe.piekos@gmail.com'
    smtp_password = 'iduo stcc hpsb zhvc'
    recipient_email = 'joe.piekos@gmail.com'

    # Create the email content
    subject = 'Daily Cricket News'
    body = '\n'.join([f"{article['title']} - {article['link']}" for article in news_articles])
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_username
    msg['To'] = recipient_email

    # Connect to the SMTP server and send the email
    #with smtplib.SMTP(smtp_server, smtp_port) as server:
     #   server.starttls()
      #  server.login(smtp_username, smtp_password)
       # server.sendmail(smtp_username, recipient_email, msg.as_string())
    
    with smtplib.SMTP(smtp_server, smtp_port) as mail_server:
        # identify ourselves to smtp gmail client
        mail_server.ehlo()
        # secure our email with tls encryption
        mail_server.starttls()
        # re-identify ourselves as an encrypted connection
        mail_server.ehlo()
        mail_server.login(smtp_username, smtp_password)
        mail_server.sendmail(smtp_username,recipient_email,msg.as_string())

@app.route('/', methods=['GET'])
def index():
    bethanMessage = "your mind is filled with thoughts of chip"
    return render_template('index.html', bethanMessage = bethanMessage)

@app.route('/get_daily_news', methods=['POST'])
def get_daily_news():
    # Scrape daily news articles
    news_articles = scrape_cricinfo_news()
    bethanMessage = "your mind is filled with thoughts of chip"
    if news_articles:
        # Send the news articles via email
        send_email(news_articles)
        return render_template('index.html', message='Daily news articles sent to your email!', status = news_articles[0]['link'])
    else:
        return render_template('index.html', message='Failed to fetch news articles.',bethanMessage = bethanMessage)

if __name__ == '__main__':
    app.run(debug=True)
    #tst = scrape_cricinfo_news()
    #print(tst[0]['title'])