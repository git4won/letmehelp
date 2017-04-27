# coding=utf-8
"""
小工具箱-各种实用工具集
0、格式化字符串工具集
0x00 headers_to_dict(headers_str)
0x01 cookies_to_dict(cookies_str)
0x02 intval(text)
0x03 floatval(text)
0x04 str_to_unicode(text='')
0x05 unicode_to_str(text='')
1、爬虫工具
0x10 add_host_into_headers(url="", headers=None)
2、日志及信息提醒
0x20 send_email(contents='', email_addr='')
3、文件及目录操作
0x30 no_space_in_filename(directory_path=None, prefix="_")
0x31 get_pwd(file_path=__file__)
"""
import sys
import os.path
import urlparse

import Format
import make_email

regex_string = {
    'headers': r'([^\s:]+):\s?([^\n]*)\s*',
    'cookies': r'([^=]+)=([^;]+);?\s*',
}

"""
格式化字符串工具
"""


# 0x00 chrome headers convert to dict
def headers_to_dict(headers_str):
    return Format.str_to_dict(headers_str, pattern=regex_string['headers'])


# 0x01 chrome cookies convert to dict
def cookies_to_dict(cookies_str):
    return Format.str_to_dict(cookies_str, pattern=regex_string['cookies'])


# 0x02 str convert to int
def intval(text):
    return Format.number_format(text, 0)


# 0x03 str convert to float, reserved 4 decimal places by default
def floatval(text):
    return Format.number_format(text, 4)


# 0x04 byte str convert to unicode
def str_to_unicode(text=''):
    return text.decode('utf-8') if isinstance(text, str) else text


# 0x05 unicode convert to byte
def unicode_to_str(text=''):
    return text.encode('utf-8') if isinstance(text, unicode) else text


# 0x06 for example convert 1000 to 1,000, add a commas into it
def int_with_commas(x):
    """在数值的千位加上逗号"""
    return Format.int_with_commas(x)


"""
爬虫工具
"""


# 0x10 add host into headers
def add_host_into_headers(url="", headers=None):
    headers = headers if isinstance(headers, dict) else {}
    headers['Host'] = urlparse.urlsplit(url)[1] if url else ''
    return headers


"""
日志及信息提醒工具
"""


# 0x20 use default email address send "contents" to "email_addr"
def send_email(contents='', email_addr=''):
    try:
        rs = make_email.send_msg(content=contents, dist_email=email_addr)
        if not rs.get('status') == 200:
            print(rs.get('msg'))
        else:
            print(rs.get('msg'))
        return 0
    except ValueError:
        print(u"Email的格式不正确！")
        return -1
    except Exception as e:
        print(u"发送失败 %s" % str(e))
        return -1


"""
文件及目录操作工具
"""


# 0x30 replace .py file's name with '_'
def no_space_in_filename(directory_path=None, prefix="_"):
    """重命名py文件，将文件名中的空格' '换成prefix
    :param prefix: 默认使用'_'替换空格
    :param directory_path: 需要遍历的根目录
    :return: [修改历史]
    """
    directory_path = directory_path if directory_path else ''
    history = []
    if isinstance(directory_path, (str, unicode)):
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            directory_path = os.path.normpath(directory_path)
            for dd, ds, fs in os.walk(directory_path):
                for f in fs:
                    if os.path.splitext(f)[1] == '.py':
                        # print os.path.join(dd, f), os.path.exists(os.path.join(dd, f))
                        try:
                            f_no_space = f.replace(' ', prefix)
                            src_file = os.path.join(dd, f)
                            dst_file = os.path.join(dd, f_no_space)
                            os.rename(src_file, dst_file)
                            history.append([src_file, dst_file])
                        except Exception as e:
                            print("ERROR! {}".format(e))
                            return history
                    else:
                        continue
            print(
                u"success! rename {sum} python files in {directory}".format(directory=directory_path, sum=len(history)))
            return history
        else:
            print("{directory} is not exists!".format(directory=directory_path))
            return history
    else:
        return history


# 0x31 get pwd
def get_pwd(file_path=__file__):
    """传入模块路径，返回模块所在文件夹"""
    return getattr(sys, '__APP_ROOT__', os.path.split(os.path.realpath(file_path))[0])


if __name__ == "__main__":
    print get_pwd()
    send_email("hello", "a54959@hotmail.com")
