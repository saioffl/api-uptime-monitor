from fastapi import FastAPI

from .routes import user, monitor, check, history
from .database import Base, engine

app = FastAPI(title="api-uptime-monitor")

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "api-uptime-monitor is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(monitor.router)
app.include_router(user.router)
app.include_router(check.router)
app.include_router(history.router)
