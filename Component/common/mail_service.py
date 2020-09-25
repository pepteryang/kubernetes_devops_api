# -*- coding:utf-8-*-
# @Author : PeterYang
# @Email : snfnvtk@163.com
# @Time : 2018/9/13 14:13
# @Site : 
# @File : mail_service.py
# @Software : PyCharm


from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from Component.common.SystemLog import system_log

import smtplib
import os


@system_log
def SendEmailText(text, receive=None,subject=None):
    From = "it_opt@bqrzzl.com"
    acc = "zhiqun.yang@bqrzzl.com"
    if receive:
        To = receive
    else:
        To = "zhihui.he@bqrzzl.com"
    username = 'it_opt@bqrzzl.com'
    password = 'qazWSX123789..'
    server = smtplib.SMTP("smtp.exmail.qq.com")

    server.login(username, password)  # 仅smtp服务器需要验证时

    # 构造MIMEMultipart对象做为根容器
    main_msg = MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    text_msg = MIMEText("%s" % text)
    main_msg.attach(text_msg)

    # 设置根容器属性
    main_msg['From'] = From
    main_msg['To'] = To

    main_msg['Cc'] = acc
    main_msg['Subject'] = Header(subject, "utf-8")
    main_msg['Date'] = formatdate()

    # 得到格式化后的完整文本
    fullText = main_msg.as_string()

    # 用smtp发送邮件
    try:
       server.sendmail(From, To.split(',') + acc.split(','), fullText)
    finally:
        server.quit()


@system_log
def SendEmailAttach(text, receive=None,subject=None, file_name=None):
    try:
        From = "it_opt@bqrzzl.com"
        acc = "zhiqun.yang@bqrzzl.com"
        if receive:
            To = receive
            # To = ["zhihui.he@bqrzzl.com","zhiqun.yang@bqrzzl.com","%s" % receive]
        else:
            To = "zhihui.he@bqrzzl.com"
        username = 'it_opt@bqrzzl.com'
        password = 'qazWSX123789..'
        server = smtplib.SMTP("smtp.exmail.qq.com")

        server.login(username, password)  # 仅smtp服务器需要验证时

        # 构造MIMEMultipart对象做为根容器
        main_msg = MIMEMultipart()

        # 构造MIMEText对象做为邮件显示内容并附加到根容器
        text_msg = MIMEText("%s" % text)
        main_msg.attach(text_msg)

        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)

        # 读入文件内容并格式化
        data = open(file_name, 'rb')
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        encoders.encode_base64(file_msg)

        # 设置附件头
        basename = os.path.basename(file_name)

        # 解决中文附件名乱码问题
        file_msg.add_header('Content-Disposition', 'attachment', filename=('gbk', '', basename))
        main_msg.attach(file_msg)

        # 设置根容器属性
        main_msg['From'] = From
        main_msg['To'] = To

        main_msg['Cc'] = acc
        main_msg['Subject'] = Header(subject, "utf-8")
        main_msg['Date'] = formatdate()

        # 得到格式化后的完整文本
        fullText = main_msg.as_string()

        # 用smtp发送邮件
        try:
            server.sendmail(From, To.split(',') + acc.split(','), fullText)
        finally:
            server.quit()
    except Exception as e:
        return e


@system_log
def SendEmailHtml(html, receive=None, subject=None, file_name=None):
    From = "it_opt@bqrzzl.com"
    if receive:
        To = receive
    else:
        To = "zhihui.he@bqrzzl.com"
    username = 'it_opt@bqrzzl.com'
    password = 'qazWSX123789..'
    server = smtplib.SMTP("smtp.exmail.qq.com")

    server.login(username, password)  # 仅smtp服务器需要验证时

    # 构造MIMEMultipart对象做为根容器
    main_msg = MIMEMultipart('alternative')

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    # text_msg = MIMEText("%s" % text)
    html_file = MIMEText(html, 'html', 'utf-8')
    main_msg.attach(html_file)

    if file_name:
        # 构造MIMEBase对象做为文件附件内容并附加到根容器
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)

        # 读入文件内容并格式化
        data = open(file_name, 'rb')
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        encoders.encode_base64(file_msg)

        # 设置附件头
        basename = os.path.basename(file_name)

        # 解决中文附件名乱码问题
        file_msg.add_header('Content-Disposition', 'attachment', filename=('gbk', '', basename))
        main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = From
    main_msg['To'] = To

    main_msg['Subject'] = Header(subject, 'utf-8')
    main_msg['Date'] = formatdate()

    # 得到格式化后的完整文本
    fullText = main_msg.as_string()

    # 用smtp发送邮件
    try:
       server.sendmail(From, To.split(','), fullText)
    finally:
        server.quit()