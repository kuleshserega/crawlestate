import os
import sys

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import get_proxy_from_db, set_proxy_status


def check_proxies():
    proxy_list = get_proxy_from_db()
    dead_proxy_list = []
    for pid, proxy in proxy_list.iteritems():
        try:
            requests.get(
                'https://google.com',
                proxies={'https': proxy},
                timeout=30)
            set_proxy_status(pid, 'Works')
        except IOError:
            dead_proxy_list.append(proxy)
            set_proxy_status(pid, 'Dead')

    if dead_proxy_list:
        send_email(dead_proxy_list)


def send_email(proxy_list):
    import smtplib
    from email.mime.text import MIMEText
    me = 'nickl.zubarev@gmail.com'
    you = 'kulesh_serega@mail.ru'
    smtp_server = 'smtp.gmail.com'

    msg_proxy_list = ''
    for proxy in proxy_list:
        msg_proxy_list += proxy + '\n'

    msg = MIMEText(msg_proxy_list)
    msg['Subject'] = 'Proxies are dead:\n'
    msg['From'] = me
    msg['To'] = you
    s = smtplib.SMTP(smtp_server, 587)
    s.starttls()
    s.login('nickl.zubarev@gmail.com', 'n1cklzub')
    s.sendmail(me, [you], msg.as_string())
    s.quit()


if __name__ == '__main__':
    check_proxies()
