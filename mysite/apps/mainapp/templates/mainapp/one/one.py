#! /usr/bin/python3
# coding: UTF-8

import requests
import re
import os

def getInfo(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    res = r.text
    no = re.findall(r'<a href="http://wufazhuce.com/one/([\w\W]*?)a>',res)

    pic_url = "\n".join(re.findall(r'src="(.+?)" alt=',no[0])) + '\n'
    words = "\n".join(re.findall(r'">([\w\W]*?)</',no[1])) + '\n'

    pwd = os.getcwd()
    filename = pwd + '/one.txt'
    filename2 = pwd + '/all.txt'

    print(filename)
    with open(filename,'w') as f:
        f.write(words)
    with open(filename2,'a') as f2:
        f2.write(pic_url)
        f2.write(words)

getInfo("http://wufazhuce.com")
