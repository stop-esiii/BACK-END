from STOP_APP.sql.services.service import Service
from STOP_APP.config import STOP_SMTP_HOST, STOP_SMTP_PORT, STOP_SMTP_USER, \
                            STOP_SMTP_PASWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class VerificationCodeService(Service):

    # >>>>>>>>>Function to send verification code by email>>>>>>>>>
    def verification_by_email(self, email, subject):
        verification_code = 0
        # >>>>>>>>>SMTP server settings>>>>>>>>>
        smtp_host = STOP_SMTP_HOST
        smtp_port = STOP_SMTP_PORT
        smtp_user = STOP_SMTP_USER
        smtp_password = STOP_SMTP_PASWORD
        # <<<<<<<<<SMTP server settings<<<<<<<<<

        # >>>>>>>>>Create email message>>>>>>>>>
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = email
        msg["Subject"] = subject
        # <<<<<<<<<Create email message<<<<<<<<<

        # >>>>>>>>>Email body>>>>>>>>>
        body = f"""
        Olá,<br><br>
        Segue o código de verificação para redefinição de senha: <strong>{verification_code}</strong>
        """
        msg.attach(MIMEText(body, "html"))
        # <<<<<<<<<Email body<<<<<<<<<

        # >>>>>>>>>Send email>>>>>>>>>
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, email, msg.as_string())
        # <<<<<<<<<Send email<<<<<<<<<
    # <<<<<<<<<Function to send verification code by email<<<<<<<<<
