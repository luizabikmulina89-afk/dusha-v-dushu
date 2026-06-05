from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: int
    pseudonym: str = Field(min_length=1, max_length=100)
    about_me: str = Field(default="", max_length=200)
    gender: str
    orientation: str
    age: int = Field(ge=18, le=99)
    city: str
    pref_gender: str
    pref_age_min: int = Field(default=18, ge=18)
    pref_age_max: int = Field(default=60, le=99)
    pref_relation_type: str

class BirthDataUpdate(BaseModel):
    birth_date: str
    birth_time: Optional[str] = None
    birth_city: Optional[str] = None
    full_name: Optional[str] = None

class HardFiltersUpdate(BaseModel):
    wants_children: str
    wants_marriage: str
    religion_own: str
    religion_partner: str
    smoking: str
    alcohol: str

class TestAnswerSubmit(BaseModel):
    test_type: str
    answers: List[Union[str, int]]

class UserResponse(BaseModel):
    id: int
    telegram_id: int
    pseudonym: str
    about_me: str
    age: int
    city: str
    is_premium: bool
    completed_systems: int

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    life_path_number: Optional[int]
    zodiac_sign: Optional[str]
    moon_sign: Optional[str]
    hd_type: Optional[str]
    matrix_key_number: Optional[int]
    psychotype: Optional[str]
    attachment_style: Optional[str]
    love_language_primary: Optional[str]
    enneagram_type: Optional[int]
    completed_systems: int

    class Config:
        from_attributes = True

class MessageSend(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
