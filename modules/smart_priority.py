
"""
Smart Priority Module
VisionGuide AI
"""

OBJECT_PRIORITY = {
    "car": 1,
    "truck": 2,
    "bus": 3,
    "motorcycle": 4,
    "bicycle": 5,
    "person": 6,
    "traffic light": 7,
    "stop sign": 8,
    "chair": 9,
    "bench": 10,
    "dog": 11,
    "cat": 12,
    "backpack": 13,
    "suitcase": 14,
    "cell phone": 15
}


def get_priority_object(objects):
    """
    Return the highest-priority detected object.

    Args:
        objects (list): List of detected object dictionaries.

    Returns:
        dict | None
    """

    if not objects:
        return None

    objects = sorted(
        objects,
        key=lambda obj: OBJECT_PRIORITY.get(
            obj.get("object", ""),
            999
        )
    )

    return objects[0]