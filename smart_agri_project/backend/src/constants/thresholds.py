
DISEASE_CONFIDENCE_THRESHOLD = 0.60



IRRIGATION_THRESHOLDS = {
    "low": 30,     # Below 30 → needs irrigation
    "medium": 60,  # 30–60 → moderate
    "high": 80     # Above 80 → no irrigation needed
}



RAINFALL_THRESHOLDS = {
    "no_rain": 0,
    "light": 2.5,
    "moderate": 7.6,
    "heavy": 35
}


TEMPERATURE_THRESHOLDS = {
    "low": 15,
    "optimal_min": 20,
    "optimal_max": 30,
    "high": 35
}


YIELD_THRESHOLDS = {
    "low": 1.5,        # < 1.5 tons = poor yield
    "moderate": 3.0,   # 1.5–3.0 tons
    "good": 5.0,       # 3.0–5.0 tons
    "excellent": 7.0   # > 7 tons
}
