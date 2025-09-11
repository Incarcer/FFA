# api_server/routers/draft.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from api_server import services
import pandas as pd

router = APIRouter(prefix="/draft", tags=["draft"])

# This endpoint would typically initialize the draft state on demand.
# It should ONLY be called once to set up the draft.
@router.post("/start")
async def start_draft():
    """
    Initializes the draft state and prepares the recommendation engine.
    This should be called once the user is ready to start a new draft session.
    """
    try:
        services.initialize_draft_state()
        # Optionally, start a background task for polling Yahoo API for real picks
        # services.start_draft_polling_task() # Uncomment if you implement this
        return JSONResponse({"message": "Draft session started successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start draft session: {str(e)}")

@router.get("/state")
async def get_draft_state():
    """
    Retrieves the current state of the draft, including board, teams, and available players.
    """
    if services.DRAFT_TRACKER is None:
        raise HTTPException(status_code=404, detail="Draft session not initialized. Call /draft/start first.")
    
    return JSONResponse(services.DRAFT_TRACKER.get_current_state())

@router.post("/make-pick/{player_id}")
async def make_pick(player_id: str):
    """
    Records a player selection in the draft.
    """
    if services.DRAFT_TRACKER is None:
        raise HTTPException(status_code=404, detail="Draft session not initialized.")
    
    completed_pick = services.DRAFT_TRACKER.add_pick(player_id)
    if not completed_pick:
        raise HTTPException(status_code=400, detail="Could not record pick. Player might be unavailable or draft is over.")
    
    # After a pick, recalculate recommendations for the next team and potentially broadcast
    # (This logic might move to services.py for cleaner background processing)
    current_state = services.DRAFT_TRACKER.get_current_state()
    next_pick_info = current_state.get('current_pick_info')
    
    if next_pick_info:
        next_team_id = next_pick_info['team_id']
        recommendations = services.RECOMMENDATION_ENGINE.get_recommendations(
            draft_tracker=services.DRAFT_TRACKER,
            team_id=next_team_id
        )
        # You would typically broadcast these recommendations via WebSockets here
        # (e.g., await services.broadcast_recommendations(recommendations))
        return JSONResponse({"message": "Pick recorded", "pick": completed_pick.to_dict(), "next_recommendations": recommendations})
    else:
        return JSONResponse({"message": "Pick recorded. Draft is complete."})

@router.get("/recommendations")
async def get_current_recommendations():
    """
    Retrieves player recommendations for the team currently on the clock.
    """
    if services.DRAFT_TRACKER is None or services.RECOMMENDATION_ENGINE is None:
        raise HTTPException(status_code=404, detail="Draft session not initialized.")
    
    current_state = services.DRAFT_TRACKER.get_current_state()
    current_pick_info = current_state.get('current_pick_info')

    if not current_pick_info:
        return JSONResponse({"message": "Draft is complete, no more recommendations."})

    team_id = current_pick_info['team_id']
    recommendations = services.RECOMMENDATION_ENGINE.get_recommendations(
        draft_tracker=services.DRAFT_TRACKER,
        team_id=team_id
    )
    return JSONResponse({"recommendations": recommendations})

