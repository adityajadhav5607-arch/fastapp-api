from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os
import time

app = FastAPI(title="Aditya FastAPI", version="1.0.0")

# Optional: per-instance concurrency guard (helps control per-pod load)
MAX_INPROC = int(os.getenv("MAX_INPROC", "50"))
_sem = asyncio.Semaphore(MAX_INPROC)

class WorkIn(BaseModel):
    x: float

@app.get("/healthz")
def healthz():
    return {"ok": True, "ts": time.time()}

@app.get("/")
def root():
    return {"msg": "FastAPI on AWS. See /docs for Swagger."}

@app.post("/compute")
async def compute(body: WorkIn):
    # simulate CPU/IO (replace with real logic)
    async with _sem:
        await asyncio.sleep(0.05)  # pretend work
        return {"input": body.x, "result": body.x ** 2}
