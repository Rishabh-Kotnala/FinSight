import os
from contextlib import nullcontext

import uvicorn
from fastapi import FastAPI
from langfuse import Langfuse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from langchain_core.messages import SystemMessage, HumanMessage
from config.config import RequestObject
from MarketInsight.components.agent import agent
from MarketInsight.utils.logger import get_logger

logger = get_logger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")
LANGFUSE_HOST = os.getenv("LANGFUSE_HOST")

langfuse = None
if LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY and LANGFUSE_HOST:
    langfuse = Langfuse(
        public_key=LANGFUSE_PUBLIC_KEY,
        secret_key=LANGFUSE_SECRET_KEY,
        host=LANGFUSE_HOST,
    )
else:
    logger.info("Langfuse disabled because one or more Langfuse environment variables are missing.")


def langfuse_observation(**kwargs):
    if langfuse is None:
        return nullcontext(None)
    return langfuse.start_as_current_observation(**kwargs)


def update_observation(observation, **kwargs):
    if observation is not None:
        observation.update(**kwargs)


def extract_stream_text(content):
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                block_type = block.get("type")
                if block_type in {"tool_call", "tool_use", "function_call"}:
                    continue
                text = block.get("text") or block.get("content")
                if isinstance(text, str):
                    parts.append(text)
        return "".join(parts)

    return str(content)


@app.get("/health")
async def health_check():
    """Health check endpoint for service monitoring and keep-alive pings"""
    return {"status": "ok", "message": "Service is running"}


@app.post("/api/chat")
async def chat(request: RequestObject):
    config = {'configurable': {'thread_id': request.threadId}}
    async def generate():
        try:
            # Create a span for the entire request
            with langfuse_observation(
                as_type="span", 
                name="chat-request",
                input=request.prompt.content
            ) as span:
                # Set user_id as metadata
                update_observation(span, metadata={"user_id": request.threadId})
                
                # Create a nested generation for the LLM/agent call
                with langfuse_observation(
                    as_type="generation",
                    name="agent-stream",
                    model="llama-3.3-70b-versatile",
                    input=request.prompt.content
                ) as generation:
                    
                    full_response = ""
                    for token, _ in agent.stream(
                        {
                            'messages': [
                                SystemMessage(content="You are a professional stock market analyst. For every user query, first determine whether a relevant tool can provide accurate or real-time data. If an appropriate tool exists, you must use it before answering. If the user does not provide an exact stock ticker, use the available tool to identify or resolve the correct ticker when required. Only when no suitable tool applies should you respond using your own reasoning and general market knowledge. Never guess, assume, or fabricate any financial data."),
                                HumanMessage(content=request.prompt.content)
                            ]
                        },
                        stream_mode='messages',
                        config=config
                    ):
                        text = extract_stream_text(getattr(token, "content", token))
                        if not text:
                            continue

                        full_response += text
                        yield text
                    
                    # Update generation with the complete output
                    update_observation(generation, output=full_response)
                
                # Update span with completion status
                update_observation(span, output="Request completed successfully")
                
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            # Keep the streaming response valid so the frontend can stop its
            # loading state and show an actionable error to the user.
            yield (
                "\n\nUnable to generate a response because the AI service could not be reached. "
                "Set a valid GROQ_API_KEY in the backend .env file "
                "and restart the backend server."
            )
    
    return StreamingResponse(generate(), media_type='text/event-stream',
        headers={
            'cache-control': 'no-cache, no-transform', 
            'connection': 'keep-alive'
        })

if __name__ == '__main__':
    logger.info("App Initiated Successfully")
    uvicorn.run(app, host='0.0.0.0', port=8000)
