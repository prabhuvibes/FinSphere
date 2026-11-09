from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import auth, learning, assets, portfolio, dashboard, user, ai_mentor

app = FastAPI(
    title="FinSphere API",
    description="Financial learning and paper trading platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(learning.router)
app.include_router(assets.router)
app.include_router(portfolio.router)
app.include_router(dashboard.router)
app.include_router(user.router)
app.include_router(ai_mentor.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to FinSphere API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
