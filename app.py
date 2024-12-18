import uvicorn
from fastapi import FastAPI

from db import Base, engine
from routers import spycats, missions

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(spycats.router)
app.include_router(missions.router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=1111, reload=True)
