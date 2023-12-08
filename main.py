from fastapi import FastAPI
from pages.postmedia import router as postmedia_router
from pages.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

# Base FastAPI app
app = FastAPI()

# Include routers
app.include_router(postmedia_router)
app.include_router(auth_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"Hi Welcome to PerformaVe!"}