from app.api.schemas import ChatRequest, ChatResponse, Metrics, TraceStep


def build_placeholder_chat_response(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        answer=(
            "Aurelia Ledger is ready for the first implementation phase. "
            "This placeholder will later route the request through LangGraph "
            "to document, macro, policy, and SQL agents."
        ),
        agent="orchestrator-placeholder",
        sources=[],
        trace=[
            TraceStep(step="receive", detail=f"Received {len(request.message)} characters."),
            TraceStep(step="route", detail="Selected placeholder orchestrator."),
            TraceStep(step="respond", detail="Returned fixed response shape for frontend integration."),
        ],
        metrics=Metrics(),
    )
