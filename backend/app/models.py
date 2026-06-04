from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    pseudonym = Column(String(100), nullable=False)
    about_me = Column(String(200), default="")
    gender = Column(String(20))
    orientation = Column(String(30))
    age = Column(Integer)
    city = Column(String(100))
    photos = Column(JSON, default=list)

    pref_gender = Column(String(20))
    pref_age_min = Column(Integer, default=18)
    pref_age_max = Column(Integer, default=99)
    pref_relation_type = Column(String(30))

    wants_children = Column(String(30))
    wants_marriage = Column(String(30))
    religion_own = Column(String(50))
    religion_partner = Column(String(50))
    smoking = Column(String(20))
    alcohol = Column(String(20))

    is_active = Column(Boolean, default=True)
    is_paused = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    premium_expires = Column(DateTime, nullable=True)
    daily_views_used = Column(Integer, default=0)
    daily_views_reset = Column(DateTime, nullable=True)
    super_likes_used_today = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    sent_likes = relationship("Like", foreign_keys="Like.from_user_id", back_populates="from_user")
    received_likes = relationship("Like", foreign_keys="Like.to_user_id", back_populates="to_user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    birth_date = Column(String(20))
    birth_time = Column(String(10))
    birth_city = Column(String(100))
    full_name = Column(String(200))

    life_path_number = Column(Integer)
    destiny_number = Column(Integer)
    soul_number = Column(Integer)
    personality_number = Column(Integer)
    zodiac_sign = Column(String(30))
    moon_sign = Column(String(30))
    hd_type = Column(String(30))
    matrix_key_number = Column(Integer)

    psychotype = Column(String(10))
    attachment_style = Column(String(20))
    love_language_primary = Column(String(30))
    enneagram_type = Column(Integer)

    family_type = Column(String(30))
    family_position = Column(String(20))
    parents_relationship = Column(String(20))

    nutrition = Column(String(20))
    sport = Column(String(20))
    height = Column(Integer)
    education = Column(String(50))
    marital_status = Column(String(30))
    has_children = Column(Boolean)

    completed_systems = Column(Integer, default=0)

    user = relationship("User", back_populates="profile")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_super = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_user_id], back_populates="sent_likes")
    to_user = relationship("User", foreign_keys=[to_user_id], back_populates="received_likes")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    user1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    compatibility_score = Column(Float)
    compatibility_breakdown = Column(JSON)
    systems_used = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, nullable=True)
    is_together = Column(Boolean, default=False)
    together_since = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=True)
    media_url = Column(String(500), nullable=True)
    media_type = Column(String(20), default="text")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
