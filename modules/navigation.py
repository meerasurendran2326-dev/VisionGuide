"""
VisionGuide AI - Navigation Engine

Combines:
- Path planning
- Risk analysis
- Action generation
- Voice guidance
"""


from modules.path_planner import find_safe_path
from modules.risk_analyzer import analyze_risk
from modules.actions import get_action



# Higher priority = more dangerous

OBJECT_PRIORITY = {

    "bus": 1,
    "truck": 2,
    "car": 3,
    "motorcycle": 4,

    "person": 5,
    "bicycle": 6,
    "dog": 7,

    "chair": 8,
    "bench": 9,

    "backpack": 10,
    "suitcase": 11,
    "cell phone": 12
}



def select_priority_object(objects):

    """
    Select most dangerous object
    based on object + distance + position
    """


    def score(obj):

        object_score = OBJECT_PRIORITY.get(
            obj.get("object"),
            99
        )


        distance = obj.get(
            "distance",
            "MEDIUM"
        )


        # Distance importance

        if distance == "VERY CLOSE":
            distance_score = -20

        elif distance == "NEAR":
            distance_score = -10

        else:
            distance_score = 0



        # Center path more important

        position_score = 0

        if obj.get("position") == "CENTER":
            position_score = -10



        return (
            object_score * 10
            +
            distance_score
            +
            position_score
        )



    return sorted(
        objects,
        key=score
    )[0]




def process_navigation(detected_objects):

    """
    Generate navigation response.

    Returns:

    {
        navigation,
        risk,
        voice,
        priority_object
    }

    """



    # -----------------------------
    # No obstacle
    # -----------------------------

    if not detected_objects:


        return {

            "navigation":
                "MOVE FORWARD",


            "risk":
                "SAFE",


            "voice":
                "Path is clear. Continue straight.",


            "priority_object":
                None
        }



    # -----------------------------
    # Find important object
    # -----------------------------


    highest = select_priority_object(
        detected_objects
    )



    # -----------------------------
    # Navigation decision
    # -----------------------------


    navigation = find_safe_path(
        detected_objects
    )



    # -----------------------------
    # Risk
    # -----------------------------


    risk = analyze_risk(
        detected_objects
    )



    # -----------------------------
    # Action message
    # -----------------------------


    action = get_action(

        highest.get("object"),

        highest.get("position"),

        highest.get("distance")

    )



    # -----------------------------
    # Natural voice
    # -----------------------------


    voice = action



    return {

        "navigation":
            navigation,


        "risk":
            risk,


        "voice":
            voice,


        "priority_object":
            highest

    }