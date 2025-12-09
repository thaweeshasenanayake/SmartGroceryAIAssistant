import json
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from logic import predict_needs, check_health_alternative, check_expiring_soon

app = FastAPI()
DB_FILE = "db.json"

# --- HELPERS ---
def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"inventory": [], "health_map": {}}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- SMART LOOKUP HELPER ---
def find_history_data(name, inventory):
    """
    Scans history to see if we already know this item's Category or Shelf Life.
    """
    for item in inventory:
        if item["name"].lower() == name.lower():
            return item["category"], item["shelf_life_days"]
    return None, None

# --- MODELS ---
class Item(BaseModel):
    name: str
    category: str
    shelf_life_days: int
    last_bought: Optional[str] = None 

# --- ENDPOINTS ---

@app.get("/api/inventory")
def get_inventory():
    return load_db()["inventory"]

@app.get("/api/predictions")
def get_predictions():
    data = load_db()
    suggestions = predict_needs(data["inventory"])
    return {"predictions": suggestions}

@app.get("/api/alerts")
def get_alerts():
    data = load_db()
    alerts = check_expiring_soon(data["inventory"])
    return {"alerts": alerts}

@app.post("/api/add-item")
def add_item(item: Item):
    data = load_db()
    
    # --- INTELLIGENT AUTO-FILL ---
    # If user leaves it as "General" or default days, try to learn from history
    hist_category, hist_days = find_history_data(item.name, data["inventory"])
    
    if hist_category and item.category == "General":
        item.category = hist_category # Auto-correct category
    
    if hist_days and item.shelf_life_days == 7: # Assuming 7 is default in frontend
        item.shelf_life_days = hist_days # Auto-correct shelf life

    # --- HEALTH CHECK ---
    better_option = check_health_alternative(item.name, data["health_map"])
    if better_option:
        return {
            "status": "suggestion",
            "message": f"Wait! '{item.name}' might be unhealthy. Try '{better_option}' instead?",
            "alternative": better_option,
            "original": item.dict()
        }

    # If safe, proceed to save
    return save_to_inventory(data, item)

@app.post("/api/force-add-item")
def force_add_item(item: Item):
    data = load_db()
    # Even in force add, run the auto-fill logic to keep data clean
    hist_category, hist_days = find_history_data(item.name, data["inventory"])
    
    if hist_category and item.category == "General":
        item.category = hist_category
        
    return save_to_inventory(data, item)

def save_to_inventory(data, item):
    if not item.last_bought:
        item.last_bought = str(datetime.date.today())

    # Check if item exists, update it instead of adding duplicate
    item_exists = False
    for i, existing in enumerate(data["inventory"]):
        if existing["name"].lower() == item.name.lower():
            data["inventory"][i] = item.dict() # Update existing entry
            item_exists = True
            break
    
    if not item_exists:
        data["inventory"].append(item.dict())

    save_db(data)
    return {"status": "success", "message": f"{item.name} saved under {item.category}."}