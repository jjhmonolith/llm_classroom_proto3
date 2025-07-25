from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import chat
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LLM Classroom Proto3",
    description="RTCF 프롬프트 학습 플랫폼 - 단일 서버 구조",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 추가
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/api")
async def api_root():
    return {"message": "Welcome to LLM Classroom Proto3 API"}

@app.get("/")
async def root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/index.html")

# Static files for frontend (이것은 마지막에 와야 함)
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    import os
    
    # 환경변수에서 설정 읽기
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    reload = os.getenv("ENV", "development") != "production"
    
    print(f"🚀 Starting LLM Classroom Proto3 server...")
    print(f"📍 Host: {host}")
    print(f"🌐 Port: {port}")
    print(f"🔄 Reload: {reload}")
    print(f"🌍 Environment: {os.getenv('ENV', 'development')}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )