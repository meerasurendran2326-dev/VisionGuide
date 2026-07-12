def check_emergency(detected_objects):
    """
    Detect emergency situations.

    Returns:
    {
        "emergency": True/False,
        "message": "...",
        "level": "SAFE/EMERGENCY"
    }
    """

    # High-priority dangerous objects
    dangerous_objects = [
        "bus",
        "truck",
        "car",
        "motorcycle",
        "train"
    ]

    for obj in detected_objects:

        object_name = obj["object"]
        position = obj["position"]
        distance = obj["distance"]

        # Vehicle very close
        if (
            object_name in dangerous_objects
            and distance == "VERY CLOSE"
        ):

            return {
                "emergency": True,
                "level": "EMERGENCY",
                "message":
                    f"Emergency! {object_name} very close on your {position}. Stop immediately."
            }

        # Person very close in front
        if (
            object_name == "person"
            and distance == "VERY CLOSE"
            and position == "CENTER"
        ):

            return {
                "emergency": True,
                "level": "EMERGENCY",
                "message":
                    "Emergency! Person directly ahead. Stop immediately."
            }

    return {
        "emergency": False,
        "level": "SAFE",
        "message": ""
    }