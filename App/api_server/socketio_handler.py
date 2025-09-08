import socketio

# create an asgi-compatible socket.io server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# the namespace for all draft-related real-time communication
draft_namespace = "/draft"

async def broadcast_draft_update(pick_data: dict):
    """broadcasts that a new pick has been made."""
    await sio.emit('draft_update', pick_data, namespace=draft_namespace)
    print(f"broadcasted 'draft_update' for player {pick_data['player']['player_id']}")

async def broadcast_recommendation_update(recommendations: list):
    """broadcasts new recommendations after a pick."""
    await sio.emit('recommendation_update', {'recommendations': recommendations}, namespace=draft_namespace)
    print("broadcasted 'recommendation_update'")

async def broadcast_error(error_message: str):
    """broadcasts a critical error to clients."""
    await sio.emit('error', {'message': error_message}, namespace=draft_namespace)
    print(f"broadcasted 'error': {error_message}")

@sio.on('connect', namespace=draft_namespace)
async def connect(sid, environ):
    print(f"client connected: {sid}")

@sio.on('disconnect', namespace=draft_namespace)
async def disconnect(sid):
    print(f"client disconnected: {sid}")