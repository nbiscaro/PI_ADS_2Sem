import smtplib
import mimetypes
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def adiciona_anexo(msg, filename):
    if not os.path.isfile(filename):
        return

    ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())

        encoders.encode_base64(mime)

    indice = filename.rfind("/") + 1
    nome_arquivo = filename[indice:]

    mime.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)
    msg.attach(mime)

def email(to, assunto, mensagem, anexos):
    email_from = "algopositivospc@gmail.com"
    email_to = to

    msg = MIMEMultipart()

    msg['From'] = email_from
    msg['To'] = ", ".join(email_to)
    msg['Subject'] = assunto


    html = f"""\
    <html>
      <head></head>
      <body>
        <img src="https://www.spcbrasil.org.br/img/master/logomarca.png" />
        <p><font size="4">{mensagem}.</font></p>
      </body>
    </html>
    """

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    for arquivos in anexos:
        filename = arquivos
        adiciona_anexo(msg, filename)

    smtp = "smtp.gmail.com"

    server = smtplib.SMTP(smtp, 587)
    server.starttls()
    text = msg.as_string()
    server.login(email_from, open('senha.txt').read().strip())

    server.sendmail(email_from, email_to, text)
    server.quit()

