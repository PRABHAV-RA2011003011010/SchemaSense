from fastapi import FastAPI
from backend.api.routers import query
from fastapi.middleware.cors import CORSMiddleware

fastapi_app = FastAPI(title="SchemaSense API", version="1.0.0")

# Include routers
fastapi_app.include_router(query.router, prefix="/query", tags=["Query"])


fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)