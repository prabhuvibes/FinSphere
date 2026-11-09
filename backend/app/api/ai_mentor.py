from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
import os
import re
from groq import Groq

from app.database import get_db
from app.models.user import User
from app.core.security import verify_token
from app.schemas.ai_mentor import (
    AIMentorQuestion,
    AIMentorResponse,
    CourseRecommendation,
    FeatureRecommendation
)

router = APIRouter(prefix="/api/ai", tags=["AI Mentor"])
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# Course and feature mappings
AVAILABLE_COURSES = {
    "Financial Basics": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "description": "Understanding fundamental concepts of personal finance and investing"
    },
    "Understanding Risk and Return": {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "description": "Learn about the relationship between investment risk and potential returns"
    },
    "Introduction to Stocks": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "description": "What are stocks, how they work, and basic stock market concepts"
    },
    "Portfolio Diversification": {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "description": "Why and how to diversify your investment portfolio"
    }
}

PLATFORM_FEATURES = {
    "explore-stocks": {
        "path": "/explore",
        "description": "Browse and search Indian stocks (RELIANCE, TCS, HDFC, INFY, etc.)"
    },
    "create-portfolio": {
        "path": "/portfolio/create",
        "description": "Start paper trading with ₹10 lakh virtual cash"
    },
    "view-courses": {
        "path": "/learn",
        "description": "Access all learning courses and track your progress"
    },
    "my-portfolio": {
        "path": "/portfolio",
        "description": "View your portfolios, holdings, and P&L"
    }
}


def get_system_prompt():
    """Generate system prompt with FinSphere context"""
    courses_list = "\n".join([f"- {name}: {info['description']}" for name, info in AVAILABLE_COURSES.items()])

    return f"""You are FinSphere AI Mentor - a specialized financial education assistant for the FinSphere platform.

YOUR EXPERTISE: You ONLY answer questions about finance, investing, stock markets, and personal finance concepts.

AVAILABLE COURSES ON FINSPHERE:
{courses_list}

PLATFORM FEATURES:
- Stock exploration (Indian stocks: RELIANCE, TCS, HDFCBANK, INFY, and more)
- Paper trading with virtual ₹10 lakh cash
- Portfolio tracking with real-time P&L calculation
- Learning progress tracking

YOUR RULES:
1. Answer ONLY finance/investing questions
2. For non-finance questions, politely refuse and explain your role
3. Recommend relevant courses using EXACTLY this format: [COURSE:Course Name]
4. Suggest platform features using EXACTLY this format: [FEATURE:feature-name]
5. Keep answers concise (2-3 paragraphs)
6. Be encouraging and educational
7. Don't give specific buy/sell recommendations
8. Use Indian market examples when relevant

RESPONSE STRATEGY:
- For basic concepts → Explain + recommend relevant course
- For "how to start" questions → Explain + suggest create-portfolio or view-courses
- For stock questions → Explain + suggest explore-stocks feature
- For portfolio questions → Explain + suggest my-portfolio feature

REJECTION EXAMPLES:
User: "What's the weather?" → "I'm FinSphere's financial mentor. I only help with investing and finance concepts. Ask me about stocks, portfolios, or investing!"
User: "Tell me a joke" → "I focus on financial education. Let's talk about investing! What would you like to learn?"

Remember: Be friendly, educational, and ALWAYS tie answers back to FinSphere features when relevant!"""


def parse_ai_response(answer_text):
    """Parse AI response for course and feature recommendations"""
    courses = []
    features = []

    # Find course recommendations
    course_pattern = r'\[COURSE:(.*?)\]'
    course_matches = re.findall(course_pattern, answer_text)

    for course_name in course_matches:
        if course_name in AVAILABLE_COURSES:
            courses.append(CourseRecommendation(
                course_name=course_name,
                course_id=AVAILABLE_COURSES[course_name]["id"],
                reason=AVAILABLE_COURSES[course_name]["description"]
            ))

    # Find feature recommendations
    feature_pattern = r'\[FEATURE:(.*?)\]'
    feature_matches = re.findall(feature_pattern, answer_text)

    for feature_key in feature_matches:
        if feature_key in PLATFORM_FEATURES:
            features.append(FeatureRecommendation(
                feature_name=feature_key.replace("-", " ").title(),
                feature_path=PLATFORM_FEATURES[feature_key]["path"],
                description=PLATFORM_FEATURES[feature_key]["description"]
            ))

    return courses, features


@router.post("/mentor", response_model=AIMentorResponse)
def ask_ai_mentor(
    question_data: AIMentorQuestion,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ask the AI Mentor a question about finance and investing.

    The AI will:
    - Answer finance/investing questions only
    - Recommend relevant FinSphere courses
    - Suggest platform features
    - Reject non-finance questions politely
    """

    # Get Groq API key from environment
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your-groq-api-key-here":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service not configured. Please add GROQ_API_KEY to .env file"
        )

    try:
        # Initialize Groq client
        client = Groq(api_key=groq_api_key)

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": get_system_prompt()
                },
                {
                    "role": "user",
                    "content": question_data.question
                }
            ],
            model="openai/gpt-oss-120b",  # Available Groq model
            temperature=0.7,
            max_tokens=500
        )

        # Get response
        answer = chat_completion.choices[0].message.content
        tokens_used = chat_completion.usage.total_tokens if hasattr(chat_completion, 'usage') else None

        # Parse for recommendations
        course_recommendations, feature_recommendations = parse_ai_response(answer)

        # Return response
        return AIMentorResponse(
            question=question_data.question,
            answer=answer,
            course_recommendations=course_recommendations,
            feature_recommendations=feature_recommendations,
            model_used="openai/gpt-oss-120b",
            tokens_used=tokens_used,
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
