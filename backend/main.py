from fastapi import FastAPI
from backend.api.routers import query

fastapi_app = FastAPI(title="SchemaSense API", version="1.0.0")

# Include routers
fastapi_app.include_router(query.router, prefix="/query", tags=["Query"])