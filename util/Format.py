# coding=utf-8
import re
import locale
import logging

logger = logging.getLogger("Format")


def str_to_unicode(text=''):
    return text.decode('utf-8') if isinstance(text, str) else text


def str_to_dict(src_str='', pattern=''):
    """
    使用正则表达式匹配源字符串，根据正则的分组将字符串中匹配到的键值对保存为字典类型
    例如：r'([^\s:]+):\s?([^\n]*)\s*' 正则表达式返回的字典{group(1): group(2)}
    :param src_str: 
    :param pattern: 
    :return: 
    """
    src_str = src_str if src_str else ''
    target_dict = {}
    if src_str:
        src_str_pattern = re.compile(pattern) if pattern else None
        try:
            src_str_list = src_str_pattern.findall(src_str) if src_str_pattern else []
        except Exception as e:
            logger.debug(u"无法正则表达式无法匹配字符串, 调试信息: {}".format(str(e)))
            return {}
        if src_str_list:
            for k, v in src_str_list:
                target_dict[k] = v
            return target_dict
        else:
            return {}
    else:
        return {}


def clear_text(text='', keep=True):
    """
    去除文本中的空字符（空格，制表符，换行符）
    :param text:文本或元素为文本的列表 
    :param keep: True 保留文本中的空格，将多个空字符替换成一个空格。
                 False 去除文本内所有空字符
    :return: 去除空字符后的文本或列表
    """
    pattern_blank = re.compile(r'\s+')
    text = text if text else ''
    if not text:
        return text
    if isinstance(text, list):
        text = [str_to_unicode(line) for line in text]
        if keep:
            text = [pattern_blank.sub(' ', line.strip()) for line in text]
        else:
            text = [pattern_blank.sub('', line.strip()) for line in text]
    elif isinstance(text, (str, unicode)):
        if keep:
            text = pattern_blank.sub(' ', text.strip())
        else:
            text = pattern_blank.sub('', text.strip())
    return text


def number_format(num=None, places=0, index=0, auto=True):
    """
    将字符串中的数字全部提取并按照index索引和规定places精度返回
    :param num: 包含数字的字符串
     :type: string
    :param places: 要求返回的数字精度
     :type: int
    :param index: 要求返回第几个数字，从第0个开始,最后一个为-1
     :type: int
    :param auto: 如果索引超出列表范围，返回最接近给定索引的数字,False返回第0个
     :type: bool
    :return: 返回数字
     :type: int or float
    """
    _number_regex = None
    if not isinstance(num, (int, float)):
        if _number_regex is None:
            _number_regex = re.compile(r'(-?\d+.?\d+)')
        num = clear_text(num).replace(',', '')
        match = _number_regex.findall(num)
        try:
            num = float(match[index]) if match else 0.0
        except Exception, e:
            if auto is None:
                num = match[0]
            elif auto:
                num = float(match[len(match) - 1])
            else:
                raise Exception(str(e))
    if places > 0:
        return float(locale.format("%.*f", (places, float(num)), True))
    else:
        return int(num)


def int_with_commas(x):
    """整型数带逗号输出比如1000则返回1,000"""
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + int_with_commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


if __name__ == "__main__":
    pass
