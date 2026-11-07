from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime


# ==================== LESSON SCHEMAS ====================

class LessonBase(BaseModel):
    title: str
    content: str
    display_order: int
    estimated_duration_minutes: int


class LessonResponse(LessonBase):
    id: UUID4
    course_id: UUID4
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== COURSE SCHEMAS ====================

class CourseBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty_level: str
    display_order: int


class CourseListResponse(CourseBase):
    id: UUID4
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CourseDetailResponse(CourseListResponse):
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True


# ==================== LEARNING PROGRESS SCHEMAS ====================

class ProgressCreate(BaseModel):
    lesson_id: UUID4


class ProgressResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    lesson_id: UUID4
    completed_at: datetime

    class Config:
        from_attributes = True


class UserProgressSummary(BaseModel):
    total_lessons: int
    completed_lessons: int
    completion_percentage: float
