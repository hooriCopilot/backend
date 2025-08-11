import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logger import logger
from api import auth, passwords, quiz
from core.database import Base, engine

# Create DB tables if not exists
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status code: {response.status_code}")
    return response

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(passwords.router, prefix="/api/passwords", tags=["passwords"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])

@app.get("/")
def root():
    return {"success": True, "message": "API is running."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)