from pydantic import BaseModel
from datetime import date


class Redeem(BaseModel):
    _id: str | None = None

    requester_email: str
    requester_userid: str

    payment_partner: str
    payment_receiver_id: str
    payment_receiver_username: str
    payment_amount: int
    request_date: str = date.today().isoformat()

    transaction_date: str | None = None
    transaction_code: str | None = None

    @property
    def id(self):
        return self._id
