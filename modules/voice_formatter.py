"""
VisionGuide AI - Voice Formatter

Creates natural voice guidance messages
for visually impaired users.
"""

from typing import Dict, Any

from modules.clock_direction import get_clock_direction



def format_voice_message(obj: Dict[str, Any]) -> str:


    if not isinstance(obj, dict):
        return ""


    object_name = str(
        obj.get("object", "")
    ).lower().strip()


    position = str(
        obj.get("position", "")
    ).upper().strip()


    distance = str(
        obj.get("distance", "")
    ).upper().strip()


    confidence = float(
        obj.get("confidence",0)
    )


    # Clock direction

    clock = get_clock_direction(
        position
    )



    # Confidence handling

    prefix = ""

    if confidence < 0.60:
        prefix = "Possible "



    # ==========================
    # VEHICLES
    # ==========================


    if object_name in [
        "car",
        "bus",
        "truck",
        "motorcycle"
    ]:


        if distance == "VERY CLOSE":

            return (
                f"Warning. "
                f"{object_name} very close "
                f"at {clock}. Stop."
            )


        elif distance == "NEAR":

            return (
                f"{object_name} nearby "
                f"at {clock}. Be careful."
            )


        else:

            return (
                f"{prefix}{object_name} "
                f"detected at {clock}."
            )



    # ==========================
    # PERSON
    # ==========================


    if object_name == "person":


        if distance == "VERY CLOSE":

            return (
                f"Person very close "
                f"at {clock}. Stop."
            )


        return (
            f"Pedestrian ahead "
            f"at {clock}. Continue carefully."
        )



    # ==========================
    # BICYCLE
    # ==========================


    if object_name == "bicycle":

        return (
            f"Bicycle detected "
            f"at {clock}."
        )



    # ==========================
    # OBSTACLES
    # ==========================


    if object_name in [
        "chair",
        "bench"
    ]:

        if position == "CENTER":

            return (
                f"{object_name} blocking path. "
                "Move around."
            )


        return (
            f"{object_name} on your "
            f"{position.lower()}."
        )



    # ==========================
    # ANIMALS
    # ==========================


    if object_name in [
        "dog",
        "cat"
    ]:

        return (
            f"{object_name} detected "
            f"at {clock}. Move carefully."
        )



    # ==========================
    # OTHER
    # ==========================


    if object_name == "backpack":

        return "Bag detected on the ground."



    if object_name == "suitcase":

        return "Suitcase ahead. Avoid collision."



    if object_name == "traffic light":

        return "Traffic signal ahead."



    if object_name == "stop sign":

        return "Stop sign ahead."



    return "Obstacle detected. Proceed carefully."