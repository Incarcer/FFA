import sys
import os
from fastapi import FastAPI
import socketio
from dotenv import load_dotenv
from api_server.routers import yahoo_fantasy

# Load environment variables from .env file
load_dotenv()


from .routers import auth, draft, players
from .socketio_handler import sio
    


app = FastAPI(
    title="Fantasy Football Draft Assistant API",
    version="1.0.0",
)


# Correctly instantiate and mount the Socket.IO ASGI app
# The path must match the client-side configuration
sio_app = socketio.ASGIApp(sio, socketio_path="socket.io")

app.include_router(yahoo_fantasy.router, prefix="/api/v1", tags=["Fantasy"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(draft.router, prefix="/api/v1", tags=["Draft"])
app.include_router(players.router, prefix="/api/v1", tags=["Players"])


# Mount the Socket.IO app
app.mount("/", sio_app)


@app.get("/health")
async def health_check():
    """A simple health check endpoint."""
    return {"status": "ok"}
