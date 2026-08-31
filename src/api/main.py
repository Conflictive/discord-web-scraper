"""Main API route handler.

Creates the API instance and adds the other routes,
also provides endpoints for generic API functions.
"""

from fastapi import FastAPI, status

from src.api.routes.champions import router as champion_router
from src.api.routes.skins import router as skin_router

app = FastAPI(title="API")

app.include_router(champion_router)
app.include_router(skin_router)


@app.get(
    "/health",
    response_model=dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Return message to confirm API is running.",
)
async def health_check():
    """Returns message to confirm API is running.

    Returns:
        dict[str, str]: A dictionary containing the operational status message.
    """
    return {"health": "good"}
