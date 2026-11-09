from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ==================== AI MENTOR SCHEMAS ====================

class AIMentorQuestion(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000, description="User's question about finance/investing")


class CourseRecommendation(BaseModel):
    course_name: str
    course_id: str
    reason: str


class FeatureRecommendation(BaseModel):
    feature_name: str
    feature_path: str
    description: str


class AIMentorResponse(BaseModel):
    question: str
    answer: str
    course_recommendations: List[CourseRecommendation] = []
    feature_recommendations: List[FeatureRecommendation] = []
    model_used: str
    tokens_used: Optional[int]
    timestamp: datetime
