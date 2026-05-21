from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from contextlib import asynccontextmanager
import json
from datetime import datetime
from typing import List, Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed

app = FastAPI(lifespan=lifespan)

# Define data models
class EventData(BaseModel):
    id: str
    name: str
    startTime: str
    competitorCount: int
    avgTimeMinutes: int
    avgTimeSeconds: int
    durationInSeconds: int
    endTime: str

class ScheduleData(BaseModel):
    name: Optional[str] = "Untitled Schedule"
    events: List[EventData]

class ScheduleResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    message: Optional[str] = None
    error: Optional[str] = None

# Database file path
DB_FILE = Path("database.json")

def init_db():
    """Initialize database.json if it doesn't exist"""
    if not DB_FILE.exists():
        default_db = {
            "schedules": [],
            "currentScheduleId": None
        }
        with open(DB_FILE, "w") as f:
            json.dump(default_db, f, indent=2)

def load_db():
    """Load database from JSON file"""
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data: dict):
    """Save database to JSON file"""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML template"""
    template_path = Path("templates/index.html")
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return "<h1>Event Timing Calculator</h1><p>templates/index.html not found</p>"

@app.get("/api/schedule")
async def get_schedule():
    """
    GET endpoint to retrieve the most recent saved schedule
    Returns 204 No Content if no schedule exists
    """
    try:
        db = load_db()

        if not db["schedules"]:
            return {"success": True, "data": None}

        # Return the most recent schedule
        current_schedule = db["schedules"][-1]

        return {
            "success": True,
            "data": current_schedule
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule")
async def post_schedule(schedule: ScheduleData):
    """
    POST endpoint to save or update the current schedule
    Persists schedule to database.json
    """
    try:
        db = load_db()

        # Create new schedule entry
        schedule_entry = {
            "id": f"schedule-{datetime.now().timestamp()}",
            "name": schedule.name or "Untitled Schedule",
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.utcnow().isoformat() + "Z",
            "events": [event.dict() for event in schedule.events]
        }

        # Add to schedules list
        db["schedules"].append(schedule_entry)
        db["currentScheduleId"] = schedule_entry["id"]

        # Save to file
        save_db(db)

        return {
            "success": True,
            "message": "Schedule saved successfully",
            "data": {
                "id": schedule_entry["id"],
                "savedAt": schedule_entry["updatedAt"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid schedule data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
