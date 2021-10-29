import pandas as pd
import smtplib
import time
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

#Changer ces informations (Email, pass, sujet, message,lien vers le cv ou juste son nom si le cv est dans le meme repertoire du script)
ton_email = "ton_email@gmail.com"
mot_de_pass = "mot_de_passe"
subject="Candidature spontanée au poste d'ingénieur..."

message="Bonjour,\n Je m'appelle khalid bouhabba, je suis un...." #utilisez \n pour sauter la ligne

e = pd.read_excel("Email.xlsx")
emails = e['Emails'].values
cv_path="Cv_Khalid_Bouhabba.pdf"

msg = MIMEMultipart()
msg['From'] = ton_email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject
msg.attach(MIMEText(message))

part = MIMEBase('application', "octet-stream")
with open(cv_path, 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename={}'.format(Path(cv_path).name))

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(ton_email, mot_de_pass)

i=1
for email_ in emails:
    msg.attach(part)
    server.sendmail(ton_email, email_, msg.as_string())
    msg['To'] = email_
    print(i,"- l'email à: ",email_, "est envoyé!")
    i+=1
    time.sleep(15)
server.quit()