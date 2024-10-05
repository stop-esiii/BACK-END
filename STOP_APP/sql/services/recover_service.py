from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import RecoverRepository
from STOP_APP.config import STOP_SMTP_HOST, STOP_SMTP_PORT, STOP_SMTP_USER, STOP_SMTP_PASWORD
from STOP_APP.sql.models import VerificationCode
from sqlalchemy import and_
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import string


service = Service()


class RecoverService(RecoverRepository):

    # >>>>>>>>>Function to generate verification code>>>>>>>>>
    def verification_code_generate(self, user):
        # >>>>>>>>>Inactivating previous verifications codes>>>>>>>>>
        verification_codes = VerificationCode.query.filter(and_(
            VerificationCode.id_user==user.id,
            VerificationCode.active==True)).all()
        if len(verification_codes) != 0:
            self.disable_verification_codes(verification_codes)
        # <<<<<<<<<Inactivating previous verifications codes<<<<<<<<<

        # >>>>>>>>>Generate verification code>>>>>>>>>
        characters = string.ascii_letters + string.digits
        verification_code = "".join(random.choices(characters, k=9))
        # <<<<<<<<<Generate verification code<<<<<<<<<

        # Add verification token in DataBase
        self.add_verification_code_to_database(user, verification_code)

        return {"status": True, "verification_code": verification_code}
    # <<<<<<<<<Function to generate verification code<<<<<<<<<

    # >>>>>>>>>Function to send verification code by email>>>>>>>>>
    def verification_code_by_email(self, payload, verification_code):
        # >>>>>>>>>SMTP server settings>>>>>>>>>
        smtp_host = STOP_SMTP_HOST
        smtp_port = STOP_SMTP_PORT
        smtp_user = STOP_SMTP_USER
        smtp_password = STOP_SMTP_PASWORD
        # <<<<<<<<<SMTP server settings<<<<<<<<<

        # >>>>>>>>>Create email message>>>>>>>>>
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = payload["email"]
        msg['Subject'] = "Recuperação de senha - STOP"
        # <<<<<<<<<Create email message<<<<<<<<<

        # >>>>>>>>>Email body>>>>>>>>>
        body = f"Olá,\n\nSegue o código de verificação para recuperação de senha: {verification_code}"
        msg.attach(MIMEText(body, 'plain'))
        # <<<<<<<<<Email body<<<<<<<<<

        # >>>>>>>>>Send email>>>>>>>>>
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, payload["email"], msg.as_string())
        # <<<<<<<<<Send email<<<<<<<<<

        return {"status": True}
    # <<<<<<<<<Function to send verification code by email<<<<<<<<<

    # >>>>>>>>>Function to verify verification code exists>>>>>>>>>
    def validate_verification_code(self, user, payload):
        verification_code = VerificationCode.query.filter(and_(
            VerificationCode.id_user==user.id,
            VerificationCode.active==True)).first()
        if verification_code is None or not verification_code.verify_verification_code(payload["verification_code"]):
            return {"status": False, "msg": "Código de verificação inválido."}
        return {"status": True, "verification_code": verification_code}
    # <<<<<<<<<Function to verify verification code exists<<<<<<<<<

    # >>>>>>>>>Function to change password>>>>>>>>>
    def change_password(self, user, verification_code, payload):
        # Update user password
        self.update_user_password(user, payload)

        # Disable verification code
        self.disable_verification_code(verification_code)

        return {"status": True}
    # <<<<<<<<<Function to change password<<<<<<<<<
