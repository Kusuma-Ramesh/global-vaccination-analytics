from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import lookups, coverage, disease, vaccines, analytics

settings = get_settings()

app = FastAPI(
    title="Vaccination Analytics API",
    description="API for exploring global WHO vaccination coverage, disease incidence, "
                 "reported cases, vaccine introduction and vaccine schedule data.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lookups.router, prefix="/api")
app.include_router(coverage.router, prefix="/api")
app.include_router(disease.router, prefix="/api")
app.include_router(vaccines.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Vaccination Analytics API is running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
