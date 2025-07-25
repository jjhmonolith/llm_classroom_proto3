from fastapi import APIRouter, HTTPException
from app.models.request_models import OneshotRequest, EvaluatePromptRequest
from app.services.openai_service import OpenAIService
from datetime import datetime

router = APIRouter()

def get_openai_service():
    return OpenAIService()

@router.post("/oneshot")
async def oneshot_llm(request: OneshotRequest):
    """One-shot LLM API 엔드포인트"""
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    openai_service = get_openai_service()
    result = openai_service.generate_oneshot(
        prompt=request.prompt,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.maxTokens
    )
    
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@router.post("/evaluate-prompt")
async def evaluate_prompt(request: EvaluatePromptRequest):
    """RTCF 기준 프롬프트 평가 API 엔드포인트"""
    if not request.currentPrompt or not request.learningObjective:
        raise HTTPException(
            status_code=400, 
            detail="Current prompt and learning objective are required"
        )
    
    try:
        openai_service = get_openai_service()
        
        # 설정을 딕셔너리로 변환
        settings = request.settings.model_dump()
        
        # 이상적인 프롬프트 생성 (제공되지 않은 경우)
        ideal_prompt = request.idealPrompt
        if not ideal_prompt:
            ideal_prompt = openai_service.generate_ideal_prompt(
                request.learningObjective, settings
            )
        
        # RTCF 평가 수행
        evaluation_result = openai_service.evaluate_prompt(
            current_prompt=request.currentPrompt,
            learning_objective=request.learningObjective,
            settings=settings,
            previous_prompt=request.previousPrompt
        )
        
        return {
            "success": True,
            "evaluation": evaluation_result,
            "idealPrompt": ideal_prompt,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "llm-classroom-proto3"
    }