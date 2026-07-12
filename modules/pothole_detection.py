"""
VisionGuide AI - Pothole Detection Module

Detects possible potholes only in road region.
Avoids indoor false detections.
"""

import cv2
import numpy as np



def detect_pothole(frame):

    """
    Detect possible potholes.

    Returns:
    {
        "detected": True/False,
        "count": int,
        "boxes": []
    }
    """

    height, width = frame.shape[:2]


    # ---------------------------------
    # Use only bottom road region
    # ---------------------------------

    roi = frame[
        int(height * 0.55):height,
        0:width
    ]



    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )


    # Reduce noise

    blur = cv2.GaussianBlur(
        gray,
        (7,7),
        0
    )


    # Detect dark depressions

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        21,
        5
    )



    # Morphology cleaning

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (7,7)
    )


    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel
    )


    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )



    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )



    potholes = []



    for cnt in contours:


        area = cv2.contourArea(cnt)



        # Ignore noise

        if area < 8000:
            continue



        if area > 120000:
            continue



        x,y,w,h = cv2.boundingRect(cnt)



        # Shape validation

        ratio = w / float(h)


        if ratio < 0.5 or ratio > 4:
            continue



        # Ignore very thin shadows

        if h < 20:
            continue



        # Convert ROI coordinates
        y = y + int(height*0.55)



        potholes.append(
            [
                x,
                y,
                w,
                h
            ]
        )



    return {

        "detected": len(potholes) > 0,

        "count": len(potholes),

        "boxes": potholes

    }