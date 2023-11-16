import os
import smtplib
from email.message import EmailMessage
from skinmonkey_se import exec
import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load the environment variables

load_dotenv()

def send_mail(sum):
    EMAIL_ADDRESS = "pratprasert@gmail.com"
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    print(EMAIL_PASSWORD)
    
    msg = EmailMessage()
    msg['Subject'] = "Daily Skin Report"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = [EMAIL_ADDRESS]

    message = ''
    for item, df in sum.items():
        message += f'''
            <h3 class='item-name'><u>Item</u>: {item}</h3>
            <p>{df.to_html()}</p>
            '''
    html_string = f'''
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                table {{
                width: 100%;
                border-collapse: collapse;
                text-align: center;
                }}
                thead th {{
                text-align: center;
                color: red;
                background-color: silver;
                }}
                tbody > tr:first-child > * {{
                background-color: yellow;
                }}
                table, th, tr {{
                padding: 0.5rem;
                }}
                .item-name {{ text-align: left; }}
            </style>
        </head>
        <body>
            <a href="https://skinsmonkey.com/trade">SkinsMonkey</a>
            <p>[update] &nbsp; {datetime.datetime.now():%d/%m/%Y %H:%M:%S}</p>
            <div>{message}</div>
        </body>
    </html>
    '''
    # msg.set_content(message)
    msg.add_alternative(html_string, subtype='html') # html

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print('\nEmail sent...')

if __name__ == '__main__':
    sum = exec()
    send_mail(sum)