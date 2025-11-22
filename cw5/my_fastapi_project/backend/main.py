"""Entry point for the FastAPI backend application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from routers import chatgpt, items, users

# Create tables (for demo purposes; prefer migrations in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="CRUD FastAPI backend with ChatGPT integration",
    version="1.0.0",
)

# Разрешаем запросы только с фронта
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # раньше было ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(items.router)
app.include_router(users.router)
app.include_router(chatgpt.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FastAPI CRUD API with ChatGPT Integration",
        "chatgpt_available": bool(settings.OPENAI_API_KEY),
        "endpoints": {
            "items": "/items",
            "users": "/users",
            "chatgpt": "/chatgpt",
            "docs": "/docs",
        },
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": "available",
            "chatgpt": "available" if settings.OPENAI_API_KEY else "not_configured",
        },
    }
