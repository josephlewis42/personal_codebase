#!/usr/bin/env python
import datetime
import re
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user = "joehms22@gmail.com"
gmail_pwd = "password"
    
def mail(to, subject, body):
    msg = MIMEMultipart('alternative')

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    if '<html>' in body:
        msg.attach(MIMEText(re.sub(r'<.*?>', '', body), 'plain'))
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    m = smtplib.SMTP("smtp.gmail.com", 587)
    m.ehlo()
    m.starttls()
    m.ehlo()
    m.login(gmail_user, gmail_pwd)
    m.sendmail(gmail_user, to, msg.as_string())
    m.quit()

if __name__ == "__main__":
    while datetime.datetime.today() < datetime.datetime(2011, 5, 24):
        time.sleep(10)
        
    mail("joehms22@gmail.com", "subject", "<html><b>body</b> nonbold</html>")