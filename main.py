from fastapi import FastAPI
from src.routes.members import member_router

app = FastAPI(
    title="SACCO Manager API",
    description="A REST API for a SACCO management web service",
    version="1.0.0"
)

app.include_router(member_router, prefix="/members")

