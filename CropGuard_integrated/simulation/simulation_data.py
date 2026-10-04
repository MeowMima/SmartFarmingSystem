
import pandas as pd

FIELD = {
    "name": "North Farm — Plot A",
    "crop": "Corn",
    "size_acres": 2.4,
    "health": 78,
    "last_inspection": "22 September 2026, 10:42 AM",
    "affected_zones": 4,
    "diseases": 2,
    "plants_inspected": 324,
    "disease": "Corn Late Blight",
    "confidence": 91,
    "severity": "High",
    "latest_zone": "B3",
}

DRONE = {
    "battery": 78,
    "signal": "Strong",
    "altitude": 18.4,
    "speed": 4.2,
    "flight_time": "18 min 42 sec",
    "current_zone": "B3",
    "position": (4.4, 2.3),
    "path": [(0.2,0.3),(1.2,0.8),(2.1,0.8),(2.1,1.7),(3.2,1.7),(3.2,2.5),(4.4,2.3)],
}

ZONES = []
severity_by_zone = {
    "A3": ("Medium","Early Blight",16,8),
    "B2": ("Medium","Early Blight",19,9),
    "B3": ("High","Corn Late Blight",31,17),
    "B4": ("Medium","Corn Late Blight",21,10),
    "C3": ("Medium","Early Blight",14,7),
}
for r in range(4):
    for c in range(6):
        zone_id = f"{chr(65+r)}{c+1}"
        sev, disease, area, plants = severity_by_zone.get(zone_id, ("Low","None",4,2))
        ZONES.append({
            "id": zone_id, "severity": sev, "disease": disease,
            "affected_area": area, "affected_plants": plants,
            "recommendation": "Targeted treatment required" if sev == "High" else ("Inspect within 24 hours" if sev == "Medium" else "Continue monitoring"),
            "acre_area": 0.18 if zone_id == "B3" else 0.10,
            "map_x": c + 0.5, "map_y": 3-r + 0.5,
        })

INSPECTIONS = pd.DataFrame([
    {"Date":"22 Sep 2026","Field":"Plot A","Area":"1.8 ac","Diseases":2,"High Severity":1,"Status":"Completed"},
    {"Date":"20 Sep 2026","Field":"Plot A","Area":"1.7 ac","Diseases":1,"High Severity":0,"Status":"Completed"},
    {"Date":"18 Sep 2026","Field":"Plot A","Area":"1.8 ac","Diseases":2,"High Severity":1,"Status":"Completed"},
    {"Date":"15 Sep 2026","Field":"Plot A","Area":"1.6 ac","Diseases":1,"High Severity":0,"Status":"Completed"},
])
