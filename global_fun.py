from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.quoprimime import unquote
import json
import os
from posixpath import basename
import smtplib

import requests

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                           ####################################
#                           ###### Send Whatsapp Function ######
#                           ####################################
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def sendWhatsAppMsg(number, msg, Attachments):
    # insetanceId = "621f17f4cd00c56ad254fd4f"
    insetanceId = "62f0dedb0857b14e2d3775c9"
    url = ""
    if msg != "" and Attachments != "":
        url = f"https://wasmsapi.com/api/sendFileWithCaption?token={insetanceId}&phone=+91{number}&message={msg}"
        attachUrl = 'http://103.234.187.197:8014'+Attachments
        url = url+"&link="+unquote(attachUrl)
        loginResponse = requests.post(url, verify=False, timeout=10)
        return json.loads(loginResponse.text)

    elif msg == "" and Attachments != "":
        url = f"https://wasmsapi.com/api/sendFiles?token={insetanceId}&phone=+91{number}"
        attachUrl = 'http://103.234.187.197:8014'+Attachments
        url = url+"&link="+unquote(attachUrl)
        loginResponse = requests.post(url, verify=False, timeout=10)
        return json.loads(loginResponse.text)

    elif msg != "" and Attachments == "":
        url = f"https://wasmsapi.com/api/sendText?token={insetanceId}&phone=+91{number}&message={msg}"
        loginResponse = requests.post(url, verify=False, timeout=10)
        return json.loads(loginResponse.text)
    
    else:
        msg = 'all field are empty! messages will not be sent'
        print(msg)
        return msg

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#
#                           ###################################
#                           ####### Send Email Function #######
#                           ###################################
#
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def sendMail(toEmail, subject, message, attachments):
    try:

        # ServerHost = "mail.waecorp.com"
        # ServerPort = 465  # For starttls
        # Sender = "bridge@waecorp.com"
        # Password = "befes6lw=trAGopr*Trlpip0aTrLjarip?LgocriwahlProt63DU7ofiBlwUcAC?"
        
        ServerHost = "smtp.gmail.com"
        ServerPort = 465  # For starttls
        Sender = "abhishek.kaithwas@cinntra.com"
        Password = "TechAbhi@123!"

        # Create message
        # msg = MIMEText(message, "HTML")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = Sender
        msg['To'] = toEmail
        msg.attach(MIMEText(message, "HTML"))

        if attachments != "":
            filename = os.path.basename(attachments)
            # attachUrl = '/home/www/b2b/standalone_pre/bridge/bridge'+attachments
            attachUrl = '/home/www/b2b/rg_industries_prod/bridge/bridge'+attachments
            
            with open(attachUrl, "rb") as fil:
                part = MIMEApplication(
                        fil.read(),
                        Name=basename(attachUrl)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            msg.attach(part)

        # Create server object with SSL option
        server = smtplib.SMTP_SSL(ServerHost, ServerPort)

        # Perform operations via server
        server.login(Sender, Password)
        server.sendmail(Sender, [toEmail], msg.as_string())
        server.quit()

        return 'sent'
    except Exception as e:
        print(str(e))
        return str(e)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
