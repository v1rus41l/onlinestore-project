from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib
import random
login = 'lifestyleofficial@yandex.ru'
password = 'LifeStyle24'

def send_email(to_addr):
    cod = random.randint(10000000, 99999999)
    text = f"Вот ваш одноразовый код подтверждения по твоему запросу: {cod}. Если у вас уже есть код или он больше не" \
           f" нужен, то просто проигнорируйте это письмо."
    msg = MIMEMultipart()
    msg['From'] = login
    msg['To'] = to_addr
    msg['Subject'] = "Код подтверждения"
    msg.attach(
        MIMEText(text, "plain")
    )

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(login)
    server.login(login, password)
    server.auth_plain()
    server.send_message(msg)
    server.quit()
    return str(cod)
