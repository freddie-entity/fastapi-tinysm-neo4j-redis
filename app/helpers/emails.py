from pydantic import BaseModel, EmailStr
from typing import List
from models.user import UserSchema
from helpers.auth import gen_token
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from config import settings

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_USERNAME,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
)

class EmailSchema(BaseModel):
    email: List[EmailStr]

async def send_email(email : list, user: UserSchema):

    token_data = {
        "username" : user['username'],
        "email" : user['email']
    }

    print(token_data)

    token = await gen_token(token_data)
    template = f"""
        <html>
        <body>
            <div style=" display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p>Thanks for choosing {settings.APP_NAME}, please 
                click on the link below to verify your account</p>

                <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                 href="http://{settings.HOST}:{settings.PORT}/auth/verification/?token={token}">
                    Verify your email
                <a>

                <p style="margin-top:1rem;">If you did not register for {settings.APP_NAME}, 
                please kindly ignore this email and nothing will happen. Thanks<p>
            </div>
        </body>
        </html>
    """

    message = MessageSchema(
        subject="TinySM Account Verification Mail",
        recipients=email,  # List of recipients, as many as you can pass 
        body=template,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)