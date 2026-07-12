"""
Scene Analyzer
Understands the surrounding environment.
"""


def analyze_scene(detected_objects, summary=False):
    """
    Analyze the surroundings.

    Args:
        detected_objects (list): List of detected objects.
        summary (bool): Return voice-friendly summary if True.

    Returns:
        str
    """

    if not detected_objects:
        if summary:
            return "You are walking safely. No nearby obstacles."
        return "No obstacles nearby."

    people = 0
    vehicles = 0
    chairs = 0
    animals = 0

    left = 0
    center = 0
    right = 0

    object_names = []

    for obj in detected_objects:

        name = obj.get("object", "")
        pos = obj.get("position", "")

        object_names.append(name)

        if name == "person":
            people += 1

        elif name in [
            "car",
            "bus",
            "truck",
            "motorcycle",
            "bicycle"
        ]:
            vehicles += 1

        elif name in [
            "chair",
            "bench"
        ]:
            chairs += 1

        elif name in [
            "dog",
            "cat"
        ]:
            animals += 1

        if pos == "LEFT":
            left += 1

        elif pos == "CENTER":
            center += 1

        elif pos == "RIGHT":
            right += 1

    description = []

    if people == 1:
        description.append("One pedestrian ahead.")

    elif people > 1:
        description.append(f"{people} pedestrians ahead.")

    if vehicles == 1:
        description.append("One vehicle nearby.")

    elif vehicles > 1:
        description.append(f"{vehicles} vehicles nearby.")

    if chairs > 0:
        description.append(f"{chairs} obstacle ahead.")

    if animals > 0:
        description.append("Animal nearby.")

    if center == 0:
        description.append("Center path is clear.")

    elif left < right:
        description.append("Move slightly left.")

    elif right < left:
        description.append("Move slightly right.")

    else:
        description.append("Proceed carefully.")

    # Voice summary every few seconds
    if summary:

        unique_objects = list(dict.fromkeys(object_names))

        return (
            "You are walking safely. "
            + "Nearby: "
            + ", ".join(unique_objects)
            + ". "
            + description[-1]
        )

    return " ".join(description)