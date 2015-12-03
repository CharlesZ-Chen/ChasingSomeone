#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
static method
Utility.send_email()
'''

__author__ = 'Quan Zhang'

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Utility(object):

    @staticmethod
    def send_email(*args, **kwargs):
        me = kwargs.get('From')
        you = kwargs.get('To')
        follower_name = kwargs.get('follower_name')
        user_name = kwargs.get('user_name')

        if not (me and you and follower_name and user_name):
            print 'Wrong arguments passed!'
            return None;

        subject = 'You got a new notification on ChasingSomeone!'

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you

        text = 'Hi, %s: %s has post a new status!' % (user_name, follower_name)
        html = """\
            <html>
              <head></head>
              <body>
                <p>Hi, %s: <br>
                   %s has post a new status!
                   <br>
                   <a href="https://localhost:8080">link</a>
                </p>
              </body>
            </html>
            """ % (user_name, follower_name)

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.ehlo()
            mail.login(me, 'pzcqkjtuscmivgsv')
            mail.sendmail(me, you, msg.as_string())
            mail.quit()
        except smtplib.SMTPException, e:
            print e.args
            print 'Error occured when sending email'

if __name__ == '__main__':
    Utility.send_email(user_name='colin_27', follower_name='leipu', From='ChasingSomeoneApp@gmail.com', To='colin_27@163.com')