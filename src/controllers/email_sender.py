from flask_mail import Message

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_mail import Mail


def send_otp_mail(mail: 'Mail', otp: str, recipient: str, sender: str) -> None:
    msg = Message(
        subject='SurvEarn OTP Verification',
        recipients=[recipient],
        html=f'Your SurvEar Verification Code is: <b>{otp}</b>',
        sender=f'SurvEarn Team <{sender}>'
    )
    mail.send(msg)
