import json
import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from logic import predict_needs, check_health_alternative, check_expiring_soon

app = FastAPI()

# Load Database
DB_FILE = "db.json"

def load_db():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Data Model for adding new items
class Item(BaseModel):
    name: str
    category: str
    shelf_life_days: int
    last_bought: Optional[str] = None # Defaults to today if empty

# --- API ENDPOINTS ---

@app.get("/")
def home():
    return {"message": "Smart Grocery AI is Running"}

@app.get("/api/inventory")
def get_inventory():
    data = load_db()
    return data["inventory"]

# 1. Prediction Endpoint
@app.get("/api/predictions")
def get_predictions():
    data = load_db()
    suggestions = predict_needs(data["inventory"])
    return {"predictions": suggestions}

# 2. Health & Add Item Endpoint
@app.post("/api/add-item")
def add_item(item: Item):
    data = load_db()
    
    # 1. Check for Healthier Alternative FIRST
    better_option = check_health_alternative(item.name, data["health_map"])
    
    # If a better option exists, return it (Don't save yet)
    if better_option:
        return {
            "status": "suggestion",
            "message": f"Wait! {item.name} is unhealthy. How about buying {better_option} instead?",
            "alternative": better_option,
            "original": item.dict()
        }

    # If no alternative (or user forces add), save to DB
    if not item.last_bought:
        item.last_bought = str(datetime.date.today())

    data["inventory"].append(item.dict())
    save_db(data)
    
    return {"status": "success", "message": f"{item.name} added to inventory."}

# 2b. Force Add (If user ignores health advice)
@app.post("/api/force-add-item")
def force_add_item(item: Item):
    data = load_db()
    if not item.last_bought:
        item.last_bought = str(datetime.date.today())
    
    data["inventory"].append(item.dict())
    save_db(data)
    return {"status": "success", "message": f"{item.name} added (Health advice ignored)."}

# 3. Expiration Alerts Endpoint
@app.get("/api/alerts")
def get_alerts():
    data = load_db()
    alerts = check_expiring_soon(data["inventory"])
    return {"alerts": alerts}