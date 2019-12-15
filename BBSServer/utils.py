import datetime
import json
import smtplib
import random
def sendEmail(type,receiver):
    if(type==1):
        opration_type = "注册"
    else:
        opration_type = "修改密码"
    vc = ""
    for i in range(6):
        temp = random.randrange(0, 3)
        if temp == 0:
            ch = chr(random.randrange(ord('A'), ord('Z') + 1))
            vc += ch
        elif temp == 1:
            ch = chr(random.randrange(ord('a'), ord('z') + 1))
            vc += ch
        else:
            ch = str((random.randrange(0, 10)))
            vc += ch

    host = 'smtp.163.com'
    port = 465
    sender = 'hbuerbbsserver@163.com'
    body = "<head>" + \
           "<base target=\"_blank\" />" + \
           "<style type=\"text/css\">::-webkit-scrollbar{ display: none; }</style>" + \
           "<style id=\"cloudAttachStyle\" type=\"text/css\">#divNeteaseBigAttach, #divNeteaseBigAttach_bak{display:none;}</style>" + \
           "<style id=\"blockquoteStyle\" type=\"text/css\">blockquote{display:none;}</style>" + \
           "<style type=\"text/css\">" + \
           "body{font-size:14px;font-family:arial,verdana,sans-serif;line-height:1.666;padding:0;margin:0;overflow:auto;white-space:normal;word-wrap:break-word;min-height:100px}" + \
           "td, input, button, select, body{font-family:Helvetica, 'Microsoft Yahei', verdana}" + \
           "pre {white-space:pre-wrap;white-space:-moz-pre-wrap;white-space:-pre-wrap;white-space:-o-pre-wrap;word-wrap:break-word;width:95%}" + \
           "th,td{font-family:arial,verdana,sans-serif;line-height:1.666}" + \
           "img{ border:0}" + \
           "header,footer,section,aside,article,nav,hgroup,figure,figcaption{display:block}" + \
           "blockquote{margin-right:0px}" \
           "</style>" + \
           "</head>" + \
           "<body tabindex=\"0\" role=\"listitem\">" + \
           "<table width=\"700\" border=\"0\" align=\"center\" cellspacing=\"0\" style=\"width:700px;\">" + \
           "<tbody>" + \
           "<tr>" + \
           "<td>" + \
           "<div style=\"width:700px;margin:0 auto;border-bottom:1px solid #ccc;margin-bottom:30px;\">" + \
           "<table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"700\" height=\"39\" style=\"font:12px Tahoma, Arial, 宋体;\">" + \
           "<tbody><tr><td width=\"210\"></td></tr></tbody>" + \
           "</table>" + \
           "</div>" + \
           "<div style=\"width:680px;padding:0 10px;margin:0 auto;\">" + \
           "<div style=\"line-height:1.5;font-size:14px;margin-bottom:25px;color:#4d4d4d;\">" + \
           "<strong style=\"display:block;margin-bottom:15px;\">尊敬的用户：<span style=\"color:#f60;font-size: 16px;\"></span>您好！</strong>" + \
           "<strong style=\"display:block;margin-bottom:15px;\">" + \
           "您正在进行<span style=\"color: red\">"+\
           opration_type+\
           "</span>操作，请在验证码输入框中输入：<span style=\"color:#f60;font-size: 24px\">" + \
           vc + \
           "</span>，以完成操作。" + \
           "</strong>" + \
           "</div>" + \
           "<div style=\"margin-bottom:30px;\">" + \
           "<small style=\"display:block;margin-bottom:20px;font-size:12px;\">" + \
           "<p style=\"color:#747474;\">" + \
           "注意：此操作可能会修改您的密码、使用您的邮箱进行注册。如非本人操作，请及时登录并修改密码以保证帐户安全" + \
           "<br>（工作人员不会向你索取此验证码，请勿泄漏！)" + \
           "</p>" + \
           "</small>" + \
           "</div>" + \
           "</div>" + \
           "<div style=\"width:700px;margin:0 auto;\">" + \
           "<div style=\"padding:10px 10px 0;border-top:1px solid #ccc;color:#747474;margin-bottom:20px;line-height:1.3em;font-size:12px;\">" + \
           "<p>此为系统邮件，请勿回复<br>" + \
           "请保管好您的邮箱，避免账号被他人盗用" + \
           "</p>" + \
           "<p>来自：HBUer生活墙服务器</p>" + \
           "</div>" + \
           "</div>" + \
           "</td>" + \
           "</tr>" + \
           "</tbody>" + \
           "</table>" + \
           "</body>"
    from email.mime.text import MIMEText
    msg = MIMEText(body, 'html')
    msg['subject'] = 'HBUer生活墙修改密码验证'
    msg['from'] = sender
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, 'Jiejie520520')
        s.sendmail(sender, receiver, msg.as_string())
        print('done')
    except smtplib.SMTPException:
        print('wrong')

    return vc


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)
