"""
Action Generator
VisionGuide AI

Generates human-friendly navigation actions
based on object, position and distance.
"""

from modules.clock_direction import get_clock_direction


def get_action(object_name, position, distance):

    object_name = str(object_name).lower().strip()
    position = str(position).upper().strip()
    distance = str(distance).upper().strip()

    clock = get_clock_direction(position)


    # ==========================
    # PERSON
    # ==========================

    if object_name == "person":

        if distance == "VERY CLOSE" and position == "CENTER":
            return (
                f"Stop immediately. "
                f"Person is very close at {clock}."
            )

        elif distance == "VERY CLOSE":
            return (
                f"Person very close on your {position.lower()}. "
                "Move carefully."
            )

        elif position == "LEFT":
            return (
                f"Person detected at {clock}. "
                "Move slightly right."
            )

        elif position == "RIGHT":
            return (
                f"Person detected at {clock}. "
                "Move slightly left."
            )

        else:
            return (
                f"Person ahead at {clock}. "
                "Continue carefully."
            )


    # ==========================
    # VEHICLES
    # ==========================

    elif object_name in ["car", "bus", "truck", "motorcycle"]:


        if distance == "VERY CLOSE":

            return (
                f"Danger. {object_name} very close "
                f"at {clock}. Stop immediately."
            )


        elif distance == "NEAR":

            return (
                f"{object_name} nearby at {clock}. "
                "Stay alert."
            )


        else:

            return (
                f"{object_name} detected at {clock}. "
                "Continue carefully."
            )


    # ==========================
    # BICYCLE
    # ==========================

    elif object_name == "bicycle":

        return (
            f"Bicycle detected at {clock}. "
            "Stay to one side."
        )


    # ==========================
    # CHAIR / OBSTACLES
    # ==========================

    elif object_name in ["chair", "bench"]:


        if position == "CENTER":

            return (
                f"{object_name} blocking your path. "
                "Move around it."
            )

        else:

            return (
                f"{object_name} detected on your "
                f"{position.lower()}."
            )


    # ==========================
    # ANIMALS
    # ==========================

    elif object_name == "dog":

        return (
            f"Dog detected at {clock}. "
            "Move carefully."
        )


    elif object_name == "cat":

        return (
            f"Cat detected at {clock}. "
            "Continue carefully."
        )


    # ==========================
    # TRAFFIC
    # ==========================

    elif object_name == "traffic light":

        return (
            "Traffic light detected. "
            "Check signal before crossing."
        )


    elif object_name == "stop sign":

        return "Stop sign ahead."


    # ==========================
    # OTHER OBJECTS
    # ==========================

    elif object_name == "backpack":

        return "Bag detected on the ground."


    elif object_name == "suitcase":

        return "Suitcase ahead. Avoid collision."


    elif object_name == "cell phone":

        return "Phone detected."


    else:

        return (
            f"{object_name} detected. "
            "Proceed carefully."
        )