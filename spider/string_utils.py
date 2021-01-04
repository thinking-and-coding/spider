# -*- coding: utf-8 -*-
# 格式化字符串,替换html格式空格同时去掉前后空格


def format_string(string):
    if string is not None:
        return string.replace(' ', ' ').strip()
    return ''
