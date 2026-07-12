# ----------------------------------------
# Object Priority
# Higher value = More Dangerous
# ----------------------------------------

OBJECT_WEIGHT = {
    "car": 10,
    "bus": 10,
    "truck": 10,
    "motorcycle": 9,

    "person": 8,
    "bicycle": 7,
    "dog": 7,

    "chair": 5,
    "bench": 5,
    "backpack": 3,
    "suitcase": 3,
    "cell phone": 1,
    "cat": 2
}


def find_safe_path(detected_objects):
    """
    Decide safest direction.

    Returns:
        Move Left
        Move Right
        Move Forward
        Stop
    """

    left_score = 0
    center_score = 0
    right_score = 0

    for obj in detected_objects:

        position = obj["position"]
        distance = obj["distance"]
        object_name = obj["object"]

        weight = OBJECT_WEIGHT.get(object_name, 1)

        # Distance multiplier
        if distance == "VERY CLOSE":
            weight *= 4

        elif distance == "NEAR":
            weight *= 3

        elif distance == "MEDIUM":
            weight *= 2

        # Add score
        if position == "LEFT":
            left_score += weight

        elif position == "CENTER":
            center_score += weight

        else:
            right_score += weight

    # ----------------------------------
    # Decision
    # ----------------------------------

    # Center blocked
    if center_score >= 20:
        return "STOP"

    # Forward path clear
    if center_score == 0:
        return "MOVE FORWARD"

    # Choose safer side
    if left_score < right_score:
        return "MOVE LEFT"

    elif right_score < left_score:
        return "MOVE RIGHT"

    else:
        return "MOVE SLOWLY"