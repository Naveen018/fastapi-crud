from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routers import items, clock_ins
from .database import client,db

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = db  # Set the database in app state
    try:
        await app.state.db.command('ping')
        print("Successfully connected to the database")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
    yield
    client.close()

# Initialize FastAPI with lifespan event handler
app = FastAPI(title="FastAPI CRUD Application", lifespan=lifespan)

app.include_router(items.router, tags=["Items"], prefix="/items")
app.include_router(clock_ins.router, tags=["Clock-Ins"], prefix="/clock-in")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI CRUD Application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
