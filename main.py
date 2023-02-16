from smtplib import SMTP_SSL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telethon import TelegramClient, events, sync
import time
import re

def sendMail(mail_content,recv_address):
    # param mail_content 邮件内容
    # param recv_address 接收邮箱
    sender_address = 'xxxx@gmail.com' # 邮箱账号
    sender_pass = 'xxxxxxxxxxxxxxxx'    #密码
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = recv_address
    message['Subject'] = '代表着上网,代表着冲浪,OK了家人们!'
    message.attach(MIMEText(mail_content,'plain'))
    session = smtplib.SMTP('smtp.gmail.com',587)
    session.starttls()
    session.login(sender_address,sender_pass)
    text = message.as_string()
    session.sendmail(sender_address,recv_address,text)
    print("send {} successfully".format(recv_address))
    session.quit()

api_id = xxxxxxxx # api_id
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' # api_hash
# 登陆client
client = TelegramClient('session_name',api_id,api_hash)
client.start()
# 向机器人发送/get
client.send_message('xxx','xxx')
# 延迟等待回复
time.sleep(5)
# 读取id.txt文件,取出所有邮箱
with open("mailConfig.txt",'r+',encoding="utf-8") as f_open:
    recvAddresss = f_open.read()
f_open.close()
# split分隔开每个邮箱并放到数组中
recvAddressList = recvAddresss.split(",")
# 打印一下看看是否正确
print(recvAddressList)
with client:
    # 获取回复信息
    text = client.get_messages('@freenodeshare_bot',limit=2)
    # 回复信息为Message类型，取长度减一为主要信息
    lens = len(text)
    # 把Message转换为str类型好进行字符串处理
    Recv = str(text[lens-1])

    #字符串处理提取其中主要信息保存到v3文件

    messageStart = "message='" # 开头
    messageEnd = "', out=False" # 结尾
    startLen = len(messageStart) # 取字符串开头长度,在提取时候去掉
    try:
        startPoint = Recv.find(messageStart)
        endPoint = Recv.find(messageEnd)
        v3 = Recv[startPoint+startLen:endPoint:]
        v3List = v3.split("\\n") # \n 分开
        with open("v3.txt","w+",encoding="utf-8") as f:
            for i in v3List:
                f.write(i) # 每条写入
                f.write("\n") # 每条后边加回车
        f.close()
        with open("v3.txt","r",encoding='utf-8') as f:
            content = f.read() #读取文件
            for recvAddress in recvAddressList: #遍历邮箱数组
                sendMail(content, recvAddress) #发送邮件
        f.close()
    except:
        with open("v3.txt","w",encoding="utf-8") as f:
            f.write("获取失败")
        f.close()





