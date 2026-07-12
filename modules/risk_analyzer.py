"""
VisionGuide AI - Risk Analyzer

Calculates navigation risk based on:
- Object type
- Distance
- Position
"""



HIGH_RISK_OBJECTS = {
    "car",
    "bus",
    "truck",
    "motorcycle"
}


MEDIUM_RISK_OBJECTS = {
    "person",
    "bicycle",
    "dog"
}


LOW_RISK_OBJECTS = {
    "chair",
    "bench",
    "backpack",
    "suitcase",
    "cell phone",
    "cat"
}



def analyze_risk(detected_objects):

    """
    Returns:
        SAFE
        CAUTION
        DANGER
    """

    if not detected_objects:
        return "SAFE"



    highest_risk = "SAFE"



    for obj in detected_objects:


        object_name = str(
            obj.get("object","")
        ).lower()


        distance = str(
            obj.get("distance","")
        ).upper()


        position = str(
            obj.get("position","")
        ).upper()



        # -----------------------------
        # VERY CLOSE
        # -----------------------------

        if distance == "VERY CLOSE":


            # Vehicle
            if object_name in HIGH_RISK_OBJECTS:

                return "DANGER"



            # Person only danger if in path

            elif object_name in MEDIUM_RISK_OBJECTS:


                if position == "CENTER":

                    return "DANGER"

                else:

                    highest_risk = "CAUTION"



            else:

                if position == "CENTER":

                    highest_risk = "CAUTION"



        # -----------------------------
        # NEAR
        # -----------------------------

        elif distance == "NEAR":


            if object_name in HIGH_RISK_OBJECTS:

                if position == "CENTER":
                    highest_risk = "DANGER"

                else:
                    highest_risk = "CAUTION"



            elif object_name in MEDIUM_RISK_OBJECTS:


                if position == "CENTER":

                    if highest_risk != "DANGER":
                        highest_risk = "CAUTION"



            elif object_name in LOW_RISK_OBJECTS:


                if position == "CENTER":

                    highest_risk = "CAUTION"



        # -----------------------------
        # MEDIUM DISTANCE
        # -----------------------------

        elif distance == "MEDIUM":


            if object_name in HIGH_RISK_OBJECTS:

                if highest_risk == "SAFE":

                    highest_risk = "CAUTION"



    return highest_risk