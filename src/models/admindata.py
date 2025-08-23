from pydantic import BaseModel


class AdminData(BaseModel):
    available_balance: int = 0
    total_payouts: int = 0
    pending_payouts: int = 0
    total_users: int = 0
    active_surveys: int = 0
    completed_responses: int = 0
    total_surveys_created: int = 0
    expired_surveys: int = None
    this_month_spending: int = None
