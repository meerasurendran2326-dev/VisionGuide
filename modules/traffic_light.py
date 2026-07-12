"""
VisionGuide AI - Traffic Light Detector

Detects traffic light color only when
a traffic light object is detected by YOLO.
"""

import cv2
import numpy as np



def detect_traffic_light(frame, traffic_object_detected=False):
    """
    Detect traffic light state.

    Args:
        frame: OpenCV frame
        traffic_object_detected: YOLO detected traffic light exists or not

    Returns:
        {
            "status":"RED/GREEN/YELLOW/NONE"
        }
    """


    # ---------------------------------
    # No traffic light object
    # ---------------------------------

    if not traffic_object_detected:

        return {
            "status": "NONE",
            "red_pixels": 0,
            "green_pixels": 0,
            "yellow_pixels": 0
        }



    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )


    # ---------------------------------
    # RED
    # ---------------------------------

    lower_red1 = np.array(
        [0,120,70]
    )

    upper_red1 = np.array(
        [10,255,255]
    )


    lower_red2 = np.array(
        [170,120,70]
    )

    upper_red2 = np.array(
        [180,255,255]
    )


    red_mask = (
        cv2.inRange(
            hsv,
            lower_red1,
            upper_red1
        )
        +
        cv2.inRange(
            hsv,
            lower_red2,
            upper_red2
        )
    )



    # ---------------------------------
    # GREEN
    # ---------------------------------

    green_mask = cv2.inRange(
        hsv,
        np.array([40,50,50]),
        np.array([90,255,255])
    )



    # ---------------------------------
    # YELLOW
    # ---------------------------------

    yellow_mask = cv2.inRange(
        hsv,
        np.array([20,100,100]),
        np.array([35,255,255])
    )



    red_pixels = cv2.countNonZero(red_mask)

    green_pixels = cv2.countNonZero(green_mask)

    yellow_pixels = cv2.countNonZero(yellow_mask)



    status = "NONE"



    # ---------------------------------
    # Minimum pixel validation
    # ---------------------------------

    if red_pixels > 300:

        status = "RED"


    elif green_pixels > 300:

        status = "GREEN"


    elif yellow_pixels > 300:

        status = "YELLOW"



    return {

        "status": status,

        "red_pixels": red_pixels,

        "green_pixels": green_pixels,

        "yellow_pixels": yellow_pixels

    }