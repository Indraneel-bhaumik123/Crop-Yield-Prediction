from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)

    season = Column(String(50), nullable=False)
    continent = Column(String(50), nullable=False)
    area = Column(String(100), nullable=False)
    crop = Column(String(100), nullable=False)

    year = Column(Integer, nullable=False)
    average_rain_fall_mm_per_year = Column(Float, nullable=False)
    pesticides_tonnes = Column(Float, nullable=False)
    avg_temp = Column(Float, nullable=False)

    predicted_yield_hg_per_ha = Column(Float, nullable=False)
    potential_score = Column(Integer, default=85)
    potential_rating = Column(String(30), default="Good")
    model_used = Column(String(50), default="KNN Regressor")

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
