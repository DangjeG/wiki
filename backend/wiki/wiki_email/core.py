from aiosmtplib import SMTPException
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from starlette import status

from wiki.common.exceptions import WikiException, WikiErrorCode
from wiki.config import settings
from wiki.wiki_email.schemas import EmailSchema
from wiki.wiki_email.utils import menage_email_sending_method


class EmailProvider:
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.EMAIL_USERNAME,
        MAIL_PASSWORD=settings.EMAIL_PASSWORD,
        MAIL_FROM=settings.EMAIL_FROM,
        MAIL_PORT=settings.EMAIL_PORT,
        MAIL_SERVER=settings.EMAIL_HOST,
        MAIL_STARTTLS=settings.EMAIL_MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.EMAIL_MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.EMAIL_USE_CREDENTIALS,
        VALIDATE_CERTS=settings.EMAIL_VALIDATE_CERTS
    )

    def __init__(self):
        self.fm = FastMail(self.conf)

    @menage_email_sending_method(settings.EMAIL_SENDING)
    async def send_mail(self, email: EmailSchema):

        html = f"<p>Code: {email.code}</p> "

        message = MessageSchema(
            subject=email.subject,
            recipients=email.email,
            body=html,
            subtype=MessageType.html
        )

        try:
            await self.fm.send_message(message)
        except SMTPException:
            raise WikiException(
                message="Sending a message failed",
                error_code=WikiErrorCode.EMAIL_SENDING_ERROR,
                http_status_code=status.HTTP_400_BAD_REQUEST
            )
