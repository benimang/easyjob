#coding=utf-8
'''
Created on 2013-5-21
@author: Beni
'''

import smtplib
from email.mime.text import MIMEText


def sendMail(server, username, password, subject, message, fromEmail, toEmailList):
    '''发送邮件'''
    with smtplib.SMTP() as server:
        server.connect(server)
        server.login(username, password)
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = fromEmail
        if type(toEmailList) == list:
            toEmailList = ';'.join(toEmailList)
        msg['To'] = toEmailList
        server.send_message(msg)

