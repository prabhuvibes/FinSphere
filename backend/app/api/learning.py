from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database import get_db
from app.models.learning import Course, Lesson, LearningProgress
from app.schemas.learning import (
    CourseListResponse,
    CourseDetailResponse,
    LessonResponse,
    ProgressCreate,
    ProgressResponse,
    UserProgressSummary
)
from app.models.user import User
from app.core.security import verify_token
from datetime import datetime

router = APIRouter(prefix="/api/learning", tags=["Learning"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    token = credentials.credentials
    email = verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# ==================== COURSE ENDPOINTS ====================

@router.get("/courses", response_model=List[CourseListResponse])
def get_all_courses(
    category: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db)
):
    """Get all published courses with optional filters"""
    query = db.query(Course).filter(Course.is_published == True)

    if category:
        query = query.filter(Course.category == category)

    if difficulty:
        query = query.filter(Course.difficulty_level == difficulty)

    courses = query.order_by(Course.display_order).all()
    return courses


@router.get("/courses/{course_id}", response_model=CourseDetailResponse)
def get_course_detail(course_id: str, db: Session = Depends(get_db)):
    """Get course details with all lessons"""
    course = db.query(Course).filter(
        Course.id == course_id,
        Course.is_published == True
    ).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course


# ==================== LESSON ENDPOINTS ====================

@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    """Get lesson content by ID"""
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id,
        Lesson.is_published == True
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return lesson


# ==================== PROGRESS ENDPOINTS ====================

@router.post("/progress", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
def track_progress(
    progress: ProgressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Track or update user's learning progress"""

    # Check if lesson exists
    lesson = db.query(Lesson).filter(Lesson.id == progress.lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    # Check if progress already exists
    existing_progress = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id,
        LearningProgress.lesson_id == progress.lesson_id
    ).first()

    if existing_progress:
        # Already completed - return existing
        return existing_progress
    else:
        # Create new progress record (mark as completed)
        new_progress = LearningProgress(
            user_id=current_user.id,
            lesson_id=progress.lesson_id,
            completed_at=datetime.utcnow()
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return new_progress


@router.get("/progress/summary", response_model=UserProgressSummary)
def get_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's overall learning progress summary"""

    # Total published lessons
    total_lessons = db.query(func.count(Lesson.id)).filter(
        Lesson.is_published == True
    ).scalar()

    # Completed lessons by user
    completed_lessons = db.query(func.count(LearningProgress.id)).filter(
        LearningProgress.user_id == current_user.id
    ).scalar()

    # Calculate completion percentage
    completion_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0

    return {
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "completion_percentage": round(completion_percentage, 2)
    }


@router.get("/progress/course/{course_id}")
def get_course_progress(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's progress for a specific course"""

    # Get all lessons in the course
    lessons = db.query(Lesson).filter(
        Lesson.course_id == course_id,
        Lesson.is_published == True
    ).all()

    if not lessons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found or has no lessons"
        )

    lesson_ids = [lesson.id for lesson in lessons]

    # Get user's progress for these lessons
    progress_records = db.query(LearningProgress).filter(
        LearningProgress.user_id == current_user.id,
        LearningProgress.lesson_id.in_(lesson_ids)
    ).all()

    # Create progress map
    progress_map = {p.lesson_id: p for p in progress_records}

    # Build response
    lesson_progress = []
    for lesson in lessons:
        progress = progress_map.get(lesson.id)
        lesson_progress.append({
            "lesson_id": lesson.id,
            "lesson_title": lesson.title,
            "completed": progress is not None,
            "completed_at": progress.completed_at if progress else None
        })

    completed_count = sum(1 for lp in lesson_progress if lp["completed"])
    total_count = len(lesson_progress)

    return {
        "course_id": course_id,
        "total_lessons": total_count,
        "completed_lessons": completed_count,
        "completion_percentage": round((completed_count / total_count * 100), 2) if total_count > 0 else 0,
        "lessons": lesson_progress
    }
