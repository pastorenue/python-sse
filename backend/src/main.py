import time
import datetime
import asyncio
import json
import uuid
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]
STREAMING_INTERVAL = 1  # seconds
RETRY_TIMEOUT = 14000  # milliseconds

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

CLIENTS = {}

@app.get("/events")
async def events(request: Request):
    client_id = str(uuid.uuid4())
    CLIENTS[client_id] = True

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    CLIENTS.pop(client_id, None)
                    break

                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                yield {
                    "event": "update",
                    "retry": RETRY_TIMEOUT,
                    "id": client_id,
                    "data": json.dumps({
                        "message": f"{current_time}: Hello from the server!",
                        "timestamp": datetime.datetime.now().isoformat(sep="T", timespec="auto"),
                    }),
                }

                await asyncio.sleep(STREAMING_INTERVAL)
        except Exception as e:
            CLIENTS.pop(client_id, None)
            print(f"Error: {e}")
    
    return EventSourceResponse(event_generator(), media_type="text/event-stream")
