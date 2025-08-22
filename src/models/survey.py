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
    reward_per_completion: int
    expiration_date: date
    _id: str | None = None
    survey_url: str
    short_description: str

    full_description: str | None
    status: SurveyStatus | None = None
    estimated_time: int | None = None
    date_posted: date | None = None
    questions_count: int | None = None
    category: str | None = None
