import os
import smtplib
from email.message import EmailMessage
from skinmonkey_se import exec

def send_mail(sum):
    EMAIL_ADDRESS = "pratprasert@gmail.com"
    EMAIL_PASSWORD = "okyi evqd qyhq gdkq"

    msg = EmailMessage()
    msg['Subject'] = "Daily Skin Report"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = [EMAIL_ADDRESS]
    message = ''
    for item, df in sum.items():
        message += f'<div><strong><u>Item: </u>{item}</strong></div><p>{df}</p>'
        
    # msg.set_content(message)
    msg.add_alternative(message, subtype='html') # html

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    sum = exec()
    send_mail(sum)