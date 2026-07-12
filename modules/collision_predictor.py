"""Collision prediction for VisionGuide AI.

This module evaluates tracked objects and returns the highest-priority
collision warning based on object type, distance, and movement state.
"""

from typing import Any, Dict, List, Optional


def predict_collision(tracked_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze tracked objects and return the highest-priority collision alert.

    Args:
        tracked_objects: A list of tracked object dictionaries. Each item
            should contain at least the keys: "object", "position",
            "distance", "movement", and "confidence".

    Returns:
        A dictionary containing:
            - collision: True if a collision risk is detected, otherwise False
            - level: "LOW", "MEDIUM", or "HIGH"
            - message: Human-readable warning text
            - object: The object name associated with the warning
            - recommended_action: Suggested action for the user
    """
    if not tracked_objects:
        return {
            "collision": False,
            "level": "LOW",
            "message": "No immediate collision risk.",
            "object": None,
            "recommended_action": "Continue carefully."
        }

    dangerous_vehicle_types = {"car", "truck", "bus", "motorcycle", "bicycle"}

    best_result: Optional[Dict[str, Any]] = None
    best_priority: Optional[tuple] = None

    for obj in tracked_objects:
        object_name = str(obj.get("object", "")).strip().lower()
        distance = str(obj.get("distance", "")).strip().upper()
        movement = str(obj.get("movement", "")).strip().upper()

        if object_name in dangerous_vehicle_types:
            if movement == "APPROACHING" and distance == "VERY CLOSE":
                result = {
                    "collision": True,
                    "level": "HIGH",
                    "message": "Vehicle approaching quickly.",
                    "object": object_name,
                    "recommended_action": "Stop immediately."
                }
                priority = (1, 0)
            else:
                continue

        elif object_name == "person":
            if movement == "APPROACHING" and distance == "NEAR":
                result = {
                    "collision": True,
                    "level": "MEDIUM",
                    "message": "Pedestrian ahead.",
                    "object": object_name,
                    "recommended_action": "Slow down."
                }
                priority = (2, 0)
            else:
                continue

        else:
            continue

        if best_priority is None or priority < best_priority:
            best_priority = priority
            best_result = result

    if best_result is not None:
        return best_result

    return {
        "collision": False,
        "level": "LOW",
        "message": "No immediate collision risk.",
        "object": None,
        "recommended_action": "Continue carefully."
    }
