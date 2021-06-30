#!/usr/bin/python3

import argparse
import logging
import smtplib
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

from data_email import addr_from, addr_to, password


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--from", dest="addr_from", help="адресат", default=f"{addr_from}")
    parser.add_argument("-p", "--psw", dest="password", help="пароль", default=f"{password}")
    parser.add_argument("-t", "--to", dest="addr_to", help="получатель", default="", required=True)
    parser.add_argument("-s", "--sub", dest='sub', help="subject", default="python script")
    parser.add_argument("-b", "--body", dest="body", help="Текст сообщения", default="Ваш отчет готов!")
    parser.add_argument("-F", "--file", dest="file", help="file", default="")
    parser.add_argument("-S", "--smtp-server", dest="smtp_server", help="smtp server", default='mail.aac.in.ua')
    parser.add_argument("-P", "--port", dest="port", help="port", default="143")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    msg = MIMEMultipart()
    msg['From'] = args.addr_from
    msg['To'] = args.addr_to
    msg['Subject'] = args.sub

    body = args.body
    msg.attach(MIMEText(body, 'plain'))

    # Вложение
    if args.file != "":
        filename = args.file
        fp = open(filename, 'rb')
        att = MIMEApplication(fp.read())
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filename))
        msg.attach(att)

    server = smtplib.SMTP(args.smtp_server)
    # server.set_debuglevel(True)
    server.starttls()
    server.login(args.addr_from, args.password)
    server.send_message(msg)
    server.quit()




if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(e)
