from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str = "bearer"
    username: str


class PredictionInput(BaseModel):
    season: str
    continent: str
    area: str
    crop: str
    year: int = Field(..., ge=1990, le=2100)
    average_rain_fall_mm_per_year: float = Field(..., ge=0)
    pesticides_tonnes: float = Field(..., ge=0)
    avg_temp: float = Field(..., ge=-20, le=60)


class FactorImpact(BaseModel):
    rainfall: str
    temperature: str
    pesticides: str


class PredictionResponse(BaseModel):
    success: bool
    username: str
    season: str
    continent: str
    country: str
    crop: str
    year: int
    predicted_yield_hg_per_ha: float
    unit: str = "hg/ha"
    potential_score: int
    potential_rating: str
    confidence: str
    status: str
    model_used: str
    factors_impact: Dict[str, str]
    history_id: int
    timestamp: str


class HistoryItem(BaseModel):
    id: int
    season: str
    continent: str
    area: str
    crop: str
    year: int
    average_rain_fall_mm_per_year: float
    pesticides_tonnes: float
    avg_temp: float
    predicted_yield_hg_per_ha: float
    potential_score: Optional[int] = 85
    potential_rating: Optional[str] = "Good"
    model_used: Optional[str] = "KNN Regressor"
    timestamp: Optional[str] = None
