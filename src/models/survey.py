from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class SurveyStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


class Survey(BaseModel):
    survey_title: str
    company_name: str
    reward_per_completion: float
    expiration_date: date
    _id: str | None = None
    survey_url: str
    short_description: str

    full_description: str = ''
    status: SurveyStatus = SurveyStatus.ACTIVE
    estimated_time: int | None = None
    date_posted: date = date.today()
    questions_count: int = 0
    category: str = ''
