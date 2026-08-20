import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from src.api.schemas import ChatRequest
from src.graph.agent import stream_agent_execution, get_agent_history

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    HTTP Adapter for Agent Execution.
    Adapts the parsed event dictionaries from the deep module into Server-Sent Events (SSE).
    """
    async def sse_generator():
        async for event_dict in stream_agent_execution(request.query, request.provider):
            yield f"data: {json.dumps(event_dict)}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")

@router.get("/history/{thread_id}")
async def get_history(thread_id: str):
    """
    HTTP Adapter for fetching state history.
    """
    try:
        history = await get_agent_history(thread_id)
        return {"history": history}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        print(f"Failed to fetch history for {thread_id}: {e}")
        return {"history": []}
