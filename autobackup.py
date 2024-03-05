import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if len(sys.argv) != 5:
    print("Uso: python autobackup.py DATABASE_NAME CONTAINER_NAME ROLE_NAME DUMP_PATH")
    sys.exit(1)

print("############### auto_backup ###############")

DATABASE_NAME = sys.argv[1]
CONTAINER_NAME = sys.argv[2]
ROLE_NAME = sys.argv[3]
DUMP_PATH = sys.argv[4]

DATE_TIME = datetime.now().strftime("%Y.%m.%d.%H.%M")
FILE_NAME = f"dump_{DATABASE_NAME}_{DATE_TIME}.sql"


def send_email(assunto="Backup", body=""):

    print("sending email...")
    try:
        smtp_server = 'smtp-mail.outlook.com'
        smtp_port = 587

        sender_email = 'email@outlook.com'
        sender_password = 'TOP_SECRET'

        receiver_email = 'email@outlook.com'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = assunto

        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, receiver_email, message.as_string())

        server.quit()

        print("email sent")
    except Exception as e:
        print(f"e-mail error: {e}")


comando_bash = (
    f'docker exec -t {CONTAINER_NAME} /bin/bash -c "pg_dump -c -U {ROLE_NAME} {DATABASE_NAME}" > {DUMP_PATH}/{FILE_NAME}'
)

try:
    print("backup started...")
    resultado = subprocess.run(comando_bash,
                               shell=True,
                               check=True,
                               text=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    if resultado.returncode == 0:
        print("backup success")
        send_email(f"SUCESSO - Backup {FILE_NAME}", "Backup realizado com sucesso.")
    else:
        print("backup error")
        send_email(f"FALHA - Backup {FILE_NAME}")
except subprocess.CalledProcessError as e:
    error_message = e.stderr.strip()
    print("backup error", error_message)
    send_email(f"FALHA - Backup {FILE_NAME}", error_message)

print("############ made by resendev #############")
