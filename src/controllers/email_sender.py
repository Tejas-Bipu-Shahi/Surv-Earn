from flask_mail import Message
import os
# logging
from icecream import ic

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask_mail import Mail


def send_otp_mail(mail: 'Mail', otp: str, recipient: str, sender: str) -> tuple[bool, str]:
    try:
        msg = Message(
            subject='SurvEarn OTP Verification',
            recipients=[recipient],
            html=f'Your SurvEar Verification Code is: <b>{otp}</b>',
            sender=f'SurvEarn Team <{sender}>'
        )
        mail.send(msg)

        ic(f'Email sent to {recipient}.')

    except Exception as e:
        return False, f'Email Error: {str(e)}'
    return True, 'Success'


def send_redeem_request_mail(mail: 'Mail', requester_email: str, requester_userid: str, payment_partner: str, payment_receiver_id: str,
                             payment_receiver_name: str, payment_amount: int | str, redeem_id: str) -> tuple[bool, str]:
    try:
        msg = Message(
            subject='SurvEarn Redeem Request',
            recipients=[os.getenv('PRIMARY_ADMIN_EMAIL')],
            html=f'''
                <b>requester email: {requester_email}</b><br>
                <b>requester userid: {requester_userid}</b><br>
                <b>payment partner: {payment_partner}</b><br>
                <b>payment receiver id: {payment_receiver_id}</b><br>
                <b>payment receiver name: {payment_receiver_name}</b><br>
                <b>payment amount: {payment_amount}</b><br>
                <b>redeem id: {redeem_id}</b>
                ''',
            sender=f'SurvEarn Team on behalf of <{requester_email}>'
        )
        mail.send(msg)

        ic(f'Redeem request sent.')

    except Exception as e:
        return False, f'Email Error: {str(e)}'
    return True, 'Success'
