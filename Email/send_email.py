from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
import os


path = os.path.dirname(__file__) # 当前文件路径
report_path= os.path.dirname(path) +'\\Report\\report.html' # 测试报告路径

def send_mail():
    """
    发送邮件
    """
    with open(report_path,'rb') as f:
        report=f.read()
    smtpserver = 'smtp.mxhichina.com'  # 邮件服务器
    sender = '***'  # 发件人邮箱
    # pwd = '***'  # 授权码
    pwd = '***'
    receiver = ['***']  # 接收人邮箱
    subject = u'UAP自动化测试报告'  # 邮件标题
    msg = MIMEMultipart()
    msg.attach(MIMEText('邮件正文', _subtype='txt', _charset='utf-8'))
    msg['From'] = sender
    msg['To'] = ','.join(receiver)
    msg['Subject'] = subject
    att = MIMEText(report, 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att.add_header("Content-Disposition", "attachment", filename=report_path)
    msg.attach(att)
    # 发送邮件
    try:
        smtp = smtplib.SMTP(smtpserver)
        smtp.login(sender, pwd)  # 登录邮箱
        smtp.sendmail(sender, receiver, msg.as_string())  # 发送者和接收者
        smtp.quit()
        print("测试报告邮件已发出！注意查收。" +
              str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    except Exception as e:
        print("send mail error:{}".format(e))
