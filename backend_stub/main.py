from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

app = FastAPI(title="Smart Plant Backend Stub", version="0.1.0")


class ReadingIn(BaseModel):
    probeId: str = Field(..., min_length=1)
    timestamp: Optional[str] = None
    moistureRaw: int
    fwVersion: Optional[str] = None
    batteryMv: Optional[int] = None
    rssi: Optional[int] = None


@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/api/v0/readings")
async def ingest_reading(reading: ReadingIn, request: Request):
    payload = reading.model_dump()

    if not payload.get("timestamp"):
        payload["timestamp"] = datetime.now(timezone.utc).isoformat()

    client = request.client.host if request.client else "unknown"
    print("\n[backend_stub] received reading from:", client)
    print(payload)

    return {"ok": True, "received": payload}
