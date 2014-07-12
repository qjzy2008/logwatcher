#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib
import os
import xml.dom.minidom
import time
import datetime
from os.path import join, getsize
from email.mime.text import MIMEText

#要发给谁
mail_list = ["13751161587@139.com", "2355340816@qq.com", "2355340802@qq.com", "13169949583@wo.cn"]

knowsfiles = {"filename":"path"}

def getServerInfo():
    path = os.getcwd() + "/configs/servers.xml";
    dom = xml.dom.minidom.parse(path)
    root = dom.documentElement
    serverGroupXml = root.getElementsByTagName('ServerGroup')[0]
    return serverGroupXml.getAttribute('id')

#检查log文件是否有更新
def checkValgrindLog():
    checkInfo = ""
    path = os.getcwd() + "/bin/gameserver/"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.find("gs_valgrind_") != -1:
                fullPath = join(root,file)
                if not knowsfiles.has_key(file):
                    # 搜索该文件中是否有Invalid read/write
                    if open(fullPath).read().find("Invalid") != -1:
                        checkInfo += ("ServerId:" + getServerInfo() + " has Invalid read or write. log=" + fullPath + "\n")
                    knowsfiles[file] = fullPath
    return checkInfo

def send_mail(to_list,sub,content):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.163.com"
    mail_user="logwatcher"
    mail_pass="zhaoyang"
    mail_postfix="163.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        print '1'
        return True
    except Exception, e:
        print '2'
        print str(e)
        return False
        
if __name__ == '__main__':
    while (1):
        checkInfo = checkValgrindLog()
        if checkInfo != "":
            for mail in mail_list:
                if send_mail(mail, "valgrind invalid read/write - " + str(datetime.datetime.now()), checkInfo):
                    print "发送成功"
                else:
                    print "发送失败"                
        time.sleep(60)
    exit()
