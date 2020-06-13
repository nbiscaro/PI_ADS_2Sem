import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

email_from = "algopositivospc@gmail.com"
email_to = "emailDestino@....com"

msg = MIMEMultipart()

msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = "Assunto"


html = """\
<html>
  <head></head>
  <body>
    <img src="https://www.spcbrasil.org.br/img/master/logomarca.png" />
    <p><font size="6">Este é um e-mail automático, por favor, não responda.</font></p>
  </body>
</html>
"""

part2 = MIMEText(html, 'html')

msg.attach(part2)

filename = 'DocVisao.pdf'
attachment = open('Algo-Positivo_Documento-de-Visão.pdf','rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
attachment.close()


smtp = "smtp.gmail.com"

server = smtplib.SMTP(smtp, 587)
server.starttls()
text = msg.as_string()
server.login(email_from, open('senha.txt').read().strip())

server.sendmail(email_from, email_to, text)
server.quit()

print("Sucesso ao enviar o email")
