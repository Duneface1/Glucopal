from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Receive a user message and return a diabetes-care-aware AI reply.
    Integrates with an LLM (OpenAI / local model) via chat_service.
    """
    reply = await generate_reply(request.message)
    return ChatResponse(reply=reply)
