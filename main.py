from fastapi import FastAPI

app = FastAPI(title="api-uptime-monitor")


@app.get("/")
def read_root():
    return {"message": "api-uptime-monitor is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
