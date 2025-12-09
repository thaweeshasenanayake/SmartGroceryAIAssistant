import datetime
import difflib # <--- Standard library for text comparison (Fuzzy Matching)

# 1. AI Rule: Smart Prediction
def predict_needs(inventory):
    suggestions = []
    today = datetime.date.today()
    
    for item in inventory:
        try:
            last_bought = datetime.datetime.strptime(item["last_bought"], "%Y-%m-%d").date()
            days_passed = (today - last_bought).days
            
            # AI Logic: Calculate "Urgency Score"
            # If 80% of shelf life is gone, it's time to buy.
            threshold = item["shelf_life_days"] * 0.8
            
            if days_passed >= threshold:
                urgency = "High" if days_passed > item["shelf_life_days"] else "Medium"
                
                suggestions.append({
                    "item": item["name"],
                    "reason": f"You bought this {days_passed} days ago. (Urgency: {urgency})"
                })
        except ValueError:
            continue # Skip invalid dates
            
    return suggestions

# 2. AI Rule: Fuzzy Health Matching (NLP-lite)
def check_health_alternative(item_name, health_map):
    """
    Uses fuzzy matching to find unhealthy items.
    Example: Input "Lays Chips" -> Matches "Chips" -> Suggests "Nuts"
    """
    # 1. Direct Match
    if item_name in health_map:
        return health_map[item_name]
    
    # 2. Fuzzy/Partial Match (The "Smart" part)
    # Check if any key word from health_map exists in the user input
    item_lower = item_name.lower()
    
    for unhealthy_key in health_map:
        # If "soda" is inside "orange soda", trigger warning
        if unhealthy_key.lower() in item_lower:
             return health_map[unhealthy_key]
             
        # Optional: Use SequenceMatcher for typos (e.g., "Chps" -> "Chips")
        similarity = difflib.SequenceMatcher(None, unhealthy_key.lower(), item_lower).ratio()
        if similarity > 0.8: # 80% similar
            return health_map[unhealthy_key]

    return None

# 3. Expiration Logic
def check_expiring_soon(inventory):
    alerts = []
    today = datetime.date.today()

    for item in inventory:
        try:
            last_bought = datetime.datetime.strptime(item["last_bought"], "%Y-%m-%d").date()
            expiry_date = last_bought + datetime.timedelta(days=item["shelf_life_days"])
            days_left = (expiry_date - today).days

            if 0 <= days_left <= 2:
                alerts.append({"item": item["name"], "days_left": days_left, "status": "Critical"})
            elif days_left < 0:
                 alerts.append({"item": item["name"], "days_left": days_left, "status": "Expired"})
        except ValueError:
            continue
            
    return alerts