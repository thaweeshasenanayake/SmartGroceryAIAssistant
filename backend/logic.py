import datetime

# 1. Rule-Based Prediction Logic
def predict_needs(inventory):
    """
    Rule: IF (Today - Last Bought) >= (Shelf Life), THEN suggest it.
    """
    suggestions = []
    today = datetime.date.today()
    
    for item in inventory:
        last_bought = datetime.datetime.strptime(item["last_bought"], "%Y-%m-%d").date()
        days_passed = (today - last_bought).days
        
        # If days passed exceeds 80% of shelf life, suggest restocking
        if days_passed >= (item["shelf_life_days"] * 0.8):
            suggestions.append({
                "item": item["name"],
                "reason": f"Bought {days_passed} days ago (Shelf life: {item['shelf_life_days']} days)"
            })
            
    return suggestions

# 2. Recommendation System Logic
def check_health_alternative(item_name, health_map):
    """
    Rule: IF item in health_map, THEN return healthy alternative.
    """
    # Simple dictionary lookup (Case insensitive)
    for unhealthy, healthy in health_map.items():
        if unhealthy.lower() == item_name.lower():
            return healthy
    return None

# 3. Expiration Tracking Logic
def check_expiring_soon(inventory):
    """
    Rule: IF (Expiry Date - Today) <= 2 days, THEN alert.
    """
    alerts = []
    today = datetime.date.today()

    for item in inventory:
        last_bought = datetime.datetime.strptime(item["last_bought"], "%Y-%m-%d").date()
        expiry_date = last_bought + datetime.timedelta(days=item["shelf_life_days"])
        days_left = (expiry_date - today).days

        if 0 <= days_left <= 2:
            alerts.append({
                "item": item["name"],
                "days_left": days_left,
                "status": "Critical"
            })
        elif days_left < 0:
             alerts.append({
                "item": item["name"],
                "days_left": days_left,
                "status": "Expired"
            })
            
    return alerts