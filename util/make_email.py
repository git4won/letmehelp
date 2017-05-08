# -*- coding: utf-8 -*-
import re
import smtplib
from instance.config import EMAIL_PROFILES
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


def send_msg(content='', dist_email=''):
    # init_smtp
    vin_work = EMAIL_PROFILES.get('vin_work', None)
    if not vin_work:
        return {'status': 0, 'msg': 'Email UNDEFINED!'}
    # 发件邮箱
    email_address = vin_work.get('email_address')
    password = vin_work.get('password')
    smtp_server = vin_work.get('smtp_server')
    smtp_port = vin_work.get('smtp_port')
    pattern_email = re.compile(r'^[a-z_0-9-]{1,64}@([a-z0-9-]{1,200}\.){1,5}[a-z]{1,6}$')
    match = pattern_email.match(dist_email)
    dist_email = match.group() if match else ''
    if not dist_email:
        raise ValueError
    # msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'Let_me_help <%s>' % email_address)
    msg['To'] = _format_addr(u'User<%s>' % dist_email)
    msg['Subject'] = Header(u'SYSTEM', 'utf-8').encode()

    # send
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # server.set_debuglevel(1)
    server.login(email_address, password)
    try:
        server.sendmail(email_address, [dist_email], msg.as_string())
        return {'status': 200, 'msg': "SEND OK"}
    except Exception as e:
        raise e
    finally:
        server.quit()
