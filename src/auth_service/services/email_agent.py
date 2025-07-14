""" Email service to send emails """

from email.message import EmailMessage

import aiosmtplib
from auth_service.core.config import settings


async def send_verification_email(email: str, token: str):
    """Send verification email

    Args:
        email (str): Email address
        token (str): Verification token

    Returns:
        None
    """
    message = EmailMessage()
    message["From"] = settings.NO_REPLY_EMAIL
    message["To"] = email
    message["Subject"] = "Verify Your Email"
    message.add_alternative(
        f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
                border-bottom: 1px solid #dddddd;
            }}
            .header h1 {{
                margin: 0;
                color: #333333;
            }}
            .body {{
                padding: 20px;
                text-align: center;
            }}
            .body p {{
                font-size: 16px;
                color: #666666;
                line-height: 1.5;
            }}
            .body a {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                font-size: 16px;
                color: #ffffff;
                background-color: #007BFF;
                text-decoration: none;
                border-radius: 5px;
            }}
            .footer {{
                text-align: center;
                padding: 10px 0;
                border-top: 1px solid #dddddd;
                margin-top: 20px;
            }}
            .footer p {{
                font-size: 14px;
                color: #999999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Verify Your Email</h1>
            </div>
            <div class="body">
                <p>Thank you for signing up! Please click the button below to
                verify your email address.</p>
                <a href="http://{settings.HOST_NAME}/api/v1/auth/verify?
                token={token}">Verify Email</a>
            </div>
            <div class="footer">
                <p>If you did not sign up for this account, you can ignore
                this email.</p>
            </div>
        </div>
    </body>
    </html>
    """,
        subtype="html",
    )

    await aiosmtplib.send(
        message, hostname=settings.SMTP_HOST, port=settings.SMTP_PORT
    )
