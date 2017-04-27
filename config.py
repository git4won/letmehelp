#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by VinChan on 4/23/2017 0023
import sys
import os
import datetime
import logging
from logging.handlers import RotatingFileHandler

if __name__ == "__mian__":
    print('Access Denied.')
    sys.exit()

"""
flask 配置
"""
DEBUG = True

APP_ROOT = getattr(sys, '__APP_ROOT__', os.path.split(os.path.realpath(__file__))[0])

APP_PATH = getattr(sys, '__APP_PATH__', os.path.join(APP_ROOT, 'packages'))

"""
日志配置
"""
APP_LOG = getattr(sys, '__APP_LOG__', True)
level = logging.DEBUG if DEBUG else logging.ERROR
LOG_DIR = os.path.join(APP_ROOT, "logs")
# 仅应用日志
if APP_LOG:
    # 每小时一个日志
    _handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIR, 'spider_' + datetime.datetime.now().strftime("%Y-%m-%d_%H") + ".logs"),
        mode='a+')
    _handler.setFormatter(
        logging.Formatter(fmt='>>> %(asctime)-10s %(name)-12s %(levelname)-8s %(message)s', datefmt='%H:%M:%S'))
    LOG = logging.getLogger('spider')
    LOG.setLevel(level)
    LOG.addHandler(_handler)
    # 在控制台打印
    _console = logging.StreamHandler()
    LOG.addHandler(_console)

# 常见浏览器的User-Agent
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.9 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/530.9',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.6 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/530.6',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/530.5',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 '
    'Chrome/27.0.1453.93 Safari/537.36',  # Ubuntu
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',  # IE10
    'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0))',  # IE9
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; .NET CLR 2.0.50727; .NET CLR '
    '3.0.4506.2152; .NET CLR 3.5.30729)',  # IE8
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; InfoPath.2; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET '
    'CLR 3.5.30729)',  # IE7
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 '
    'LBBROWSER',  # 猎豹浏览器
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ' #qq浏览器 ie 6
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ', #qq 浏览器 ie7
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15', #firefox
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',  # firefox ubuntu
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',  # firefox mac
    'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',  # Opera windows
    # 'Googlebot/2.1 (+http://www.googlebot.com/bot.html)',  # Google蜘蛛
    # 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',  # Bing蜘蛛
    # 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',  # Yahoo蜘蛛
]
# 默认的头部
DEFAULT_HEADERS = {'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4', 'Accept-Encoding': 'gzip, deflate, sdch, br', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

# 常用的正则
COMMON_REGEX = {
    # Email的规则: name @ domain
    # name最长64，domain最长253，总长最长256
    # name可以使用任意ASCII字符: 大小写英文字母(a - z, A - Z)、数字(0 - 9)
    # 字符 !  # $%&'*+-/=?^_`{|}~
    # 字符.不能是第一个和最后一个，不能连续出现两次
    # 但是有些邮件服务器会拒绝包含有特殊字符的邮件地址
    # domain仅限于26个英文字母、10
    # 个数字、连词号 -
    # 连词号 - 不能是第一个字符
    # 顶级域名（com、cn等）长度为2到6个
    'EMAIL': r'^[a-z_0-9-]{1,64}@([a-z0-9-]{1,200}\.){1,5}[a-z]{1,6}$',
    # URL
    'URL': r'^https?://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$',
    # 国内手机号码根据维基百科上公布的手机号码分配
    # https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%86%85%E5%9C%B0%E7%A7%BB%E5%8A%A8%E7%BB%88%E7%AB%AF%E9%80%9A%E8%AE%AF%E5%8F%B7%E7%A0%81
    'PHONE': r'',
    # 身份证号码,仅根据身份证长度校验，并没有根据实际内容限制检验
    'ID_CARD': r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)',
    # ip地址
    'IP': r'((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))',
    # 强密码(必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间)
    'PASSWORD': r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$',
    # 匹配汉字
    'CHINESE': r'^[\u4e00-\u9fa5]{0,}$'
}
