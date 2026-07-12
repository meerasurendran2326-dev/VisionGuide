"""Crossing analysis for VisionGuide AI.

This module evaluates whether a zebra crossing is safe to use based on
traffic signal state, nearby vehicles, and crowding conditions.
"""

from typing import Dict, List, Any


def analyze_crossing(traffic_status: str, zebra_detected: bool, detected_objects: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Analyze the safety of a zebra crossing.

    Args:
        traffic_status: Traffic light state. Expected values are "RED",
            "GREEN", "YELLOW", or "NONE".
        zebra_detected: Whether a zebra crossing was detected.
        detected_objects: List of detected objects with at least an
            "object" and "distance" field.

    Returns:
        A dictionary with:
            - "score": "NONE" | "SAFE" | "MODERATE" | "UNSAFE"
            - "message": Human-readable guidance message
    """
    if not zebra_detected:
        return {
            "score": "NONE",
            "message": "No crossing detected."
        }

    # Priority rule: nearby vehicles always override crossing signal state.
    dangerous_vehicle_types = {"bus", "truck", "car", "motorcycle", "bicycle"}

    for obj in detected_objects:
        object_name = str(obj.get("object", "")).strip().lower()
        distance = str(obj.get("distance", "")).strip().upper()

        if object_name in dangerous_vehicle_types and distance == "VERY CLOSE":
            return {
                "score": "UNSAFE",
                "message": "Vehicle approaching. Do not cross."
            }

    # Count people occupying the crossing area.
    people_count = 0
    for obj in detected_objects:
        if str(obj.get("object", "")).strip().lower() == "person":
            people_count += 1

    if people_count >= 2:
        return {
            "score": "MODERATE",
            "message": "Crowded crossing."
        }

    # Evaluate traffic signal status if no vehicle hazard is present.
    traffic_status = str(traffic_status).strip().upper()

    if traffic_status == "GREEN":
        return {
            "score": "SAFE",
            "message": "You may cross carefully."
        }

    if traffic_status == "RED":
        return {
            "score": "UNSAFE",
            "message": "Wait for the green signal."
        }

    if traffic_status == "YELLOW":
        return {
            "score": "MODERATE",
            "message": "Prepare to cross."
        }

    # Fallback for missing or unknown traffic state.
    return {
        "score": "MODERATE",
        "message": "Cross with caution."
    }
