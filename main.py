from fastapi import FastAPI
from pages.postmedia import router as postmedia_router
from pages.auth import router as auth_router

# Base FastAPI app
app = FastAPI()

# Include routers
app.include_router(postmedia_router)
app.include_router(auth_router)

@app.get('/')
async def root():
    return {"Hi Welcome to PerformaVe!"}